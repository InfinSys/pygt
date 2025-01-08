
""" Application Window View Interface Controller """


#   EXTERNAL IMPORTS
from tkinter import Frame, Widget


#   INTERNAL IMPORTS
from pygt.window.service import WindowServiceBroker, CoreSvcKeys
from pygt.utility.geometric import is_intersecting_bounds
from pygt.model.geometric import GeoBounds


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ViewController:
    """ Window view interface controller. """
    def __init__(self, view: Frame, view_parent: Widget, service_call) -> None:
        self.__view_ref: Frame = view if issubclass(type(view), Frame) else None
        self.__view_parent_ref: Widget = view_parent
        self.__service_call = service_call if callable(service_call) else None

    def width(self) -> int:
        """ Returns view width. """
        if self.__view_ref.winfo_width() < 2:
            return self.__service(request=CoreSvcKeys.WINDOW_WIDTH)()

        return self.__view_ref.winfo_width()

    def height(self) -> int:
        """ Returns view height. """
        if self.__view_ref.winfo_height() < 2:
            return self.__service(request=CoreSvcKeys.WINDOW_HEIGHT)()

        return self.__view_ref.winfo_height()

    def size(self) -> tuple[int, int]:
        """ Returns size of view as tuple. """
        return self.width(), self.height()

    def parent_width(self) -> int:
        """ Returns view parent widget width. """
        return self.__view_parent_ref.winfo_width()

    def parent_height(self) -> int:
        """ Returns view parent widget height. """
        return self.__view_parent_ref.winfo_height()

    def parent_size(self) -> tuple[int, int]:
        """ Returns size of view parent as tuple. """
        return self.parent_width(), self.parent_height()

    def x_coord(self) -> int:
        """ Returns view on-display x-coordinate. """
        return self.__view_ref.winfo_rootx()

    def y_coord(self) -> int:
        """ Returns view on-display y-coordinate. """
        return self.__view_ref.winfo_rooty()

    def coord(self) -> tuple[int, int]:
        """ Returns coordinate of view anchor point. """
        return self.x_coord(), self.y_coord()

    def rel_x_coord(self) -> int:
        """ Returns view x-coordinate relative to parent. """
        return self.__view_ref.winfo_x()

    def rel_y_coord(self) -> int:
        """ Returns view y-coordinate relative to parent. """
        return self.__view_ref.winfo_y()

    def rel_coord(self) -> tuple[int, int]:
        """ Returns coordinate of view anchor point relative to parent. """
        return self.rel_x_coord(), self.rel_y_coord()

    def vertices(self) -> dict[str, tuple[int, int]]:
        """ Returns coordinates of all four view corners. """
        return {
            'lt': (self.x_coord(), self.y_coord()),
            'lb': (self.x_coord(), (self.y_coord() + self.height())),
            'rb': ((self.x_coord() + self.width()), (self.y_coord() + self.height())),
            'rt': ((self.x_coord() + self.width()), self.y_coord())
        }

    def bounds(self) -> GeoBounds:
        """ Returns two-point bounds coordinates of view position. """
        return GeoBounds(
            x_min=self.x_coord(),
            y_min=self.y_coord(),
            x_max=(self.x_coord() + self.width()),
            y_max=(self.y_coord() + self.height())
        )

    def is_within(self, bounds: GeoBounds) -> bool:
        """ Returns true if view is entirely within provided bounds. """
        view_bounds: GeoBounds = self.bounds()

        if (view_bounds.x_left < bounds.x_left) or (view_bounds.x_right > bounds.x_right):
            return False

        return not ((view_bounds.y_top < bounds.y_top) or (view_bounds.y_bottom > bounds.y_bottom))

    def is_partly_within(self, bounds: GeoBounds) -> bool:
        """ Returns true if any part of view is within provided bounds. """
        return is_intersecting_bounds(b1=self.bounds(), b2=bounds)

    def window_mouse_x(self) -> int:
        """ Returns mouse x-coordinate relative to encompassing window. """
        return self.__service(request=CoreSvcKeys.WINDOW_REL_MOUSE_X)()

    def window_mouse_y(self) -> int:
        """ Returns mouse y-coordinate relative to encompassing window. """
        return self.__service(request=CoreSvcKeys.WINDOW_REL_MOUSE_Y)()

    def window_mouse_coord(self) -> tuple[int, int]:
        """ Returns mouse coordinate relative to encompassing window. """
        return self.__service(request=CoreSvcKeys.WINDOW_REL_MOUSE_COORD)()

    def rel_mouse_x(self) -> int:
        """ Returns mouse x-coordinate relative to view. """
        return self.window_mouse_x() - self.x_coord()

    def rel_mouse_y(self) -> int:
        """ Returns mouse y-coordinate relative to view. """
        return self.window_mouse_y() - self.y_coord()

    def rel_mouse_coord(self) -> tuple[int, int]:
        """ Returns mouse coordinate relative to view. """
        return self.rel_mouse_x(), self.rel_mouse_y()

    def has_mouse(self) -> bool:
        """ Returns true if mouse is within view bounds. """
        rel_mouse_x, rel_mouse_y = self.rel_mouse_coord()

        if (rel_mouse_x < 0) or (rel_mouse_x > self.width()):
            return False
        elif (rel_mouse_y < 0) or (rel_mouse_y > self.height()):
            return False

        return True

    def set_size(self, width: int, height: int) -> None:
        """ Set view size. """
        self.__view_ref.config(width=width, height=height)

    def set_width(self, width: int) -> None:
        """ Set view width. """
        self.__view_ref.config(width=width)

    def set_height(self, height: int) -> None:
        """ Set view height. """
        self.__view_ref.config(height=height)

    def set_scale(self, scale: float, aspect: tuple[int, int] = None) -> None:
        """ Set view size. """
        new_width, new_height = self.__calculate_ratio_size(scale=scale, aspect=aspect)
        self.set_size(width=new_width, height=new_height)

    def set_x_pad(self, x_padding: int) -> None:
        """ Set view x-padding. """
        self.__view_ref.config(padx=x_padding)

    def set_y_pad(self, y_padding: int) -> None:
        """ Set view y-padding. """
        self.__view_ref.config(pady=y_padding)

    def set_padding(self, x_padding: int, y_padding: int) -> None:
        """ Set view padding. """
        self.__view_ref.config(padx=x_padding, pady=y_padding)

    def set_background(self, color: str) -> None:
        """ Set view background color. """
        self.__view_ref.config(bg=color)

    def close(self) -> None:
        """ Close view. """
        print("View close request.")
        pass

    def __service(self, request: str = None) -> any:
        """ Application window services. """
        if request is not None:
            return self.__service_call().request(request)
        else:
            return self.__service_call()

    def __calculate_ratio_size(self, scale: float, aspect: tuple[int, int]) -> tuple[int, int]:
        """ Calculate relative size based on view parent and provided aspect. """
        parent_width, parent_height = self.parent_size()

        new_width: int = 1
        new_height: int = 1

        if aspect is not None:
            aspect_ratio: float = (aspect[0] / aspect[1])

            if (parent_width / parent_height) > aspect_ratio:
                new_height = int(parent_height * scale)
                new_width = int(new_height * aspect_ratio)
            else:
                new_width = int(parent_width * scale)
                new_height = int(new_width / aspect_ratio)
        else:
            new_width = int(parent_width * scale)
            new_height = int(parent_height * scale)

        return new_width, new_height
