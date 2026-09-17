import threading
import time
from collections import deque
from datetime import datetime

import psutil

from app.monitor.collector import collect_processes
from app.features.runtime_features import RuntimeFeatureBuilder
from app.detection.engine import DetectionEngine
from app.detection.alert_manager import AlertManager
from app.detection.alert_writer import AlertWriter


MONITOR_INTERVAL = 2
DETECTION_THRESHOLD = 0.50
REQUIRED_CONSECUTIVE = 3
ALERT_COOLDOWN = 60

HISTORY_SIZE = 30


class MonitorService:

    def __init__(self):

        self.engine = DetectionEngine()

        self.feature_builder = RuntimeFeatureBuilder()

        self.alert_manager = AlertManager(
            required_consecutive=REQUIRED_CONSECUTIVE,
            cooldown_seconds=ALERT_COOLDOWN
        )

        self.alert_writer = AlertWriter()

        self.lock = threading.Lock()

        self.running = False

        # Historique pour les graphiques
        self.time_history = deque(
            maxlen=HISTORY_SIZE
        )

        self.cpu_history = deque(
            maxlen=HISTORY_SIZE
        )

        self.ram_history = deque(
            maxlen=HISTORY_SIZE
        )

        self.state = {
            "status": "Starting",
            "timestamp": None,

            "total_processes": 0,
            "normal_count": 0,
            "suspicious_count": 0,

            "system_cpu": 0,
            "system_ram": 0,

            "top_suspicious": [],

            "history": {
                "time": [],
                "cpu": [],
                "ram": []
            }
        }

    def start(self):

        if self.running:
            return

        self.running = True

        thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        thread.start()

    def _run(self):

        print(
            "\nBackground monitoring started."
        )

        # Première observation
        first_snapshot = collect_processes()

        self.feature_builder.build(
            first_snapshot
        )

        with self.lock:
            self.state["status"] = "Running"

        while self.running:

            time.sleep(
                MONITOR_INTERVAL
            )

            try:

                # ======================================
                # 1. COLLECTE
                # ======================================

                processes = collect_processes()

                # Ressources globales de la machine
                system_cpu = psutil.cpu_percent(
                    interval=None
                )

                system_ram = psutil.virtual_memory().percent

                # ======================================
                # 2. FEATURES TEMPS REEL
                # ======================================

                runtime_features = (
                    self.feature_builder.build(
                        processes
                    )
                )

                runtime_features = [
                    process
                    for process in runtime_features
                    if process["username"] != "root"
                ]

                if not runtime_features:
                    continue

                # ======================================
                # 3. MACHINE LEARNING
                # ======================================

                predictions = (
                    self.engine.predict_many(
                        runtime_features,
                        threshold=DETECTION_THRESHOLD
                    )
                )

                detections = []

                for process, prediction in zip(
                    runtime_features,
                    predictions
                ):

                    detection = {
                        "pid":
                            process["pid"],

                        "name":
                            process["name"],

                        "username":
                            process["username"],

                        "cpu_percent":
                            process["cpu_percent"],

                        "memory_mb":
                            process["memory_mb"],

                        "connections":
                            process["connections"],

                        "label":
                            prediction["label"],

                        "score":
                            prediction["suspicious_score"]
                    }

                    detections.append(
                        detection
                    )

                # ======================================
                # 4. SUSPICIOUS
                # ======================================

                suspicious = [
                    detection
                    for detection in detections
                    if detection["label"] == "Suspicious"
                ]

                suspicious = sorted(
                    suspicious,
                    key=lambda item: item["score"],
                    reverse=True
                )

                normal_count = (
                    len(detections)
                    - len(suspicious)
                )

                # ======================================
                # 5. ALERTES
                # ======================================

                alerts = self.alert_manager.process(
                    detections
                )

                for alert in alerts:
                    self.alert_writer.save(
                        alert
                    )

                # ======================================
                # 6. HISTORIQUE CPU / RAM
                # ======================================

                now_text = (
                    datetime.now()
                    .strftime("%H:%M:%S")
                )

                self.time_history.append(
                    now_text
                )

                self.cpu_history.append(
                    round(system_cpu, 1)
                )

                self.ram_history.append(
                    round(system_ram, 1)
                )

                # ======================================
                # 7. ETAT POUR FLASK
                # ======================================

                with self.lock:

                    self.state = {
                        "status": "Running",

                        "timestamp":
                            now_text,

                        "total_processes":
                            len(detections),

                        "normal_count":
                            normal_count,

                        "suspicious_count":
                            len(suspicious),

                        "system_cpu":
                            round(system_cpu, 1),

                        "system_ram":
                            round(system_ram, 1),

                        "top_suspicious":
                            suspicious[:10],

                        "history": {
                            "time":
                                list(
                                    self.time_history
                                ),

                            "cpu":
                                list(
                                    self.cpu_history
                                ),

                            "ram":
                                list(
                                    self.ram_history
                                )
                        }
                    }

            except Exception as error:

                print(
                    f"Monitoring error: {error}"
                )

                with self.lock:
                    self.state["status"] = "Error"

    def get_state(self):

        with self.lock:

            return self.state.copy()
