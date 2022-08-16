import multiprocessing
import os
import youtube_dl
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


class Process:
    def __init__(self, app, music_links, timestamp, dir_path):
        self.app = app

        self.music_links = music_links
        self.process_thread = multiprocessing.Process(target=self.process)

        self.timestamp = str(timestamp)
        self.process_pid = None
        self.is_running = False
        self.was_cancelled = False

        self.dir_path = dir_path
        self.downloaded_files = []

        self.db_session = self.init_db_session()

    def init_db_session(self):
        db_engine = sqlalchemy.create_engine(self.app.config["SQLALCHEMY_DATABASE_URI"], poolclass=NullPool)
        session = sessionmaker(bind=db_engine, expire_on_commit=False)

        return session()

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

        self.downloaded_files = os.listdir(self.dir_path)

        os.system(f"zip -r -j {self.dir_path}.zip {self.dir_path}")
        os.system(f"rm -rf {self.dir_path}")

        self.is_running = False

        self.update_log()

        self.finish_process()

    def update_log(self):
        log_data = self.app.redis_manager.get_value(self.timestamp)

        if log_data is None:
            log_data = {}

            log_data["timestamp"] = self.timestamp
            log_data["dir_path"] = self.dir_path.split("/")[-1]
            log_data["music_links"] = self.music_links
            log_data["music_names"] = self.downloaded_files
            log_data["process_pid"] = self.process_pid
            log_data["is_running"] = self.is_running
            log_data["was_canceled"] = self.was_cancelled

            self.app.redis_manager.set_value(self.timestamp, log_data)

        else:
            log_data["process_pid"] = self.process_pid
            log_data["is_running"] = self.is_running
            log_data["was_canceled"] = self.was_cancelled
            log_data["music_names"] = self.downloaded_files

            self.app.redis_manager.set_value(self.timestamp, log_data)

    def finish_process(self):
        self.app.redis_manager.delete_key(self.timestamp)
