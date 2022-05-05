import math
from typing import Final

RRR: Final = 6378.388

def _coordinate_to_radian(coordinate: float) -> float:
    degrees = int(coordinate)
    minutes = coordinate - degrees
    return math.radians(degrees + minutes * 5 / 3)

def get_distance_geographic(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> int:
    # Convert coordinates into radians
    latitude_1 = _coordinate_to_radian(latitude_1)
    longitude_1 = _coordinate_to_radian(longitude_1)
    latitude_2 = _coordinate_to_radian(latitude_2)
    longitude_2 = _coordinate_to_radian(longitude_2)

    # Calculate the distance
    q1: float = math.cos(longitude_1 - longitude_2)
    q2: float = math.cos(latitude_1 - latitude_2)
    q3: float = math.cos(latitude_1 + latitude_2)

    distance = RRR * math.acos(0.5 * ((1 + q1) * q2 - (1 - q1) * q3)) + 1
    return int(distance)

def get_distance_euclidean(p_1: int, p_2: int, q_1: int, q_2: int) -> int:
    """
    Given the coordinate of two nodes, the function returns the distance from those nodes
    calculate on an Euclidean plane.

    Parameters:
    -----------

    p1: int
    p2: int
    q1: int
    q2: int
    """
    return round(math.sqrt(((p_1 - q_1) ** 2) + ((p_2 - q_2) ** 2)))
