import yaml

from utils import *


if __name__ == "__main__":
    with open("./config.yaml") as config:
        y = yaml.safe_load(config)

        def on_msg(client, userdata, msg):
            global global_message
            print(msg.topic + " " + str(msg.payload))

        configure_sub(
            y["broker_host"],
            int(y["broker_port"]),
            y["broker_user"],
            y["broker_pwd"],
            0,
            y["broker_room_topic"],
            on_msg
        )

        '''
        mqtt_conn = MqttManager(
            y["broker_host"],
            int(y["broker_port"]),
            y["broker_user"],
            y["broker_pwd"],
        )

        mqtt_conn.on_message(y["broker_room_topic"], on_msg)
        mqtt_conn.loop_forever()
        '''

