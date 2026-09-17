import os
import pandas as pd


INPUT_FILE = "data/raw/process_monitoring.csv"
OUTPUT_FILE = "data/processed/process_features.csv"


def build_features():
    df = pd.read_csv(INPUT_FILE)

    print("=" * 60)
    print("FEATURE ENGINEERING V2")
    print("=" * 60)

    print(f"\nObservations brutes : {len(df)}")

    # Trier les observations par processus et par temps
    df = df.sort_values(
        by=["pid", "name", "timestamp"]
    )

    # Regrouper les observations appartenant
    # au même processus
    groups = df.groupby(
        ["pid", "name"]
    )

    # --------------------------------------------------
    # 1. Temps écoulé entre deux observations
    # --------------------------------------------------

    df["time_delta"] = (
        groups["timestamp"]
        .diff()
    )

    # --------------------------------------------------
    # 2. Changements absolus
    # --------------------------------------------------

    df["cpu_change"] = (
        groups["cpu_percent"]
        .diff()
    )

    df["memory_change_mb"] = (
        groups["memory_mb"]
        .diff()
    )

    df["threads_change"] = (
        groups["num_threads"]
        .diff()
    )

    df["connections_change"] = (
        groups["connections"]
        .diff()
    )

    # --------------------------------------------------
    # 3. Taux de changement
    # --------------------------------------------------

    df["cpu_change_rate"] = (
        df["cpu_change"]
        / df["time_delta"]
    )

    df["memory_change_rate"] = (
        df["memory_change_mb"]
        / df["time_delta"]
    )

    df["connections_change_rate"] = (
        df["connections_change"]
        / df["time_delta"]
    )

    # --------------------------------------------------
    # 4. Première observation de chaque processus
    # --------------------------------------------------
    #
    # Elle n'a pas d'observation précédente.
    # Les différences sont donc inconnues.
    # Pour notre première version, on les met à 0.
    #

    temporal_features = [
        "time_delta",
        "cpu_change",
        "memory_change_mb",
        "threads_change",
        "connections_change",
        "cpu_change_rate",
        "memory_change_rate",
        "connections_change_rate"
    ]

    df[temporal_features] = (
        df[temporal_features]
        .fillna(0)
    )

    # Arrondir les valeurs
    df[
        [
            "time_delta",
            "cpu_change",
            "memory_change_mb",
            "cpu_change_rate",
            "memory_change_rate",
            "connections_change_rate"
        ]
    ] = (
        df[
            [
                "time_delta",
                "cpu_change",
                "memory_change_mb",
                "cpu_change_rate",
                "memory_change_rate",
                "connections_change_rate"
            ]
        ]
        .round(3)
    )

    # --------------------------------------------------
    # 5. Sauvegarde
    # --------------------------------------------------

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nDataset créé : {OUTPUT_FILE}"
    )

    print(
        f"Nombre d'observations : {len(df)}"
    )

    print("\nFeatures comportementales :")

    for feature in temporal_features:
        print(f"- {feature}")

    # --------------------------------------------------
    # 6. Montrer les changements CPU les plus importants
    # --------------------------------------------------

    columns = [
        "pid",
        "name",
        "cpu_percent",
        "cpu_change",
        "time_delta",
        "cpu_change_rate",
        "memory_mb",
        "memory_change_mb",
        "memory_change_rate",
        "num_threads",
        "threads_change",
        "connections",
        "connections_change"
    ]

    print("\nTop variations CPU :\n")

    print(
        df[columns]
        .sort_values(
            by="cpu_change_rate",
            ascending=False
        )
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    build_features()
