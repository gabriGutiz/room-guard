import base64
from io import BytesIO
import json
from mqtt import configure_sub as mqtt_sub
import os
from PIL import Image
import sys
from ultralytics import YOLO


BROKER_HOST = os.environ.get("BROKER_HOST", "ec2-3-82-138-13.compute-1.amazonaws.com")
BROKER_PORT = os.environ.get("BROKER_PORT", 1883)
BROKER_USER = "user1"
BROKER_PWD = "user1"

ROOM_TOPIC = os.environ.get("ROOM_TOPIC", "paho/room")
MSG_QOS = 0

YOLO_MODEL = "yolov8n.pt"


model = YOLO(YOLO_MODEL)


def process_message(msg):
    content = json.load(msg)
    img = Image.open(BytesIO(base64.b64decode(content.get("img"))))


def mqtt_on_message(client, userdata, msg):
    global global_message
    if msg.topic == ROOM_TOPIC:
        print(msg.topic + " " + str(msg.payload))
        process_message(msg.payload)


if __name__ == "__main__":
    try:
        mqtt_sub(
            BROKER_HOST,
            BROKER_PORT,
            BROKER_USER,
            BROKER_PWD,
            MSG_QOS,
            ROOM_TOPIC,
            mqtt_on_message)
    except KeyboardInterrupt:
        sys.exit()

