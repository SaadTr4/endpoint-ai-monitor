import pandas as pd


INPUT_FILE = "data/processed/process_features.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    print("=" * 70)
    print("COMPARAISON PROCESSUS SYSTEME / UTILISATEUR")
    print("=" * 70)

    print(f"\nNombre total d'observations : {len(df)}")

    # --------------------------------------------------
    # 1. Nombre d'observations par utilisateur
    # --------------------------------------------------

    print("\n1. OBSERVATIONS PAR UTILISATEUR\n")

    user_counts = (
        df["username"]
        .value_counts()
    )

    print(user_counts.to_string())

    # --------------------------------------------------
    # 2. Créer deux catégories simples
    # --------------------------------------------------

    df["process_type"] = df["username"].apply(
        lambda username:
        "system" if username == "root"
        else "user"
    )

    # --------------------------------------------------
    # 3. Moyennes par catégorie
    # --------------------------------------------------

    print("\n2. MOYENNES PAR TYPE DE PROCESSUS\n")

    summary = (
        df.groupby("process_type")
        [
            [
                "cpu_percent",
                "memory_mb",
                "num_threads",
                "connections",
                "cpu_change_rate",
                "memory_change_rate"
            ]
        ]
        .mean()
        .round(3)
    )

    print(summary.to_string())

    # --------------------------------------------------
    # 4. Maximums
    # --------------------------------------------------

    print("\n3. VALEURS MAXIMALES\n")

    maximums = (
        df.groupby("process_type")
        [
            [
                "cpu_percent",
                "memory_mb",
                "num_threads",
                "connections",
                "cpu_change_rate",
                "memory_change_rate"
            ]
        ]
        .max()
        .round(3)
    )

    print(maximums.to_string())

    # --------------------------------------------------
    # 5. Pourcentage de CPU = 0
    # --------------------------------------------------

    print("\n4. POURCENTAGE DE CPU A ZERO\n")

    cpu_zero = (
        df.groupby("process_type")["cpu_percent"]
        .apply(
            lambda column:
            (column == 0).mean() * 100
        )
        .round(2)
    )

    print(cpu_zero.to_string())

    # --------------------------------------------------
    # 6. Pourcentage de connexions = 0
    # --------------------------------------------------

    print("\n5. POURCENTAGE DE CONNEXIONS A ZERO\n")

    connection_zero = (
        df.groupby("process_type")["connections"]
        .apply(
            lambda column:
            (column == 0).mean() * 100
        )
        .round(2)
    )

    print(connection_zero.to_string())


if __name__ == "__main__":
    main()
