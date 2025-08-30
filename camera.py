from picamzero import Camera as c
import exif
from astro_pi_orbit import ISS
from log import logger

iss = ISS()

def get_gps_coordinates(iss):
    """
    Returns a tuple of latitude and longitude coordinates expressed
    in signed degrees minutes seconds.
    """
    point = iss.coordinates()
    return (point.latitude.signed_dms(), point.longitude.signed_dms())

class Photo:
    def __init__(self, photo_path):
        self.photo = photo_path

class Camera:
    def __init__(self):
        self.cam = c()
        self.num_photos = 0
        self.log = logger()

    def take_photo(self) -> Photo:
        photo_name = f"ISS{self.num_photos + 1}.jpg"
        self.cam.take_photo(f"{photo_name}", gps_coordinates=get_gps_coordinates(iss))
        self.num_photos += 1
        self.log.info(f"Camera: Photo Taken NO: {self.num_photos}")
        return Photo("gps_image1.jpg")
