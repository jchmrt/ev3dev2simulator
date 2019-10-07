import math
from pathlib import Path
from typing import Tuple

import yaml
from arcade import PointList


def get_circle_points(center_x: float,
                      center_y: float,
                      radius: float,
                      num_segments: int = 32) -> PointList:
    """
    Determine all the coordinate points located on the outline of a circle of given position and radius.
    The number of points, which correlates to the smoothness of the outline,
    is specified by the number of segments.

    :param center_x: the x coordinate of the created circle center.
    :param center_y: the y coordinate of the created circle center.
    :param radius: the radius of the created circle.
    :param num_segments: the number of segments of the circle outline.
    :return: a PointList object containing the coordinates of the circle points.
    """

    points = []

    for segment in range(num_segments):
        theta = 2.0 * 3.1415926 * segment / num_segments

        x = radius * math.cos(theta) + center_x
        y = radius * math.sin(theta) + center_y

        points.append((x, y))

    points.append(points[0])
    points.append(points[1])
    return points


def pythagoras(x: int, y: int) -> float:
    """
    Calculate Pythagoras' theorem
    :param x: length of one side.
    :param y: length of the other one side.
    :return: a floating point value representing the length of the third side.
    """

    return math.sqrt(x * x + y * y)


def distance_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate the distance between two points in 2D space.
    :param x1: coordinate of point 1
    :param y1: coordinate of point 1
    :param x2: coordinate of point 2
    :param y2: coordinate of point 2
    :return: a floating point value representing the distance.
    """

    v1 = (x2 - x1) ** 2
    v2 = (y2 - y1) ** 2
    return math.sqrt(v1 + v2)


def load_config():
    """
    Load config data from config.yaml
    :return: the config data.
    """

    path = get_project_root() + '/config/config.yaml'

    with open(path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def calc_differential_steering_angle_x_y(b: int, dl: float, dr: float, o: float) -> Tuple[float, float, float]:
    """
    Calculate the next orientation, x and y values of a two-wheel
    propelled object based on the differential steering principle.

    :param b: the distance between the two wheels.
    :param dl: linear displacement of the left motor in pixels.
    :param dr: linear displacement of the right motor in pixels.
    :param o: current orientation of the object in radians.
    :return: the new orientation in degrees and the new x and y values in pixels.
    """

    dc = (dr + dl) / 2
    diff_angle = (dr - dl) / b

    diff_x = dc * math.cos(diff_angle + o)
    diff_y = dc * math.sin(diff_angle + o)

    return diff_angle, diff_x, diff_y


def get_cm_multiplier() -> float:
    """
    Get the multiplier needed for converting pixels to centimeters.
    :return: a floating point value representing the multiplier.
    """

    return 0.150


def get_inch_multiplier() -> float:
    """
    Get the multiplier needed for converting pixels to inches.
    :return: a floating point value representing the multiplier.
    """

    return 0.381


def get_project_root() -> str:
    """
    Get the absolute path to project root folder.
    :return: a string representing the path.
    """

    path = Path(__file__).parent.parent.parent.parent
    return str(path)


def apply_scaling(value):
    return scaling_multiplier * value


def remove_scaling(value):
    return value / scaling_multiplier


scaling_multiplier = load_config()['screen_settings']['scaling_multiplier']
