import os
import shutil
import signal
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


def get_process_data(logs_path, timestamp):
    with open(os.path.join(logs_path, timestamp), "r") as log_file:
        data = json.loads(log_file.read())

    return data


def stop_process(log_path, out_path):
    with open(log_path, "r") as file:
        log_data = json.loads(file.read())

        pid = log_data["process_pid"]
        dir_path = log_data["dir_path"]
        log_data["is_running"] = False
        log_data["was_canceled"] = True
        log_data["process_pid"] = None

        try:
            os.kill(pid, signal.SIGTERM)
        except Exception as e:
            pass

        if os.path.exists(os.path.join(out_path, dir_path)):
            shutil.rmtree(os.path.join(out_path, dir_path))

    with open(log_path, "w") as file:
        file.write(json.dumps(log_data, indent=4))
