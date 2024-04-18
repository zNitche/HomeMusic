FROM python:3.8.5

COPY . /HomeMusic

WORKDIR /HomeMusic

RUN pip3 install -r requirements.txt
RUN apt update && apt -y install ffmpeg zip

CMD gunicorn -c gunicorn.conf.py app:app --preload