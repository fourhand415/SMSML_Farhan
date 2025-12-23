# ===== IMPORT =====
import mlflow
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ===== EXPERIMENT =====
mlflow.set_experiment("Heart Disease - Basic")
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# ===== LOAD DATA =====
df = pd.read_csv("heart_disease_preprocessing.csv")

X = df.drop("Heart Disease", axis=1)
y = df["Heart Disease"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ===== TRAIN + LOG =====
with mlflow.start_run():
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    mlflow.log_param("model", "RandomForestClassifier")
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")

    print("Accuracy:", acc)