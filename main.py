import time

from app.monitor.collector import collect_processes
from app.storage.writer import save_processes_to_csv


def main():

    print("=" * 60)
    print("AI-Powered Endpoint Monitor")
    print("=" * 60)

    print(
        "\nMonitoring démarré."
        "\nCtrl + C pour arrêter.\n"
    )

    try:

        while True:

            processes = collect_processes()

            save_processes_to_csv(
                processes
            )

            print(
                f"Collecte terminée : "
                f"{len(processes)} processus"
            )

            time.sleep(2)

    except KeyboardInterrupt:

        print(
            "\nMonitoring arrêté."
        )


if __name__ == "__main__":
    main()
