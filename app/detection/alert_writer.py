import csv
import json
import os

from datetime import datetime


CSV_FILE = "data/alerts/alerts.csv"
JSON_FILE = "data/alerts/alerts.json"


class AlertWriter:

    def __init__(self):

        os.makedirs(
            "data/alerts",
            exist_ok=True
        )

    def save(self, alert):
        """
        Enregistre une alerte confirmée
        au format CSV et JSON.
        """

        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )

        alert_data = {
            "timestamp": timestamp,
            "pid": alert["pid"],
            "name": alert["name"],
            "username": alert["username"],
            "cpu_percent": alert["cpu_percent"],
            "memory_mb": alert["memory_mb"],
            "connections": alert["connections"],
            "score": alert["score"],
            "consecutive": alert["consecutive"]
        }

        self._save_csv(
            alert_data
        )

        self._save_json(
            alert_data
        )

    def _save_csv(self, alert):

        file_exists = os.path.exists(
            CSV_FILE
        )

        fieldnames = [
            "timestamp",
            "pid",
            "name",
            "username",
            "cpu_percent",
            "memory_mb",
            "connections",
            "score",
            "consecutive"
        ]

        with open(
            CSV_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(
                alert
            )

    def _save_json(self, alert):

        alerts = []

        if os.path.exists(
            JSON_FILE
        ):

            try:

                with open(
                    JSON_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:

                    alerts = json.load(
                        file
                    )

            except (
                json.JSONDecodeError,
                FileNotFoundError
            ):

                alerts = []

        alerts.append(
            alert
        )

        with open(
            JSON_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                alerts,
                file,
                indent=4
            )
