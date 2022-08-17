def get_running_processes_data(logs_data, owner_id):
    running_processes_data = []

    for log_data in logs_data:
        if log_data["owner_id"] == owner_id:
            running_processes_data.append(log_data)

    return running_processes_data
