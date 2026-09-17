import pandas as pd


INPUT_FILE = "data/processed/process_features.csv"


FEATURES = [
    "cpu_percent",
    "memory_percent",
    "memory_mb",
    "num_threads",
    "connections",
    "process_age_seconds",
    "cpu_change",
    "memory_change_mb",
    "threads_change",
    "connections_change",
    "cpu_change_rate",
    "memory_change_rate",
    "connections_change_rate"
]


def main():
    df = pd.read_csv(INPUT_FILE)

    print("=" * 70)
    print("ANALYSE DES FEATURES")
    print("=" * 70)

    print(f"\nNombre d'observations : {len(df)}")

    # --------------------------------------------------
    # 1. Statistiques générales
    # --------------------------------------------------

    print("\n1. STATISTIQUES GENERALES\n")

    print(
        df[FEATURES]
        .describe()
        .round(3)
        .to_string()
    )

    # --------------------------------------------------
    # 2. Pourcentage de valeurs égales à zéro
    # --------------------------------------------------

    print("\n2. POURCENTAGE DE VALEURS A ZERO\n")

    zero_percentages = (
        (df[FEATURES] == 0)
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
    )

    for feature, percentage in zero_percentages.items():
        print(
            f"{feature:<28} "
            f"{percentage:>6.2f} %"
        )

    # --------------------------------------------------
    # 3. Variance
    # --------------------------------------------------

    print("\n3. VARIANCE DES FEATURES\n")

    variances = (
        df[FEATURES]
        .var()
        .round(3)
        .sort_values(ascending=False)
    )

    for feature, variance in variances.items():
        print(
            f"{feature:<28} "
            f"{variance}"
        )

    # --------------------------------------------------
    # 4. Corrélations
    # --------------------------------------------------

    print("\n4. CORRELATIONS ENTRE FEATURES\n")

    correlation = (
        df[FEATURES]
        .corr()
        .round(2)
    )

    print(
        correlation.to_string()
    )

    # --------------------------------------------------
    # 5. Features presque toujours nulles
    # --------------------------------------------------

    print("\n5. FEATURES A SURVEILLER\n")

    weak_features = []

    for feature in FEATURES:

        zero_ratio = (
            (df[feature] == 0).mean()
        )

        if zero_ratio >= 0.95:
            weak_features.append(
                (
                    feature,
                    round(
                        zero_ratio * 100,
                        2
                    )
                )
            )

    if weak_features:

        print(
            "Features ayant au moins "
            "95% de valeurs égales à 0 :\n"
        )

        for feature, percentage in weak_features:
            print(
                f"- {feature}: "
                f"{percentage}% de zéros"
            )

    else:

        print(
            "Aucune feature ne dépasse "
            "95% de valeurs nulles."
        )


if __name__ == "__main__":
    main()
