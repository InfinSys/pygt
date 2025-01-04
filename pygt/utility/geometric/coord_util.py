
""" Geometric Coordinate Utility """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
from pygt.model.geometric import GeoCoord, GeoBounds


#   GLOBAL DEFINITIONS
pass


#   FUNCTIONS
def is_intersecting_bounds(b1: GeoBounds, b2: GeoBounds) -> bool:
    """ Returns true if provided geometric bounds overlap. """
    x_left = max(b1.x_left, b2.x_left)
    y_top = max(b1.y_top, b2.y_top)
    x_right = min(b1.x_right, b2.x_right)
    y_bottom = min(b1.y_bottom, b2.y_bottom)

    return not ((x_right <= x_left) or (y_bottom <= y_top))


def find_intersect_bounds(b1: GeoBounds, b2: GeoBounds) -> GeoBounds:
    """ Returns geometric bounds of intersection area if any. """
    if not is_intersecting_bounds(b1, b2):
        return None

    return GeoBounds(
        x_min=max(b1.x_left, b2.x_left),
        y_min=max(b1.y_top, b2.y_top),
        x_max=min(b1.x_right, b2.x_right),
        y_max=min(b1.y_bottom, b2.y_bottom)
    )
