from flask import Flask
from prometheus_client import Counter, Histogram, Gauge, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter("ml_requests_total", "Total requests")
ERROR_COUNT = Counter("ml_errors_total", "Total errors")
LATENCY = Histogram("ml_latency_seconds", "Latency")
CPU_USAGE = Gauge("ml_cpu_usage", "CPU usage")
MEMORY_USAGE = Gauge("ml_memory_usage", "Memory usage")

@app.route("/metrics")
def metrics():
    REQUEST_COUNT.inc()
    CPU_USAGE.set(30)
    MEMORY_USAGE.set(512)
    return generate_latest()

if __name__ == "__main__":
    app.run(port=5002)