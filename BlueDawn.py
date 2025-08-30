import camera
import Math
import log

from datetime import datetime, timedelta
from time import sleep
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

###################################################################################################

def main() -> int:
    """ Returns ISS Speed"""

    l = log.logger(config=config, log_config=True)
    cam = camera.Camera()
    start_time = datetime.now()
    now_time = datetime.now()
    speed = 0

    while (now_time < start_time + timedelta(minutes=config["TimeRun"])):
        now_time = datetime.now()

    if speed == 0:
        return int(config["DefualtSpeed"])
    return speed
