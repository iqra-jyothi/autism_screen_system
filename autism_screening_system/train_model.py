import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


# traine the model and save it to model/model.pkl file. This model will be used for prediction in the application.

# ==========================================
# 1. Load dataset
# ==========================================

DATASET_PATH = "data/asd_training.csv"

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# 2. Define features and target
# ==========================================

features = [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9",
    "A10",
    "Age"
]

target = "Class"


X = df[features]
y = df[target]


print("\nFeatures used for training:")
print(features)

print("\nTarget:")
print(target)


# ==========================================
# 3. Split dataset
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 4. Create Random Forest
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)


# ==========================================
# 5. Train model
# ==========================================

print("\nTraining Random Forest...")

model.fit(X_train, y_train)

print("Training completed!")


# ==========================================
# 6. Make predictions
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 7. Calculate accuracy
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n======================================")
print("MODEL PERFORMANCE")
print("======================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


# ==========================================
# 8. Classification report
# ==========================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["NO", "YES"]
    )
)


# ==========================================
# 9. Confusion matrix
# ==========================================

print("\nConfusion Matrix:")

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)


# ==========================================
# 10. Save model
# ==========================================

MODEL_PATH = "model/model.pkl"

joblib.dump(
    model,
    MODEL_PATH
)

print("\n======================================")
print("MODEL SAVED")
print("======================================")

print(
    f"Model saved to: {MODEL_PATH}"
)