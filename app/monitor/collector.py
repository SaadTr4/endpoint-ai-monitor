import os
import time
import psutil


def get_connection_count(process):
    try:
        connections = process.net_connections(
            kind="inet"
        )

        return len(connections)

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):
        return 0


def get_username(process):
    try:
        return process.username()

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):
        return "unknown"


def collect_processes():
    processes = []

    monitor_pid = os.getpid()
    timestamp = time.time()

    # Première mesure CPU
    for process in psutil.process_iter():
        try:

            if process.pid == monitor_pid:
                continue

            process.cpu_percent(
                interval=None
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    time.sleep(0.5)

    # Collecte réelle
    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "status",
            "memory_percent",
            "num_threads"
        ]
    ):
        try:

            if process.pid == monitor_pid:
                continue

            info = process.info

            info["timestamp"] = timestamp

            info["username"] = get_username(
                process
            )

            info["cpu_percent"] = (
                process.cpu_percent(
                    interval=None
                )
            )

            memory = process.memory_info()

            info["memory_mb"] = round(
                memory.rss / (1024 * 1024),
                2
            )

            info["connections"] = (
                get_connection_count(
                    process
                )
            )

            info["process_age_seconds"] = round(
                time.time()
                - process.create_time(),
                2
            )

            processes.append(info)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return processes
