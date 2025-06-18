import base64
import io
import json
from PIL import Image
import paho.mqtt.client as mqtt
import time


BROKER_HOST = "ec2-44-201-199-224.compute-1.amazonaws.com"
BROKER_PORT = 1883
BROKER_USER = "user1"
BROKER_PWD = "user1"

ROOM_TOPIC = "paho/room"
MSG_QOS = 0


class MqttManager:
    def __init__(self, host, port, user, pwd, qos=0):
        self._host = host
        self._port = port
        self._user = user
        self._pwd = pwd
        self._qos = qos

        self._connect();

    def _connect(self):
        self._mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self._mqttc.username_pw_set(self._user, self._pwd)
        self._mqttc.connect(self._host, self._port)


    def _disconnect(self):
        self._mqttc.disconnect()


    def on_message(self, topic, on_msg):
        self._mqttc.subscribe(ROOM_TOPIC, qos=MSG_QOS)

        def _on_msg(client, userdata, msg):
            if msg.topic == topic:
                on_msg(msg)
            else:
                print(f"'{msg.topic}' is not the topic")

        self._mqttc.on_message = _on_msg


    def publish_msg(self, topic, msg):
        self._mqttc.publish(topic, msg, qos=self._qos)


    def loop_forever(self):
        self._mqttc.loop_forever()


def img2str(img_path):
    with Image.open(img_path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        img_string = base64.b64encode(img_bytes).decode('utf-8')
    return img_string


if __name__ == "__main__":
    img_str = img2str("./test-data/free.jpeg")

    data = {
        "datetime": "now",
        "img": img_str
    }

    mqtt_conn = MqttManager(
        BROKER_HOST,
        BROKER_PORT,
        BROKER_USER,
        BROKER_PWD,
    )

    mqtt_conn.publish_msg(ROOM_TOPIC, "TESTE IOT")
    print('Message published')
    '''

    def on_msg(msg):
        print(f"MESSAGE RECEIVED: '{msg.payload}'")

    mqtt_conn.on_message(ROOM_TOPIC, on_msg)

    mqtt_conn.loop_forever()
    '''

