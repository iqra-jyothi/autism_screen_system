from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for

from config import FLASK_SECRET_KEY
from services.auth_service import authenticate_user, create_user, init_auth_db
from services.email_service import send_screening_email
from services.prediction_service import predict_screening
# from services.sos_service import send_sos_alert
from visualization.dashboard_visualization import build_dashboard, probability_chart


app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY
init_auth_db()


@app.get("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        if not name or not email or not password:
            flash("Please complete every registration field.", "error")
        elif len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
        elif password != confirmation:
            flash("Passwords do not match.", "error")
        elif create_user(name, email, password) is None:
            flash("An account with this email already exists.", "error")
        else:
            flash("Your account has been created. Please sign in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = authenticate_user(email, password)
        if user is None:
            flash("Email or password is incorrect.", "error")
        else:
            session["user"] = user
            return redirect(url_for("home"))
    return render_template("login.html")


@app.get("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


@app.get("/dashboard")
def dashboard():
    return render_template("dashboard.html", dashboard=build_dashboard())


@app.route("/screening", methods=["GET"])
def screening():
    return render_template("screening.html")


@app.post("/predict")
def predict():
    patient = {
        "name": request.form.get("name", "").strip(),
        "age": request.form.get("age", "").strip(),
        "gender": request.form.get("gender", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
    }
    answers = {f"A{i}": request.form.get(f"A{i}", "") for i in range(1, 11)}

    if not patient["name"] or not patient["age"] or not patient["gender"]:
        flash("Please complete all personal information fields.", "error")
        return redirect(url_for("screening"))
    if not all(answers.values()):
        flash("Please answer all ten screening questions.", "error")
        return redirect(url_for("screening"))

    try:
        result, probability = predict_screening(answers, int(patient["age"]))
    except (TypeError, ValueError) as error:
        flash(str(error), "error")
        return redirect(url_for("screening"))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    session["result"] = {
        **patient,
        "prediction": result,
        "probability": probability,
        "timestamp": timestamp,
    }
    email_status = send_screening_email(**session["result"])
    session["email_status"] = email_status
    return redirect(url_for("result"))


@app.get("/result")
def result():
    screening_result = session.get("result")
    if not screening_result:
        return redirect(url_for("screening"))
    return render_template(
        "result.html", result=screening_result,
        email_status=session.pop("email_status", None),
        probability_chart=probability_chart(screening_result["probability"]),
    )


@app.get("/about")
def about():
    return render_template("about.html")


@app.get("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
