import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883
BROKER_USER = "server"
BROKER_PWD = "server@pwd1"

ROOM_TOPIC = "paho/room"
MSG_QOS = 0


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")


def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()


def on_message(client, userdata, msg):
    global global_message
    if msg.topic == ROOM_TOPIC:
        print(msg.topic + " " + str(msg.payload))


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        client.subscribe(ROOM_TOPIC, qos = MSG_QOS)


if __name__ == "__main__":
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_unsubscribe = on_unsubscribe

    mqttc.username_pw_set(BROKER_USER, BROKER_PWD)
    mqttc.connect(BROKER_HOST, BROKER_PORT)
    mqttc.loop_forever()
    print(f"Received the following message: {mqttc.user_data_get()}")

