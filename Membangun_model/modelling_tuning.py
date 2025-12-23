import dagshub
import mlflow
import mlflow.sklearn

import pandas as pd
import matplotlib.pyplot as plt
import json

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix

dagshub.init(
    repo_owner="fourhand415",
    repo_name="SMSML_Farhan",
    mlflow=True
)

mlflow.set_experiment("Heart Disease - Advanced")


# Load Data
df = pd.read_csv("heart_disease_preprocessing.csv")
X = df.drop("Heart Disease", axis=1)
y = df["Heart Disease"]


# Hyperparameter Tuning

params = {
    "n_estimators": [50, 100],
    "max_depth": [5, 10]
}

model = RandomForestClassifier(random_state=42)

grid = GridSearchCV(
    estimator=model,
    param_grid=params,
    cv=3,
    scoring="accuracy"
)


# MLFLOW RUN
with mlflow.start_run():

    grid.fit(X, y)
    best_model = grid.best_estimator_

    # ===== Log Parameters =====
    mlflow.log_params(grid.best_params_)

    # ===== Evaluation =====
    y_pred = best_model.predict(X)
    acc = accuracy_score(y, y_pred)

    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("cv_score", grid.best_score_)

    # ===== Log Model =====
    mlflow.sklearn.log_model(
        best_model,
        name="model"
    )

    # ===== Confusion Matrix Artifact =====
    cm = confusion_matrix(y, y_pred)
    plt.imshow(cm)
    plt.title("Training Confusion Matrix")
    plt.colorbar()
    plt.savefig("training_confusion_matrix.png")
    plt.close()

    mlflow.log_artifact("training_confusion_matrix.png")

    # ===== Metric Info Artifact =====
    metric_info = {
        "accuracy": acc,
        "cv_score": grid.best_score_
    }

    with open("metric_info.json", "w") as f:
        json.dump(metric_info, f)

    mlflow.log_artifact("metric_info.json")