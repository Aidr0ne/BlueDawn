from control import app

import math

@app.register_function
def dms_to_decimal(sign, deg, minutes, seconds):
    decimal = deg + minutes/60 + seconds/3600
    if sign < 0:  # negative sign means South or West
        decimal = -decimal
    return decimal

@app.register_function
def harvensine(lat1, lon1, lat2, lon2):
    """Implements the harvensine formula"""
    R = 6371.0  # Earth radius in km
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c