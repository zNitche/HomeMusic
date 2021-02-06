FROM python:3.8.5

COPY . /HomeMusic

WORKDIR /HomeMusic

RUN pip3 install -r requirements.txt
RUN apt -y install ffmpeg zip

CMD ["python3", "app.py"]