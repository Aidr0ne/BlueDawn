import camera
import Math
import log
from control import app

from datetime import datetime, timedelta
from time import sleep
import tomllib
from astro_pi_orbit import ISS
iss = ISS()

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

l = log.logger(config=config, log_config=True, log_fc=True)

###################################################################################################

@app.register_function
def harvensine(cam: camera.Camera):
    speed = 0     #    S
    distance = 0  #--------
    time = 0      #  D | T
    if len(cam.photo_list) % 2 == 1:
        cam.photo_list.pop(len(cam.photo_list)-1)
        l.debug("Deleted Odd Photo From List")


    for i in range(0, len(cam.photo_list)-1, 1):
        coords1 = cam.photo_list[i].gps
        coords2 = cam.photo_list[i+1].gps
        lat1 = Math.dms_to_decimal(coords1[0][0], coords1[0][1], coords1[0][2], coords1[0][3])
        lon1 = Math.dms_to_decimal(coords1[1][0], coords1[1][1], coords1[1][2], coords1[1][3])
        lat2 = Math.dms_to_decimal(coords2[0][0], coords2[0][1], coords2[0][2], coords2[0][3])
        lon2 = Math.dms_to_decimal(coords2[1][0], coords2[1][1], coords2[1][2], coords2[1][3])
        distance += Math.harvensine(lat1, lon1, lat2, lon2)
        l.debug(f"DISTANCE: {Math.harvensine(lat1, lon1, lat2, lon2)}KM")
        l.debug(f"DISTANCE (TOTAL): {distance}KM")

        time1 = cam.photo_list[i].time
        time2 = cam.photo_list[i+1].time
        diff = time2 - time1
        l.debug(f"TIME (DIFF): {diff}")
        time += diff.total_seconds()
        l.debug(f"TIME: {time}")

    speed = (distance / time)
    return speed

@app.register_function
def main() -> float:
    """ Returns ISS Speed"""

    cam = camera.Camera()
    start_time = datetime.now()
    now_time = datetime.now()
    speed = 0.0

    while (now_time < start_time + timedelta(minutes=config["TimeRun"])):
        now_time = datetime.now()
        cam.take_photo()
        sleep(config["TimeBetweenPhotos"])

    speed = harvensine(cam)

    if speed == 0.0:
        return int(config["DefualtSpeed"])
    return speed
