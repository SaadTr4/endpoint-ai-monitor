import csv
import os


CSV_FILE = "data/raw/process_monitoring.csv"


def save_processes_to_csv(processes):
    os.makedirs(
        os.path.dirname(CSV_FILE),
        exist_ok=True
    )

    file_exists = os.path.exists(
        CSV_FILE
    )

    fieldnames = [
        "timestamp",
        "pid",
        "name",
        "username",
        "status",
        "cpu_percent",
        "memory_percent",
        "memory_mb",
        "num_threads",
        "connections",
        "process_age_seconds"
    ]

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        for process in processes:
            writer.writerow(process)
