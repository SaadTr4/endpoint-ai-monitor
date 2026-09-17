import joblib
import pandas as pd


MODEL_FILE = "models/gradient_boosting.joblib"


class DetectionEngine:

    def __init__(self):
        package = joblib.load(
            MODEL_FILE
        )

        self.model = package["model"]
        self.features = package["features"]
        self.model_name = package["model_name"]

    def predict(self, process_features, threshold=0.5):
        """
        Analyse un seul processus.
        """

        results = self.predict_many(
            [process_features],
            threshold=threshold
        )

        return results[0]

    def predict_many(
        self,
        processes_features,
        threshold=0.5
    ):
        """
        Analyse plusieurs processus en une seule fois.
        """

        if not processes_features:
            return []

        rows = []

        for process in processes_features:

            row = {}

            for feature in self.features:
                row[feature] = process[feature]

            rows.append(row)

        dataframe = pd.DataFrame(
            rows
        )

        probabilities = self.model.predict_proba(
            dataframe
        )[:, 1]

        results = []

        for score in probabilities:

            score = float(score)

            if score >= threshold:
                label = "Suspicious"
                prediction = 1

            else:
                label = "Normal"
                prediction = 0

            results.append(
                {
                    "label": label,
                    "prediction": prediction,
                    "suspicious_score": round(
                        score,
                        4
                    )
                }
            )

        return results
