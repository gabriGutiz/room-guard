import boto3
import json
import logging
from mqtt import configure_sub as mqtt_sub
import os
from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.client as mqtt
import sys

from img import is_room_empty


LOGS_FOLDER_NAME = "./logs"
LOGS_FILE_NAME = LOGS_FOLDER_NAME + "/server.log"

BROKER_HOST = os.environ.get("BROKER_HOST", "ec2-52-90-173-232.compute-1.amazonaws.com")
BROKER_PORT = int(os.environ.get("BROKER_PORT", 1883))
BROKER_USER = "user1"
BROKER_PWD = "user1"

ROOM_TOPIC = os.environ.get("ROOM_TOPIC", "paho/room")
MSG_QOS = 0

AWS_REGION = os.environ.get("aws_region", "us-east-1")


dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

room_guard_table = dynamodb.Table("room-guard")


class RoomState:
    room_id: str
    time: str
    room_is_empty: bool
    door_is_closed: bool


def _extract_msg_state(msg_body: str) -> RoomState:
    body = json.loads(msg_body)

    state = RoomState()
    state.room_id = body.get("room_id")
    state.time = body.get("time")
    state.room_is_empty = is_room_empty(body.get("img"))
    state.door_is_closed = body.get("door_is_closed")

    return state


def send_mqtt_message(room_id: str, is_busy: bool):
    client = mqtt.Client(CallbackAPIVersion.VERSION2)
    client.username_pw_set(BROKER_USER, BROKER_PWD)
    client.connect(BROKER_HOST, BROKER_PORT)
    client.publish(ROOM_TOPIC + f"/{room_id}", json.dumps({"is_busy": is_busy}))
    client.disconnect()


def process_message(msg_body: str) -> None:
    state = _extract_msg_state(msg_body)

    if state.room_is_empty:
        logging.info("THERE IS PEOPLE IN THE ROOM")

    room_guard_table.put_item(
        Item={
            "id": f"room-{state.room_id}",
            "type": "room",
            "room_is_empty": state.room_is_empty,
            "datetime": state.time
        }
    )

    send_mqtt_message(state.room_id, not state.room_is_empty)


def mqtt_on_message(client, userdata, msg):
    global global_message
    if msg.topic == ROOM_TOPIC:
        try:
            #print(msg.topic + " " + str(msg.payload))
            process_message(msg.payload)
        except Exception as e:
            logging.exception("Error processing message")


if __name__ == "__main__":
    try:
        if not os.path.exists(LOGS_FOLDER_NAME):
            print(f"Folder {LOGS_FOLDER_NAME} does not exists. Creating folder...")
            os.mkdir(LOGS_FOLDER_NAME)
        else:
            print(f"Folder {LOGS_FOLDER_NAME} already exists. Skipping mkdir...")

        logging.basicConfig(filename=LOGS_FILE_NAME, level=logging.INFO)

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

