import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


TRAIN_FILE = "data/processed/ml_train.csv"
TEST_FILE = "data/processed/ml_test.csv"

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


def evaluate_model(
    name,
    model,
    x_train,
    y_train,
    x_test,
    y_test
):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    # Entraînement
    model.fit(
        x_train,
        y_train
    )

    # Prédictions
    predictions = model.predict(
        x_test
    )

    # Métriques
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions
    )

    recall = recall_score(
        y_test,
        predictions
    )

    f1 = f1_score(
        y_test,
        predictions
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    print(
        f"\nAccuracy  : {accuracy:.4f}"
    )

    print(
        f"Precision : {precision:.4f}"
    )

    print(
        f"Recall    : {recall:.4f}"
    )

    print(
        f"F1-score  : {f1:.4f}"
    )

    print("\nMatrice de confusion :")
    print(matrix)

    return {
        "name": name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


def main():
    print("=" * 70)
    print("ENTRAINEMENT DES MODELES - DATASET V2")
    print("=" * 70)

    # --------------------------------------------------
    # Charger train et test séparément
    # --------------------------------------------------

    train_df = pd.read_csv(
        TRAIN_FILE
    )

    test_df = pd.read_csv(
        TEST_FILE
    )

    print(
        f"\nTrain : {len(train_df)} observations"
    )

    print(
        f"Test  : {len(test_df)} observations"
    )

    # --------------------------------------------------
    # Features / labels
    # --------------------------------------------------

    x_train = train_df[
        FEATURES
    ]

    y_train = train_df[
        "label"
    ]

    x_test = test_df[
        FEATURES
    ]

    y_test = test_df[
        "label"
    ]

    # --------------------------------------------------
    # Modèles
    # --------------------------------------------------

    logistic_regression = Pipeline(
        [
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    random_state=RANDOM_SEED
                )
            )
        ]
    )

    random_forest = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_SEED,
        n_jobs=-1
    )

    gradient_boosting = GradientBoostingClassifier(
        random_state=RANDOM_SEED
    )

    # --------------------------------------------------
    # Entraînement + évaluation
    # --------------------------------------------------

    results = []

    results.append(
        evaluate_model(
            "LOGISTIC REGRESSION",
            logistic_regression,
            x_train,
            y_train,
            x_test,
            y_test
        )
    )

    results.append(
        evaluate_model(
            "RANDOM FOREST",
            random_forest,
            x_train,
            y_train,
            x_test,
            y_test
        )
    )

    results.append(
        evaluate_model(
            "GRADIENT BOOSTING",
            gradient_boosting,
            x_train,
            y_train,
            x_test,
            y_test
        )
    )

    # --------------------------------------------------
    # Résumé
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("RESUME")
    print("=" * 70)

    results_df = pd.DataFrame(
        results
    )

    print(
        results_df
        .round(4)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
