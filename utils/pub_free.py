import json
import yaml

from utils import *


if __name__ == "__main__":
    with open("./config.yaml") as config:
        y = yaml.safe_load(config)

        img_str = img2str(y.get("free_img_path"))

        data = {
            "room_id": "804d9fa5-e65b-49ed-92de-082e38cda6a9",
            "time": "now",
            "img": img_str,
            "door_is_closed": False,
        }

        mqtt_conn = MqttManager(
            y.get("broker_host"),
            int(y.get("broker_port")),
            y.get("broker_user"),
            y.get("broker_pwd"),
        )

        mqtt_conn.publish_msg(y.get("broker_room_topic"), json.dumps(data))
        print('Message published')

