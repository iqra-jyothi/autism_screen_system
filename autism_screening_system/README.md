# AI-Based Autism Spectrum Disorder Screening and Risk Prediction System

This Flask application provides an AI-assisted autism screening indication using the existing trained Random Forest model. It is **not a medical diagnosis**.

## Features

- Responsive HTML/CSS/JavaScript interface
- Ten-question behavioral screening form
- Existing `model/model.pkl` integration with exact training features
- Risk result and probability dashboard
- Interactive analytics dashboard at `/dashboard`
- Independent demo-mode email and SOS service modules
- No database or sensitive-data persistence by default

## Technology Stack

Python, Flask, pandas, scikit-learn, joblib, python-dotenv, HTML5, CSS3, and JavaScript.

## Installation and Run

From this folder in VS Code:

```powershell
.\venv\Scripts\pytho-m pip install -r requirements.txtn.exe 
.\venv\Scripts\python.exe app.py
```

Open `http://127.0.0.1:5000`. For development, copy `.env.example` to `.env` and set a strong `FLASK_SECRET_KEY`.

## Folder Structure

```text
app.py                 Flask routes and application entry point
config.py              Environment-backed configuration
model/model.pkl        Existing trained model (preserved)
services/              Prediction, email, and SOS services
templates/             HTML pages
static/                CSS and JavaScript
visualization/         Dataset and model analytics charts
data/                  Existing datasets
```

## Machine Learning Integration

The model was trained with `A1`, `A2`, ..., `A10`, and `Age`, in that order. The prediction service encodes `Yes` and `Maybe` as `1`, `No` as `0`, and sends a pandas DataFrame with those exact columns to `model/model.pkl`. No scaler or label encoder was present in the existing project, so none is applied.

## Email and SOS Setup

Both modules default to demo mode. Copy `.env.example` to `.env`; keep `EMAIL_ENABLED=False` and `SOS_ENABLED=False` until an approved provider and explicit authorization are configured. API integrations are intentionally not enabled or hardcoded.

## Analytics Dashboard

Open `http://127.0.0.1:5000/dashboard` to view dataset overview, class distribution, age analysis, question responses, feature importance, correlation analysis, confusion matrix, and holdout accuracy. Charts are generated only from columns present in `data/asd_training.csv`; the dataset has no gender column, so no gender chart is shown.

## Future Improvements

Add a consent-aware database, authentication, audit logging, provider adapters, automated tests, and clinical review of the questionnaire and model.

## Disclaimer

This software is an educational screening aid. Its output is not a medical diagnosis and must not replace assessment by a qualified healthcare professional.
