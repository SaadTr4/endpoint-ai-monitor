import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
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


def evaluate_by_scenario(
    model_name,
    model,
    x_train,
    y_train,
    test_df
):
    print("\n" + "=" * 70)
    print(model_name)
    print("=" * 70)

    model.fit(
        x_train,
        y_train
    )

    x_test = test_df[
        FEATURES
    ]

    predictions = model.predict(
        x_test
    )

    results = test_df.copy()

    results["prediction"] = predictions

    # --------------------------------------------------
    # Faux positifs sur les données normales
    # --------------------------------------------------

    normal = results[
        results["scenario"] == "normal"
    ]

    false_positives = (
        normal["prediction"] == 1
    ).sum()

    print(
        f"\nNormal : {len(normal)} observations"
    )

    print(
        f"Faux positifs : {false_positives}"
    )

    false_positive_rate = (
        false_positives
        / len(normal)
        * 100
    )

    print(
        f"Taux de faux positifs : "
        f"{false_positive_rate:.2f}%"
    )

    # --------------------------------------------------
    # Détection par scénario Suspicious
    # --------------------------------------------------

    print("\nDétection des scénarios :\n")

    scenarios = [
        "cpu_spike",
        "memory_growth",
        "thread_burst",
        "network_burst",
        "mixed"
    ]

    for scenario in scenarios:

        scenario_df = results[
            results["scenario"] == scenario
        ]

        total = len(
            scenario_df
        )

        detected = (
            scenario_df["prediction"] == 1
        ).sum()

        missed = total - detected

        detection_rate = (
            detected
            / total
            * 100
        )

        print(
            f"{scenario:<20} "
            f"Détectés={detected:<4} "
            f"Ratés={missed:<4} "
            f"Recall={detection_rate:.2f}%"
        )


def main():

    print("=" * 70)
    print("EVALUATION PAR SCENARIO")
    print("=" * 70)

    train_df = pd.read_csv(
        TRAIN_FILE
    )

    test_df = pd.read_csv(
        TEST_FILE
    )

    x_train = train_df[
        FEATURES
    ]

    y_train = train_df[
        "label"
    ]

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

    evaluate_by_scenario(
        "LOGISTIC REGRESSION",
        logistic_regression,
        x_train,
        y_train,
        test_df
    )

    evaluate_by_scenario(
        "RANDOM FOREST",
        random_forest,
        x_train,
        y_train,
        test_df
    )

    evaluate_by_scenario(
        "GRADIENT BOOSTING",
        gradient_boosting,
        x_train,
        y_train,
        test_df
    )


if __name__ == "__main__":
    main()
