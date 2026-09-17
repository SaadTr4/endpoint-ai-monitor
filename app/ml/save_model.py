import joblib
import pandas as pd

from sklearn.ensemble import GradientBoostingClassifier


TRAIN_FILE = "data/processed/ml_train.csv"
MODEL_FILE = "models/gradient_boosting.joblib"

RANDOM_SEED = 42


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
    print("ENTRAINEMENT ET SAUVEGARDE DU MODELE")
    print("=" * 70)

    # Charger le dataset d'entraînement
    train_df = pd.read_csv(
        TRAIN_FILE
    )

    x_train = train_df[
        FEATURES
    ]

    y_train = train_df[
        "label"
    ]

    print(
        f"\nObservations d'entraînement : "
        f"{len(train_df)}"
    )

    # Créer le modèle
    model = GradientBoostingClassifier(
        random_state=RANDOM_SEED
    )

    # Entraîner
    print("\nEntraînement du modèle...")

    model.fit(
        x_train,
        y_train
    )

    # On sauvegarde le modèle ET la liste
    # exacte des features utilisées.
    model_package = {
        "model": model,
        "features": FEATURES,
        "model_name": "GradientBoostingClassifier"
    }

    joblib.dump(
        model_package,
        MODEL_FILE
    )

    print(
        f"\nModèle sauvegardé : "
        f"{MODEL_FILE}"
    )

    print("\nFeatures attendues :")

    for feature in FEATURES:
        print(
            f"- {feature}"
        )

    print("\nSauvegarde terminée.")


if __name__ == "__main__":
    main()
