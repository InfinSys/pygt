
""" Geometric Quadrilateral Coordinate Model """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
pass


#   CLASSES
class GeoCoord:
    """ Geometric quadrilateral coordinates. """
    def __init__(self, x_coord: int, y_coord: int) -> None:
        self.x: int = x_coord if type(x_coord) is int else 0
        self.y: int = y_coord if type(y_coord) is int else 0

    def coordinates(self) -> tuple[int, int]:
        """ Returns coordinates as tuple. """
        return self.x, self.y
