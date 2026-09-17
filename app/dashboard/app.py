import json
import os

from flask import (
    Flask,
    jsonify,
    render_template
)

from app.dashboard.runtime_service import (
    MonitorService
)


app = Flask(__name__)

ALERT_FILE = "data/alerts/alerts.json"


# ==============================================
# Service de monitoring
# ==============================================

monitor_service = MonitorService()

monitor_service.start()


def load_alerts():

    if not os.path.exists(
        ALERT_FILE
    ):
        return []

    try:

        with open(
            ALERT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except json.JSONDecodeError:

        return []


# ==============================================
# Dashboard
# ==============================================

@app.route("/")
def dashboard():

    alerts = load_alerts()

    alerts = list(
        reversed(alerts)
    )

    return render_template(
        "index.html",
        model_name="Gradient Boosting",
        alert_count=len(alerts),
        alerts=alerts[:10]
    )


# ==============================================
# API temps réel
# ==============================================

@app.route("/api/status")
def api_status():

    state = (
        monitor_service.get_state()
    )

    return jsonify(
        state
    )


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
