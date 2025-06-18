# Este script é feito para ser executado no Ubuntu oficial da Orange Pi
# A instalação do wiringpi deve ser feita seguindo o passo a passo 

import base64
import cv2
import datetime
import json
from mqtt import configure_sub as mqtt_sub
import os
from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.client as mqtt
import sys
import time
import traceback
import wiringpi as wp
from zoneinfo import ZoneInfo


ROOM_ID = "01a24e11-be17-490a-b754-4a92cd0f15a4"

BROKER_HOST = os.environ.get("BROKER_HOST", "ec2-44-201-199-224.compute-1.amazonaws.com")
BROKER_PORT = int(os.environ.get("BROKER_PORT", 1883))
BROKER_USER = "user1"
BROKER_PWD = "user1"

ROOM_TOPIC = os.environ.get("ROOM_TOPIC", "paho/room")
MSG_QOS = 0

DOOR_SENSOR_PIN = 13


wp.wiringPiSetup()
wp.pinMode(DOOR_SENSOR_PIN, wp.GPIO.INPUT)


def take_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Can not open camera")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to grab frame")
        return None

    _, buffer = cv2.imencode(".jpg", frame)

    img_base64 = base64.b64encode(buffer).decode("utf-8")
    return img_base64


def door_is_closed():
    door_state = wp.analogRead(DOOR_SENSOR_PIN)
    print(f"DOOR STATE: {door_state}")
    return door_state == 1


def send_message_mqtt(state):
    client = mqtt.Client(CallbackAPIVersion.VERSION2)
    client.username_pw_set(BROKER_USER, BROKER_PWD)
    client.connect(BROKER_HOST, BROKER_PORT)
    client.publish(ROOM_TOPIC, json.dumps(state))
    client.disconnect()


def send_current_state():
    now = datetime.datetime.now(ZoneInfo("America/Sao_Paulo"))
    state = {
        "room_id": ROOM_ID,
        "time": str(now),
        "img": take_image(),
        "door_is_closed": door_is_closed()
    }
    print(f"{now}: room_id={ROOM_ID} img {'taken' if state['img'] != None else 'not taken'} door_closed={state['door_is_closed']}")
    send_message_mqtt(state)


def send_state():
    while True:
        try:
            send_current_state()
        except:
            print("error occurred")
            traceback.print_exc()
        finally:
            time.sleep(10)


def main():
    print("Running – Ctrl-C to stop")
    try:
        send_state()
    except:
        print("error occurred")
    finally:
        print("\nDone.")


if __name__ == "__main__":
    # asyncio.run(main())
    main()

