import time
import json
import requests
from prometheus_client import start_http_server, Counter, Histogram, Gauge

MODEL_URL = "http://localhost:5001/invocations"
EXPORTER_PORT = 8000
SCRAPE_INTERVAL_SEC = 2

REQUESTS_TOTAL = Counter("ml_requests_total", "Total requests to model")
REQUEST_ERRORS_TOTAL = Counter("ml_request_errors_total", "Total failed requests to model")
REQUEST_LATENCY = Histogram("ml_request_latency_seconds", "Latency seconds for model request")

MODEL_UP = Gauge("ml_model_up", "1 if model endpoint reachable, else 0")
LAST_PREDICTION = Gauge("ml_last_prediction", "Last prediction value (numeric)")
LAST_STATUS_CODE = Gauge("ml_last_status_code", "Last HTTP status code")

SAMPLE_PAYLOAD = {
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

def ping_model():
    try:
        with REQUEST_LATENCY.time():
            r = requests.post(
                MODEL_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(SAMPLE_PAYLOAD),
                timeout=5,
            )
        LAST_STATUS_CODE.set(r.status_code)
        REQUESTS_TOTAL.inc()

        if r.status_code != 200:
            MODEL_UP.set(0)
            REQUEST_ERRORS_TOTAL.inc()
            return

        MODEL_UP.set(1)

        js = r.json()
        preds = js.get("predictions", [])
        if isinstance(preds, list) and len(preds) > 0:
            try:
                LAST_PREDICTION.set(float(preds[0]))
            except Exception:
                pass

    except Exception:
        MODEL_UP.set(0)
        REQUEST_ERRORS_TOTAL.inc()

def main():
    start_http_server(EXPORTER_PORT)
    print(f"Exporter running: http://localhost:{EXPORTER_PORT}/metrics")
    while True:
        ping_model()
        time.sleep(SCRAPE_INTERVAL_SEC)

if __name__ == "__main__":
    main()