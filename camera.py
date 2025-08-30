from control import app

from picamzero import Camera as c
import exif
from astro_pi_orbit import ISS
from log import logger
import datetime

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
