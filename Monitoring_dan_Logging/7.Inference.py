import json
import requests

SERVE_URL = "http://localhost:5001/invocations"

def build_payload():
    columns = [
            "Age", "Sex", "Chest pain type", "BP", "Cholesterol",
            "FBS over 120", "EKG results", "Max HR",
            "Exercise angina", "ST depression", "Slope of ST",
            "Number of vessels fluro", "Thallium"
    ]

    data = [[63, 1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 6]]

    return {"dataframe_split": {"columns": columns, "data": data}}

def main():
    payload = build_payload()
    headers = {"Content-Type": "application/json"}

    r = requests.post(SERVE_URL, headers=headers, data=json.dumps(payload), timeout=30)
    print("HTTP", r.status_code)
    print(r.text)

if __name__ == "__main__":
    main()
