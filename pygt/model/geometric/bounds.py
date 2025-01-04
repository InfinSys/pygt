
""" Geometric Quadrilateral Coordinate Bounds Model """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
pass


#   CLASSES
class GeoBounds:
    """ Geometric quadrilateral coordinate bounds. """
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int) -> None:
        self.x_left: int = x_min if type(x_min) is int else 0
        self.y_top: int = y_min if type(y_min) is int else 0
        self.x_right: int = x_max if type(x_max) is int else 0
        self.y_bottom: int = y_max if type(y_max) is int else 0
