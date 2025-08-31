import camera
import Math
import log
from control import app, config

from datetime import datetime, timedelta
from time import sleep
from astro_pi_orbit import ISS
import cv2
iss = ISS()

l = log.logger(config=config, log_config=True, log_fc=True)

###################################################################################################

@app.register_function
def a():
    pass

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

        diff = cam.get_time_diff(cam.photo_list[i], cam.photo_list[i+1])
        l.debug(f"TIME (DIFF): {diff}")
        time += diff.total_seconds()
        l.debug(f"TIME: {time}")

    speed = (distance / time)
    return speed

def find_coords(k1, k2, matches):
    coordinates_1 = []
    coordinates_2 = []
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1,y1) = k1[image_1_idx].pt
        (x2,y2) = k2[image_2_idx].pt
        coordinates_1.append((x1,y1))
        coordinates_2.append((x2,y2))
    return coordinates_1, coordinates_2

def feature_matchng(cam: camera.Camera):
    cam.photo_list[0].load_image()
    cam.photo_list[1].load_image()
    diff = cam.get_time_diff(cam.photo_list[0], cam.photo_list[1])
    k1, d1 = cam.photo_list[0].get_features()
    k2, d2 = cam.photo_list[1].get_features()
    matches = cam.photo_list[0].compare_features(cam.photo_list[1])
    c1, c2 = find_coords(k1, k2, matches)
    afd = Math.calculate_mean_distance(c1, c2)
    speed = Math.calculate_speed_in_kmps(afd, config.config["solution"]["matching"]["GSD"], diff)
    return speed


def main() -> float:
    """ Returns ISS Speed"""

    cam = camera.Camera()
    start_time = datetime.now()
    now_time = datetime.now()
    speed = 0.0

    while (now_time < start_time + timedelta(minutes=config.config["TimeRun"])):
        now_time = datetime.now()
        cam.take_photo()
        sleep(config.config["TimeBetweenPhotos"])

    speed = feature_matchng(cam)

    if speed == 0.0:
        return int(config.config["DefualtSpeed"])
    return speed
