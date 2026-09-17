from app.detection.alert_writer import AlertWriter


def main():

    print("=" * 70)
    print("TEST DE L'HISTORIQUE DES ALERTES")
    print("=" * 70)

    writer = AlertWriter()

    test_alert = {
        "pid": 12345,
        "name": "test_process",
        "username": "cytech",
        "cpu_percent": 75.0,
        "memory_mb": 350.0,
        "connections": 8,
        "score": 0.97,
        "consecutive": 3
    }

    writer.save(
        test_alert
    )

    print(
        "\nAlerte de test enregistrée."
    )

    print(
        "CSV : data/alerts/alerts.csv"
    )

    print(
        "JSON : data/alerts/alerts.json"
    )


if __name__ == "__main__":
    main()
