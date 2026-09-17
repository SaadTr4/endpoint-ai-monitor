import time


class AlertManager:

    def __init__(
        self,
        required_consecutive=3,
        cooldown_seconds=60
    ):
        self.required_consecutive = (
            required_consecutive
        )

        self.cooldown_seconds = (
            cooldown_seconds
        )

        self.states = {}

    def process(self, detections):
        """
        Analyse les résultats d'un cycle et retourne
        uniquement les alertes confirmées.
        """

        confirmed_alerts = []

        current_keys = set()

        for detection in detections:

            key = (
                detection["pid"],
                detection["name"]
            )

            current_keys.add(key)

            if key not in self.states:

                self.states[key] = {
                    "consecutive": 0,
                    "last_alert": 0
                }

            state = self.states[key]

            # ------------------------------------------
            # Processus actuellement Suspicious
            # ------------------------------------------

            if detection["label"] == "Suspicious":

                state["consecutive"] += 1

                # Vérifier si l'anomalie persiste
                if (
                    state["consecutive"]
                    >= self.required_consecutive
                ):

                    now = time.time()

                    # Anti-spam :
                    # ne pas répéter l'alerte trop vite
                    if (
                        now
                        - state["last_alert"]
                        >= self.cooldown_seconds
                    ):

                        alert = detection.copy()

                        alert["consecutive"] = (
                            state["consecutive"]
                        )

                        confirmed_alerts.append(
                            alert
                        )

                        state["last_alert"] = now

            # ------------------------------------------
            # Retour à Normal
            # ------------------------------------------

            else:

                state["consecutive"] = 0

        # ----------------------------------------------
        # Supprimer les processus disparus
        # ----------------------------------------------

        old_keys = list(
            self.states.keys()
        )

        for key in old_keys:

            if key not in current_keys:

                del self.states[key]

        return confirmed_alerts
