FROM python:3.13-slim

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && \
    apt-get install ffmpeg libsm6 libxext6 -y

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./server.py"]
