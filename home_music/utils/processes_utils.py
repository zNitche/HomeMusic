def get_running_processes(logs_data):
    running_processes = []

    for log_data in logs_data:
        if log_data["is_running"]:
            running_processes.append(log_data["timestamp"])

    return running_processes
