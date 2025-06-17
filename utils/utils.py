import base64
import io
from PIL import Image
from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.client as mqtt


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
        self._mqttc.subscribe(topic, qos=self._qos)

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


def _on_subscribe(client, userdata, mid, reason_code_list, properties):
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")


def _on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()


def configure_sub(host, port, user, pw, qos, topic, on_msg):

    def _on_connect_with_sub(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
        else:
            client.subscribe(topic, qos = qos)

    mqttc = mqtt.Client(CallbackAPIVersion.VERSION2)
    mqttc.on_connect = _on_connect_with_sub
    mqttc.on_message = on_msg
    mqttc.on_subscribe = _on_subscribe
    mqttc.on_unsubscribe = _on_unsubscribe

    print(f"Connecting to broker {host}:{port}")
    mqttc.username_pw_set(user, pw)
    mqttc.connect(host, port)
    print("Connected to broker")
    mqttc.loop_forever()
    print(f"Received the following message: {mqttc.user_data_get()}")



def img2str(img_path):
    with Image.open(img_path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        img_string = base64.b64encode(img_bytes).decode('utf-8')
    return img_string

