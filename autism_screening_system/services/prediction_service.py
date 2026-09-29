from pathlib import Path

import joblib    # read trainedmodel

import pandas as pd

# load the trained model and define the feature columns and datafream tables similar to excel sheet

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "model.pkl"
FEATURE_COLUMNS = [f"A{i}" for i in range(1, 11)] + ["Age"]
model = joblib.load(MODEL_PATH)


def _encode_answer(answer):
    if answer in {"Yes", "Maybe"}:
        return 1
    if answer == "No":
        return 0
    raise ValueError("Each screening answer must be Yes, Maybe, or No.")


def predict_screening(answers, age):
    if not 1 <= age <= 100:
        raise ValueError("Age must be between 1 and 100.")
    values = [_encode_answer(answers[column]) for column in FEATURE_COLUMNS[:-1]]
    patient = pd.DataFrame([values + [age]], columns=FEATURE_COLUMNS)
    prediction = model.predict(patient)[0]
    probability = float(model.predict_proba(patient)[0][1])
    return ("YES" if prediction == 1 else "NO"), probability
