from control import app, config

from picamzero import Camera as c
import exif
from astro_pi_orbit import ISS
from log import logger
import datetime
import cv2

iss = ISS()

@app.register_function
def get_gps_coordinates(iss):
    """
    Returns a tuple of latitude and longitude coordinates expressed
    in signed degrees minutes seconds.
    """
    point = iss.coordinates()
    return (point.latitude.signed_dms(), point.longitude.signed_dms())

@app.register_class
class Photo:
    def __init__(self, photo_path, time, coords):
        self.photo = photo_path
        self.time = time
        self.gps = coords
        self.keypoints = None
        self.cv2_image = None
        self.descriptures = None

    def load_image(self):
        self.cv2_image = cv2.imread(self.photo)

    def remove_image(self):
        self.cv2_image = None

    def get_features(self):
        if self.cv2_image is None:
            self.load_image()
        orb = cv2.ORB.create(nfeatures=int(config.config["camera"]["Photo"]["NumberOfFeatures"]))
        self.keypoints, self.descriptures = orb.detectAndCompute(self.cv2_image, None) # type: ignore
        return self.keypoints, self.descriptures
    
    def compare_features(self, photo2):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(self.descriptures, photo2.descriptures) # type: ignore
        matches = sorted(matches, key=lambda x: x.distance)
        return matches


@app.register_class
class Camera:
    def __init__(self):
        self.cam = c()
        self.num_photos = 0
        self.log = logger()
        self.photo_list = []

    def take_photo(self) -> Photo:
        photo_name = f"ISS{self.num_photos + 1}.jpg"
        gps_coords = get_gps_coordinates(iss)
        self.cam.take_photo(f"{photo_name}", gps_coordinates=gps_coords)
        self.num_photos += 1
        self.log.info(f"Camera: Photo Taken NO: {self.num_photos}")

        time = datetime.datetime.now()

        p = Photo(photo_name, time, gps_coords)
        self.photo_list.append(p)

        return p
    
    def get_time_diff(self, p1, p2):
        time1 = p1.time
        time2 = p2.time
        diff = time2 - time1
        return diff
