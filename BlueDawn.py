import camera
import Math

from datetime import datetime, timedelta
from time import sleep
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

def main() -> int:
    """ Returns ISS Speed"""
    start_time = datetime.now()
    now_time = datetime.now()
    while (now_time < start_time + timedelta(minutes=config["TimeRun"])):
        now_time = datetime.now()
    return 0
