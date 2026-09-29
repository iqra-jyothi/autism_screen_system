import joblib
import pandas as pd


# Path of trained model
MODEL_PATH = "model/model.pkl"


# Load the trained Random Forest model
model = joblib.load(MODEL_PATH)


def predict_autism(
    A1,
    A2,
    A3,
    A4,
    A5,
    A6,
    A7,
    A8,
    A9,
    A10,
    Age
):

    # Create patient data
    patient = pd.DataFrame([{
        "A1": A1,
        "A2": A2,
        "A3": A3,
        "A4": A4,
        "A5": A5,
        "A6": A6,
        "A7": A7,
        "A8": A8,
        "A9": A9,
        "A10": A10,
        "Age": Age
    }])

    # Make prediction
    prediction = model.predict(patient)[0]

    # Get prediction probability
    probability = model.predict_proba(patient)[0]

    # Convert prediction to readable result
    if prediction == 1:
        result = "YES"
    else:
        result = "NO"

    return result, probability[1]