import threading
import time
from obsws_python import ReqClient

HOST = "localhost"
PORT = 4455
PASSWORD = "YOUR_PASSWORD"

SCENE_NAME = "Chatbox test"
SOURCE_NAME = "Video Capture Device 3"
WAIT_SECONDS = 5  # 2 minutes





def half_height_temporarily():
    ws = ReqClient(
        host=HOST,
        port=PORT,
        password=PASSWORD
    )

    # Get scene items
    items = ws.get_scene_item_list(
        SCENE_NAME
    ).scene_items

    item = next(i for i in items if i["sourceName"] == SOURCE_NAME)
    item_id = item["sceneItemId"]

    # Get current transform
    transform = ws.get_scene_item_transform(
        SCENE_NAME,
        item_id
    ).scene_item_transform

    original_scale_y = transform["scaleY"]

    # Half the height
    ws.set_scene_item_transform(
        SCENE_NAME,
        item_id,
        {
            "scaleY": original_scale_y * 0.5
        }
    )

    time.sleep(WAIT_SECONDS)

    # Restore original size
    ws.set_scene_item_transform(
        SCENE_NAME,
        item_id,
        {
            "scaleY": original_scale_y
        }
    )

    ws.disconnect()


def trigger_squish():
    threading.Thread(
        target=half_height_temporarily,
        daemon=True
    ).start()


if __name__ == "__main__":
    trigger_squish()
    while True:
        time.sleep(1)
