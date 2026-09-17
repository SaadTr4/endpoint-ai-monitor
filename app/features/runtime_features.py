class RuntimeFeatureBuilder:

    def __init__(self):
        # On mémorise l'état précédent
        # de chaque processus.
        self.previous_processes = {}

    def build(self, processes):
        """
        Transforme les données brutes du System Monitor
        en features utilisables par le modèle ML.
        """

        results = []

        current_processes = {}

        for process in processes:

            pid = process["pid"]
            name = process["name"]

            key = (
                pid,
                name
            )

            # Sauvegarde temporaire de l'état actuel
            current_processes[key] = process

            previous = self.previous_processes.get(
                key
            )

            # --------------------------------------------------
            # Première observation du processus
            # --------------------------------------------------

            if previous is None:

                time_delta = 0

                cpu_change_rate = 0
                memory_change_rate = 0
                threads_change = 0
                connections_change_rate = 0

            # --------------------------------------------------
            # Le processus avait déjà été observé
            # --------------------------------------------------

            else:

                time_delta = (
                    process["timestamp"]
                    - previous["timestamp"]
                )

                if time_delta > 0:

                    cpu_change = (
                        process["cpu_percent"]
                        - previous["cpu_percent"]
                    )

                    memory_change = (
                        process["memory_mb"]
                        - previous["memory_mb"]
                    )

                    threads_change = (
                        process["num_threads"]
                        - previous["num_threads"]
                    )

                    connections_change = (
                        process["connections"]
                        - previous["connections"]
                    )

                    cpu_change_rate = (
                        cpu_change
                        / time_delta
                    )

                    memory_change_rate = (
                        memory_change
                        / time_delta
                    )

                    connections_change_rate = (
                        connections_change
                        / time_delta
                    )

                else:

                    cpu_change_rate = 0
                    memory_change_rate = 0
                    threads_change = 0
                    connections_change_rate = 0

            # --------------------------------------------------
            # Features finales
            # --------------------------------------------------

            features = {
                "pid": pid,

                "name": name,

                "username": process["username"],

                "cpu_percent":
                    process["cpu_percent"],

                "memory_mb":
                    process["memory_mb"],

                "num_threads":
                    process["num_threads"],

                "connections":
                    process["connections"],

                "process_age_seconds":
                    process["process_age_seconds"],

                "cpu_change_rate":
                    round(
                        cpu_change_rate,
                        3
                    ),

                "memory_change_rate":
                    round(
                        memory_change_rate,
                        3
                    ),

                "threads_change":
                    threads_change,

                "connections_change_rate":
                    round(
                        connections_change_rate,
                        3
                    )
            }

            results.append(
                features
            )

        # L'état actuel devient l'état précédent
        # pour la prochaine collecte.
        self.previous_processes = (
            current_processes
        )

        return results
