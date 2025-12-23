import requests
import pandas as pd

url = "http://127.0.0.1:5001/invocations"

data = {
    "dataframe_split": {
        "columns": [
            "Age", "Sex", "Chest pain type", "BP", "Cholesterol",
            "FBS over 120", "EKG results", "Max HR",
            "Exercise angina", "ST depression", "Slope of ST",
            "Number of vessels fluro", "Thallium"
        ],
        "data": [[63, 1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 6]]
    }
}

response = requests.post(url, json=data)
print(response.json())