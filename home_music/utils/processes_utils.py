def get_running_processes(logs_data, owner_id):
    running_processes = []

    for log_data in logs_data:
        if log_data["is_running"] and log_data["owner_id"] == owner_id:
            running_processes.append(log_data["timestamp"])

    return running_processes
