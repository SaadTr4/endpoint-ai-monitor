import os

import numpy as np
import pandas as pd

from sklearn.model_selection import GroupShuffleSplit


INPUT_FILE = "data/processed/process_features.csv"

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


def create_suspicious_samples(
    normal_df,
    random_seed
):
    """
    Crée des observations synthétiques Suspicious
    à partir d'observations normales.

    Aucun malware réel n'est utilisé.
    """

    rng = np.random.default_rng(
        random_seed
    )

    # Échantillonnage avec remplacement
    suspicious = normal_df.sample(
        n=len(normal_df),
        replace=True,
        random_state=random_seed
    ).copy()

    # IMPORTANT :
    # on recrée des index uniques 0, 1, 2, 3...
    suspicious = suspicious.reset_index(
        drop=True
    )

    suspicious["scenario"] = "unknown"

    # Positions uniques des lignes
    indexes = np.arange(
        len(suspicious)
    )

    rng.shuffle(indexes)

    # Diviser les observations en 5 scénarios
    groups = np.array_split(
        indexes,
        5
    )

    # ==================================================
    # SCENARIO 1 : PIC CPU
    # ==================================================

    idx = groups[0]

    suspicious.loc[
        idx,
        "cpu_percent"
    ] = (
        suspicious.loc[
            idx,
            "cpu_percent"
        ].to_numpy()
        + rng.uniform(
            10,
            60,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "cpu_change_rate"
    ] = (
        suspicious.loc[
            idx,
            "cpu_change_rate"
        ].to_numpy()
        + rng.uniform(
            2,
            20,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "scenario"
    ] = "cpu_spike"

    # ==================================================
    # SCENARIO 2 : CROISSANCE MEMOIRE
    # ==================================================

    idx = groups[1]

    suspicious.loc[
        idx,
        "memory_mb"
    ] = (
        suspicious.loc[
            idx,
            "memory_mb"
        ].to_numpy()
        + rng.uniform(
            30,
            300,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "memory_change_rate"
    ] = (
        suspicious.loc[
            idx,
            "memory_change_rate"
        ].to_numpy()
        + rng.uniform(
            1,
            25,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "scenario"
    ] = "memory_growth"

    # ==================================================
    # SCENARIO 3 : AUGMENTATION DES THREADS
    # ==================================================

    idx = groups[2]

    suspicious.loc[
        idx,
        "num_threads"
    ] = (
        suspicious.loc[
            idx,
            "num_threads"
        ].to_numpy()
        + rng.integers(
            3,
            16,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "threads_change"
    ] = (
        suspicious.loc[
            idx,
            "threads_change"
        ].to_numpy()
        + rng.integers(
            1,
            9,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "scenario"
    ] = "thread_burst"

    # ==================================================
    # SCENARIO 4 : ACTIVITE RESEAU INHABITUELLE
    # ==================================================

    idx = groups[3]

    suspicious.loc[
        idx,
        "connections"
    ] = (
        suspicious.loc[
            idx,
            "connections"
        ].to_numpy()
        + rng.integers(
            2,
            16,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "connections_change_rate"
    ] = (
        suspicious.loc[
            idx,
            "connections_change_rate"
        ].to_numpy()
        + rng.uniform(
            0.5,
            5,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "scenario"
    ] = "network_burst"

    # ==================================================
    # SCENARIO 5 : ANOMALIE MIXTE MODEREE
    # ==================================================

    idx = groups[4]

    suspicious.loc[
        idx,
        "cpu_percent"
    ] = (
        suspicious.loc[
            idx,
            "cpu_percent"
        ].to_numpy()
        + rng.uniform(
            5,
            30,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "memory_mb"
    ] = (
        suspicious.loc[
            idx,
            "memory_mb"
        ].to_numpy()
        + rng.uniform(
            20,
            150,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "num_threads"
    ] = (
        suspicious.loc[
            idx,
            "num_threads"
        ].to_numpy()
        + rng.integers(
            1,
            8,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "cpu_change_rate"
    ] = (
        suspicious.loc[
            idx,
            "cpu_change_rate"
        ].to_numpy()
        + rng.uniform(
            1,
            10,
            len(idx)
        )
    )

    suspicious.loc[
        idx,
        "scenario"
    ] = "mixed"

    # ==================================================
    # LABEL
    # ==================================================

    suspicious["label"] = 1
    suspicious["label_name"] = "Suspicious"

    return suspicious


def prepare_split(
    df,
    random_seed
):
    """
    Construit un dataset équilibré :
    Normal + Suspicious synthétique.
    """

    normal = df[
        FEATURES
    ].copy()

    normal = normal.reset_index(
        drop=True
    )

    normal["label"] = 0
    normal["label_name"] = "Normal"
    normal["scenario"] = "normal"

    suspicious = create_suspicious_samples(
        normal[FEATURES],
        random_seed
    )

    result = pd.concat(
        [
            normal,
            suspicious
        ],
        ignore_index=True
    )

    # Mélanger les lignes
    result = result.sample(
        frac=1,
        random_state=random_seed
    ).reset_index(
        drop=True
    )

    return result


def main():

    print("=" * 70)
    print("CONSTRUCTION DU DATASET MACHINE LEARNING V2")
    print("=" * 70)

    # ==================================================
    # 1. CHARGEMENT
    # ==================================================

    df = pd.read_csv(
        INPUT_FILE
    )

    # Pour cette première version ML,
    # on évite les nombreux processus root inactifs.
    df = df[
        df["username"] != "root"
    ].copy()

    print(
        f"\nObservations disponibles : "
        f"{len(df)}"
    )

    # ==================================================
    # 2. SEPARATION TRAIN / TEST PAR PID
    # ==================================================
    #
    # Un PID présent dans l'entraînement
    # ne doit pas apparaître dans le test.
    #

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.20,
        random_state=RANDOM_SEED
    )

    train_index, test_index = next(
        splitter.split(
            df,
            groups=df["pid"]
        )
    )

    base_train = df.iloc[
        train_index
    ].copy()

    base_test = df.iloc[
        test_index
    ].copy()

    print(
        f"Observations normales TRAIN : "
        f"{len(base_train)}"
    )

    print(
        f"Observations normales TEST : "
        f"{len(base_test)}"
    )

    # ==================================================
    # 3. CREATION DES DATASETS
    # ==================================================

    train_df = prepare_split(
        base_train,
        RANDOM_SEED
    )

    test_df = prepare_split(
        base_test,
        RANDOM_SEED + 1
    )

    # ==================================================
    # 4. SAUVEGARDE
    # ==================================================

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    train_df.to_csv(
        TRAIN_FILE,
        index=False
    )

    test_df.to_csv(
        TEST_FILE,
        index=False
    )

    # ==================================================
    # 5. RESULTATS
    # ==================================================

    print(
        f"\nTrain : "
        f"{len(train_df)} lignes"
    )

    print(
        f"Test  : "
        f"{len(test_df)} lignes"
    )

    print("\nClasses TRAIN :")

    print(
        train_df[
            "label_name"
        ]
        .value_counts()
        .to_string()
    )

    print("\nClasses TEST :")

    print(
        test_df[
            "label_name"
        ]
        .value_counts()
        .to_string()
    )

    print(
        "\nScénarios synthétiques TRAIN :"
    )

    print(
        train_df[
            "scenario"
        ]
        .value_counts()
        .to_string()
    )

    print(
        "\nScénarios synthétiques TEST :"
    )

    print(
        test_df[
            "scenario"
        ]
        .value_counts()
        .to_string()
    )

    print(
        "\nFichiers créés :"
    )

    print(
        f"- {TRAIN_FILE}"
    )

    print(
        f"- {TEST_FILE}"
    )

    print(
        "\nDataset V2 terminé."
    )


if __name__ == "__main__":
    main()
