import multiprocessing
from config import Config


bind = f"{Config.APP_HOST}:{Config.APP_PORT}"

workers = int(multiprocessing.cpu_count() / 2)
threads = 2
worker_class = "gthread"

timeout = 5
keepalive = 1
