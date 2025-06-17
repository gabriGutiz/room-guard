# Este script é feito para ser executado no Ubuntu oficial da Orange Pi
# A instalação do wiringpi deve ser feita seguindo o passo a passo 

import asyncio
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

BROKER_HOST = os.environ.get("BROKER_HOST", "ec2-34-230-39-39.compute-1.amazonaws.com")
BROKER_PORT = int(os.environ.get("BROKER_PORT", 1883))
BROKER_USER = "user1"
BROKER_PWD = "user1"

ROOM_TOPIC = os.environ.get("ROOM_TOPIC", f"paho/room/{ROOM_ID}")
MSG_QOS = 0

WHI_LED_PIN = 2
RED_LED_PIN = 5


wp.wiringPiSetup()
wp.pinMode(WHI_LED_PIN, wp.GPIO.OUTPUT)
wp.pinMode(RED_LED_PIN, wp.GPIO.OUTPUT)


def process_message(msg_body: str) -> None:
    body = json.loads(msg_body)

    if body["is_busy"]:
        wp.digitalWrite(RED_LED_PIN, wp.GPIO.HIGH)
    else:
        wp.digitalWrite(RED_LED_PIN, wp.GPIO.LOW)


def mqtt_on_message(client, userdata, msg):
    global global_message
    if msg.topic == ROOM_TOPIC:
        try:
            print(msg.payload)
            process_message(msg.payload)
        except Exception as e:
            print("Error processing message")


def main():
    print("Running – Ctrl-C to stop")
    try:
        mqtt_sub(
            BROKER_HOST,
            BROKER_PORT,
            BROKER_USER,
            BROKER_PWD,
            MSG_QOS,
            ROOM_TOPIC,
            mqtt_on_message)
    except:
        print("error occurred")
    finally:
        wp.digitalWrite(RED_LED_PIN, wp.GPIO.LOW)
        wp.digitalWrite(WHI_LED_PIN, wp.GPIO.LOW)
        print("\nDone.")


if __name__ == "__main__":
    main()

