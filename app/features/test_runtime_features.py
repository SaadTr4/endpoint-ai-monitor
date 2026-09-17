import time

from app.monitor.collector import collect_processes
from app.features.runtime_features import RuntimeFeatureBuilder


def main():

    print("=" * 70)
    print("TEST DES FEATURES TEMPS REEL")
    print("=" * 70)

    builder = RuntimeFeatureBuilder()

    print("\nPremière collecte...")

    processes = collect_processes()

    builder.build(
        processes
    )

    print(
        "Première observation mémorisée."
    )

    print(
        "\nAttente avant la deuxième collecte..."
    )

    time.sleep(2)

    processes = collect_processes()

    features = builder.build(
        processes
    )

    # Trier selon les plus grosses variations CPU
    features = sorted(
        features,
        key=lambda process:
        process["cpu_change_rate"],
        reverse=True
    )

    print(
        "\nTop variations CPU temps réel :\n"
    )

    for process in features[:10]:

        print(
            f"PID={process['pid']} | "
            f"Nom={process['name']} | "
            f"CPU={process['cpu_percent']}% | "
            f"CPU_RATE={process['cpu_change_rate']} | "
            f"RAM={process['memory_mb']} MB | "
            f"RAM_RATE={process['memory_change_rate']} | "
            f"Threads={process['num_threads']} | "
            f"Threads_CHANGE={process['threads_change']} | "
            f"Connexions={process['connections']} | "
            f"NET_RATE={process['connections_change_rate']}"
        )


if __name__ == "__main__":
    main()
