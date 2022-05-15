import math
from typing import Final

RRR: Final = 6378.388


def _coordinate_to_radian(coordinate: float) -> float:
    """
    Function to convert coordinate in radians

    Parameters:
    -----------
    coordinate: float
        is the coordinate to be converted

    Returns:
    --------
    float
        the coordinate express in radian
    """
    degrees = int(coordinate)
    minutes = coordinate - degrees
    return math.radians(degrees + minutes * 5 / 3)


def get_distance_geographic(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> int:
    """
    Given the coordinate of two nodes, the function returns the geographic distance of those nodes

    Parameters:
    -----------
    latitude_1: float
        is the latitude of the first point
    longitude_1: float
        is the longitude of the first point
    latitude_2: float
        is the latitude of the second point
    longitude_2: float
        is the longitude of the second point

    Returns:
    --------
    int
        the geographic distance between the two nodes
    """
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


def get_distance_euclidean(x_1: float, y_1: float, x_2: float, y_2: float) -> int:
    """
    Given the coordinate of two nodes, the function returns the euclidean distance of those nodes

    Parameters:
    -----------
    x_1: float
        the abscissa coordinate of the first node
    y_1: float
        the ordinate coordinate of the first node
    x_2: float
        the abscissa coordinate of the second node
    y_2: float
        the ordinate coordinate of the second node

    Returns:
    --------
    int
        the euclidean distance between the two nodes
    """
    return round(math.sqrt(((x_1 - x_2) ** 2) + ((y_1 - y_2) ** 2)))
