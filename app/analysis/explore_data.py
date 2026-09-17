import pandas as pd


CSV_FILE = "data/raw/process_monitoring.csv"


def main():
    # Charger le fichier CSV
    df = pd.read_csv(CSV_FILE)

    print("=" * 60)
    print("ANALYSE DES DONNEES DU SYSTEM MONITOR")
    print("=" * 60)

    # Nombre de lignes
    print(f"\nNombre total d'observations : {len(df)}")

    # Colonnes disponibles
    print("\nColonnes disponibles :")
    print(list(df.columns))

    # Transformer le timestamp en date lisible
    df["datetime"] = pd.to_datetime(
        df["timestamp"],
        unit="s"
    )

    print("\nPremières observations :")
    print(
        df[
            [
                "datetime",
                "pid",
                "name",
                "cpu_percent",
                "memory_mb",
                "num_threads",
                "connections"
            ]
        ].head()
    )

    # Vérifier les valeurs manquantes
    print("\nValeurs manquantes :")
    print(df.isnull().sum())

    # Statistiques générales
    print("\nStatistiques principales :")
    print(
        df[
            [
                "cpu_percent",
                "memory_mb",
                "num_threads",
                "connections",
                "process_age_seconds"
            ]
        ].describe()
    )

    # Processus ayant consommé le plus de CPU
    print("\nTop 10 observations CPU :")
    print(
        df[
            [
                "name",
                "pid",
                "cpu_percent",
                "memory_mb"
            ]
        ]
        .sort_values(
            by="cpu_percent",
            ascending=False
        )
        .head(10)
    )

    # Processus ayant utilisé le plus de RAM
    print("\nTop 10 observations RAM :")
    print(
        df[
            [
                "name",
                "pid",
                "memory_mb",
                "cpu_percent"
            ]
        ]
        .sort_values(
            by="memory_mb",
            ascending=False
        )
        .head(10)
    )


if __name__ == "__main__":
    main()
