from control import app

import math

@app.register_function
def dms_to_decimal(sign, deg, minutes, seconds):
    decimal = deg + minutes/60 + seconds/3600
    if sign < 0:  # negative sign means South or West
        decimal = -decimal
    return decimal

@app.register_function
def calculate_mean_distance(coordinates_1, coordinates_2):
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)

@app.register_function
def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    distance = feature_distance * GSD / 100000
    speed = distance / time_difference.seconds
    return speed

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