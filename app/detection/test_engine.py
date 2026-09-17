import pandas as pd

from app.detection.engine import DetectionEngine


TEST_FILE = "data/processed/ml_test.csv"


FEATURES = [
    "cpu_percent",
    "memory_mb",
    "num_threads",
    "connections",
    "process_age_seconds",
    "cpu_change_rate",
    "memory_change_rate",
    "threads_change",
    "connections_change_rate"
]


def main():

    print("=" * 70)
    print("TEST DU DETECTION ENGINE")
    print("=" * 70)

    df = pd.read_csv(
        TEST_FILE
    )

    engine = DetectionEngine()

    print(
        f"\nModèle chargé : "
        f"{engine.model_name}"
    )

    # --------------------------------------------------
    # Récupérer un exemple Normal
    # --------------------------------------------------

    normal_row = df[
        df["label_name"] == "Normal"
    ].iloc[0]

    normal_features = (
        normal_row[FEATURES]
        .to_dict()
    )

    normal_result = engine.predict(
        normal_features
    )

    print("\n--- Exemple NORMAL ---")

    print(
        f"Classe réelle : "
        f"{normal_row['label_name']}"
    )

    print(
        f"Prédiction : "
        f"{normal_result['label']}"
    )

    print(
        f"Score Suspicious : "
        f"{normal_result['suspicious_score']}"
    )

    # --------------------------------------------------
    # Récupérer un exemple Suspicious
    # --------------------------------------------------

    suspicious_row = df[
        df["label_name"] == "Suspicious"
    ].iloc[0]

    suspicious_features = (
        suspicious_row[FEATURES]
        .to_dict()
    )

    suspicious_result = engine.predict(
        suspicious_features
    )

    print("\n--- Exemple SUSPICIOUS ---")

    print(
        f"Scénario : "
        f"{suspicious_row['scenario']}"
    )

    print(
        f"Classe réelle : "
        f"{suspicious_row['label_name']}"
    )

    print(
        f"Prédiction : "
        f"{suspicious_result['label']}"
    )

    print(
        f"Score Suspicious : "
        f"{suspicious_result['suspicious_score']}"
    )


if __name__ == "__main__":
    main()
