"""
ScalePilot AI - Predictive Auto-Scaling of Cloud Applications Using Machine Learning
Mini-project demo: Flask + scikit-learn (Linear Regression) + SQLite + Chart.js
"""
import sqlite3
from datetime import datetime

from flask import Flask, request, render_template
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
DB_NAME = "scalepilot.db"

# Sample historical workload data: (CPU usage %, request rate requests/minute).
# This tiny dataset makes the demo easy to understand.
HISTORICAL_DATA = [
    (20, 100), (25, 130), (30, 160), (35, 190),
    (40, 220), (45, 250), (50, 280), (55, 310),
    (60, 340), (65, 370), (70, 400), (75, 430),
]


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                cpu REAL NOT NULL,
                memory REAL NOT NULL,
                requests INTEGER NOT NULL,
                predicted_cpu REAL NOT NULL,
                instances INTEGER NOT NULL,
                action TEXT NOT NULL
            )
        """)


def train_model():
    # Use past CPU and request-rate observations to learn a simple relationship.
    X = [[req] for cpu, req in HISTORICAL_DATA]
    y = [cpu for cpu, req in HISTORICAL_DATA]
    model = LinearRegression()
    model.fit(X, y)
    return model


model = train_model()
init_db()


def get_history():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("""
            SELECT substr(created_at, 12, 8), round(cpu,1), round(predicted_cpu,1), instances
            FROM predictions ORDER BY id DESC LIMIT 5
        """).fetchall()


def decide_scaling(predicted_cpu, memory):
    """Simple, understandable scaling policy for demonstration."""
    if predicted_cpu > 70 or memory > 80:
        return 3, "Scale up: add 1 instance"
    if predicted_cpu < 30 and memory < 40:
        return 1, "Scale down: remove 1 instance"
    return 2, "No change needed"


@app.route("/", methods=["GET", "POST"])
def index():
    cpu, memory, requests = 45.0, 50.0, 250

    if request.method == "POST":
        try:
            cpu = float(request.form.get("cpu", 45))
            memory = float(request.form.get("memory", 50))
            requests = int(request.form.get("requests", 250))
            if not (0 <= cpu <= 100 and 0 <= memory <= 100 and requests >= 0):
                raise ValueError("Values out of range")
        except (ValueError, TypeError):
            return ("Please enter CPU and memory from 0 to 100, "
                    "and a non-negative request count."), 400

    # Estimate CPU from request rate; include current CPU as a stabilizing factor.
    request_prediction = float(model.predict([[requests]])[0])
    predicted_cpu = max(0, min(100, 0.7 * request_prediction + 0.3 * cpu))

    instances, action = decide_scaling(predicted_cpu, memory)

    if request.method == "POST":
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                INSERT INTO predictions
                (created_at, cpu, memory, requests, predicted_cpu, instances, action)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (datetime.now().isoformat(timespec="seconds"),
                  cpu, memory, requests, predicted_cpu, instances, action))

    history = get_history()
    chart_labels = [str(req) for cpu_v, req in HISTORICAL_DATA]
    chart_values = [cpu_v for cpu_v, req in HISTORICAL_DATA]

    return render_template(
        "index.html",
        cpu=cpu, memory=memory, requests=requests,
        predicted_cpu=round(predicted_cpu, 1), instances=instances, action=action,
        history=history, chart_labels=chart_labels, chart_values=chart_values,
    )


if __name__ == "__main__":
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True)
