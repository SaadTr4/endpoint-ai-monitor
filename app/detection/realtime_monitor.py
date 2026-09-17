import time
from datetime import datetime

from app.monitor.collector import collect_processes

from app.features.runtime_features import (
    RuntimeFeatureBuilder
)

from app.detection.engine import (
    DetectionEngine
)

from app.detection.alert_manager import (
    AlertManager
)

from app.detection.alert_writer import (
    AlertWriter
)


MONITOR_INTERVAL = 2

DETECTION_THRESHOLD = 0.50

REQUIRED_CONSECUTIVE = 3

ALERT_COOLDOWN = 60


def main():

    print("=" * 75)
    print("AI-POWERED ENDPOINT MONITOR")
    print("=" * 75)

    # ==================================================
    # COMPOSANTS
    # ==================================================

    engine = DetectionEngine()

    feature_builder = (
        RuntimeFeatureBuilder()
    )

    alert_manager = AlertManager(
        required_consecutive=REQUIRED_CONSECUTIVE,
        cooldown_seconds=ALERT_COOLDOWN
    )

    alert_writer = AlertWriter()

    print(
        f"\nModèle chargé : "
        f"{engine.model_name}"
    )

    print(
        f"Seuil ML : "
        f"{DETECTION_THRESHOLD}"
    )

    print(
        f"Confirmation alerte : "
        f"{REQUIRED_CONSECUTIVE} "
        f"détections consécutives"
    )

    print(
        f"Cooldown : "
        f"{ALERT_COOLDOWN} secondes"
    )

    # ==================================================
    # PREMIERE OBSERVATION
    # ==================================================

    print(
        "\nInitialisation..."
    )

    first_snapshot = (
        collect_processes()
    )

    feature_builder.build(
        first_snapshot
    )

    print(
        "Première observation mémorisée."
    )

    print(
        "\nMonitoring démarré."
    )

    print(
        "Ctrl + C pour arrêter.\n"
    )

    try:

        while True:

            time.sleep(
                MONITOR_INTERVAL
            )

            # ==========================================
            # 1. COLLECTE
            # ==========================================

            processes = (
                collect_processes()
            )

            # ==========================================
            # 2. FEATURE ENGINEERING TEMPS REEL
            # ==========================================

            runtime_features = (
                feature_builder.build(
                    processes
                )
            )

            # Le modèle a été entraîné
            # uniquement sur des processus non-root
            runtime_features = [
                process
                for process in runtime_features
                if process["username"] != "root"
            ]

            if not runtime_features:
                continue

            # ==========================================
            # 3. MACHINE LEARNING
            # ==========================================

            predictions = (
                engine.predict_many(
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
                        prediction[
                            "suspicious_score"
                        ]
                }

                detections.append(
                    detection
                )

            # ==========================================
            # 4. STATISTIQUES
            # ==========================================

            suspicious = [
                detection
                for detection in detections
                if detection["label"]
                == "Suspicious"
            ]

            normal_count = (
                len(detections)
                - len(suspicious)
            )

            now_text = (
                datetime.now()
                .strftime("%H:%M:%S")
            )

            print(
                "\n"
                + "=" * 75
            )

            print(
                f"[{now_text}] "
                f"Processus analysés : "
                f"{len(detections)}"
            )

            print(
                f"Normal : {normal_count} | "
                f"Suspicious temporaire : "
                f"{len(suspicious)}"
            )

            # ==========================================
            # 5. OBSERVATIONS TEMPORAIRES
            # ==========================================

            if suspicious:

                suspicious = sorted(
                    suspicious,
                    key=lambda item:
                    item["score"],
                    reverse=True
                )

                print(
                    "\nObservations Suspicious :"
                )

                for detection in suspicious[:10]:

                    print(
                        f"PID={detection['pid']} | "
                        f"Nom={detection['name']} | "
                        f"CPU="
                        f"{detection['cpu_percent']}% | "
                        f"RAM="
                        f"{detection['memory_mb']} MB | "
                        f"Score="
                        f"{detection['score']}"
                    )

            else:

                print(
                    "\nAucune anomalie temporaire."
                )

            # ==========================================
            # 6. CONFIRMATION DES ALERTES
            # ==========================================

            alerts = (
                alert_manager.process(
                    detections
                )
            )

            # ==========================================
            # 7. ENREGISTREMENT DES ALERTES
            # ==========================================

            if alerts:

                print(
                    "\n"
                    + "!" * 75
                )

                print(
                    "ALERTE(S) CONFIRMEE(S)"
                )

                print(
                    "!" * 75
                )

                for alert in alerts:

                    print(
                        f"PID={alert['pid']} | "
                        f"Nom={alert['name']} | "
                        f"Score={alert['score']} | "
                        f"Détections consécutives="
                        f"{alert['consecutive']}"
                    )

                    # Sauvegarde CSV + JSON
                    alert_writer.save(
                        alert
                    )

                    print(
                        "→ Alerte enregistrée "
                        "dans l'historique."
                    )

    except KeyboardInterrupt:

        print(
            "\n\nMonitoring arrêté."
        )


if __name__ == "__main__":
    main()
