import os
import json


def get_processes(logs_path):
    finished_processes = []
    running_processes = []

    for log in os.listdir(logs_path):
        if log.endswith(".json"):
            with open(os.path.join(logs_path, log), "r") as log_file:
                log_data = json.loads(log_file.read())

                log = log.split(".")[0]

                if log_data["is_running"]:
                    running_processes.append(log)
                else:
                    finished_processes.append(log)

    return running_processes, finished_processes
