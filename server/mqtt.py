from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.client as mqtt


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

