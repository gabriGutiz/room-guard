import json
import yaml

from utils import *


if __name__ == "__main__":
    with open("./config.yaml") as config:
        y = yaml.safe_load(config)

        img_str = img2str(y.get("free_img_path"))

        data = {
            "is_busy": False
        }

        mqtt_conn = MqttManager(
            y.get("broker_host"),
            int(y.get("broker_port")),
            y.get("broker_user"),
            y.get("broker_pwd"),
        )

        mqtt_conn.publish_msg(y.get("broker_send_action_topic"), json.dumps(data))
        print('Message published')

