import multiprocessing
import os
import shutil
import signal
import json
import youtube_dl


def get_processes(logs_path):
    finished_processes = []
    running_processes = []

    for log in os.listdir(logs_path):
        with open(os.path.join(logs_path, log), "r") as log_file:
            log_data = json.loads(log_file.read())

            log = log.split(".")[0]

            if log_data["is_running"]:
                running_processes.append(log)
            else:
                finished_processes.append(log)

    return running_processes, finished_processes


def stop_process(log_path, out_path):
    with open(log_path, "r") as file:
        log_data = json.loads(file.read())

        pid = log_data["process_pid"]
        dir_path = log_data["dir_path"]
        log_data["is_running"] = False
        log_data["was_canceled"] = True
        log_data["process_pid"] = None

        os.kill(pid, signal.SIGTERM)

        if os.path.exists(os.path.join(out_path, dir_path)):
            shutil.rmtree(os.path.join(out_path, dir_path))

    with open(log_path, "w") as file:
        file.write(json.dumps(log_data, indent=4))


class Process:
    def __init__(self, music_links, timestamp, log_path, dir_path):
        self.music_links = music_links
        self.process_thread = multiprocessing.Process(target=self.process)
        self.timestamp = str(timestamp)
        self.process_pid = None
        self.is_running = False
        self.was_cancelled = False
        self.log_path = log_path
        self.dir_path = dir_path

    def start_process(self):
        if os.path.exists(self.dir_path):
            os.remove(self.dir_path)

        os.mkdir(self.dir_path)

        self.update_log()

        self.process_thread.start()
        self.process_pid = self.process_thread.pid
        self.is_running = True

        self.update_log()

    def process(self):
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "outtmpl": f"{self.dir_path}/%(title)s.%(ext)s",
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(self.music_links)

        os.system(f"zip -r -j {self.dir_path}.zip {self.dir_path}")
        os.system(f"rm -rf {self.dir_path}")

        self.is_running = False

        self.update_log()

    def read_log(self):
        with open(self.log_path, "r") as file:
            log_file = json.loads(file.read())

        return log_file

    def update_log(self):
        if not os.path.exists(self.log_path):
            log_data = {}

            log_data["timestamp"] = self.timestamp
            log_data["dir_path"] = self.dir_path.split("/")[-1]
            log_data["music_links"] = self.music_links
            log_data["process_pid"] = self.process_pid
            log_data["is_running"] = self.is_running
            log_data["was_canceled"] = self.was_cancelled

            with open(self.log_path, "w") as file:
                file.write(json.dumps(log_data, indent=4))
        else:
            log_data = self.read_log()

            log_data["process_pid"] = self.process_pid
            log_data["is_running"] = self.is_running
            log_data["was_canceled"] = self.was_cancelled

            with open(self.log_path, "w") as file:
                file.write(json.dumps(log_data, indent=4))
