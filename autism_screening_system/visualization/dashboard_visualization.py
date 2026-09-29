from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "asd_training.csv"
MODEL_PATH = ROOT / "model" / "model.pkl"
FEATURE_COLUMNS = [f"A{i}" for i in range(1, 11)] + ["Age"]
TARGET_COLUMN = "Class"


def _chart_html(figure):
    return figure.to_html(full_html=False, include_plotlyjs=False, config={"displayModeBar": False})


def build_dashboard():
    dataframe = pd.read_csv(DATASET_PATH)
    missing_columns = set(FEATURE_COLUMNS + [TARGET_COLUMN]) - set(dataframe.columns)
    if missing_columns:
        raise ValueError(f"Dashboard dataset is missing columns: {', '.join(sorted(missing_columns))}")

    model = joblib.load(MODEL_PATH)
    features = dataframe[FEATURE_COLUMNS]
    target = dataframe[TARGET_COLUMN]
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.20, random_state=42, stratify=target
    )
    evaluation_model = model
    evaluation_model.fit(x_train, y_train)
    predictions = evaluation_model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions, labels=[0, 1])

    class_counts = dataframe[TARGET_COLUMN].map({0: "Lower Risk", 1: "Higher Risk"}).value_counts()
    class_chart = px.bar(
        x=class_counts.index, y=class_counts.values, labels={"x": "Screening Result", "y": "Records"},
        title="Autism Screening Class Distribution", color=class_counts.index,
        color_discrete_sequence=["#2563eb", "#dc2626"],
    )
    age_chart = px.histogram(dataframe, x="Age", color=TARGET_COLUMN, nbins=20,
                             title="Age Distribution of Participants",
                             labels={TARGET_COLUMN: "Screening Class"})
    risk_age_chart = px.box(dataframe, x=TARGET_COLUMN, y="Age", points=False,
                            title="Age by Autism Screening Result",
                            labels={TARGET_COLUMN: "Screening Class"})

    response_counts = dataframe[[f"A{i}" for i in range(1, 11)]].sum().sort_values()
    response_chart = px.bar(x=response_counts.values, y=response_counts.index, orientation="h",
                            title="Positive Behavioral Responses by Question",
                            labels={"x": "Positive Responses", "y": "Question"})
    importances = getattr(model, "feature_importances_", None)
    importance_chart = None
    if importances is not None:
        importance = pd.Series(importances, index=FEATURE_COLUMNS).sort_values()
        importance_chart = px.bar(x=importance.values, y=importance.index, orientation="h",
                                  title="Feature Importance", labels={"x": "Importance", "y": "Feature"})

    correlation = px.imshow(dataframe[FEATURE_COLUMNS].corr(), text_auto=".2f",
                            color_continuous_scale="Blues", title="Feature Correlation Analysis")
    matrix_chart = px.imshow(matrix, text_auto=True, x=["Predicted Lower", "Predicted Higher"],
                             y=["Actual Lower", "Actual Higher"], color_continuous_scale="Blues",
                             title="Confusion Matrix")
    return {
        "records": len(dataframe),
        "features": len(FEATURE_COLUMNS),
        "missing": int(dataframe[FEATURE_COLUMNS + [TARGET_COLUMN]].isna().sum().sum()),
        "accuracy": accuracy * 100,
        "class_chart": _chart_html(class_chart),
        "age_chart": _chart_html(age_chart),
        "risk_age_chart": _chart_html(risk_age_chart),
        "response_chart": _chart_html(response_chart),
        "importance_chart": _chart_html(importance_chart) if importance_chart else None,
        "correlation_chart": _chart_html(correlation),
        "matrix_chart": _chart_html(matrix_chart),
    }


def probability_chart(probability):
    figure = go.Figure(go.Pie(
        labels=["Higher Risk", "Lower Risk"], values=[probability, 1 - probability],
        hole=0.62, marker={"colors": ["#dc2626", "#2563eb"]},
    ))
    figure.update_layout(showlegend=True, margin={"t": 20, "b": 20, "l": 20, "r": 20})
    return _chart_html(figure)
