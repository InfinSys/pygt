
""" Application Window Instance Controller """


#   EXTERNAL IMPORTS
from tkinter import Tk
from math import gcd as greatest_common_divisor


#   INTERNAL IMPORTS
from pygt.utility.platform import get_windows_version,  \
    win32_get_display_bounds, win32_get_display_bounding_boxes, \
    win32_get_display_dimensions, win32_get_display_coordinates
from pygt.utility.geometric import is_intersecting_bounds, \
    find_intersect_bounds
from pygt.model.geometric import GeoBounds


#   GLOBAL DEFINITIONS
DEFAULT_WINDOW_WIDTH: int = 250
DEFAULT_WINDOW_HEIGHT: int = 250

WIN32_VERSION: str = get_windows_version()


#   CLASSES
class WindowController:
    """ Application window instance controller. """
    def __init__(self, window: Tk, width: int, height: int, window_exit_call) -> None:
        self.__tk: Tk = window if issubclass(type(window), Tk) else None
        self.__tk_exit = window_exit_call if callable(window_exit_call) else None
        self.__min_width: int = width if width is not None else DEFAULT_WINDOW_WIDTH
        self.__min_height: int = height if height is not None else DEFAULT_WINDOW_HEIGHT

        for config_func in [self.__tk.config, self.__tk.minsize]:
            config_func(width=self.__min_width, height=self.__min_height)

    def width(self) -> int:
        """ Returns window width. """
        if self.__tk.winfo_width() < 2:
            return self.__min_width

        return self.__tk.winfo_width()

    def height(self) -> int:
        """ Returns window height. """
        if self.__tk.winfo_height() < 2:
            return self.__min_height

        return self.__tk.winfo_height()

    def x_coord(self) -> int:
        """ Returns window on-display x-coordinate. """
        return self.__tk.winfo_x() + 8

    def y_coord(self) -> int:
        """ Returns window on-display y-coordinate. """
        return self.__tk.winfo_y()

    def coord(self) -> tuple[int, int]:
        """ Returns coordinate of window anchor point. """
        return self.x_coord(), self.y_coord()

    def vertices(self) -> dict[str, tuple[int, int]]:
        """ Returns coordinates of all four window corners. """
        return {
            'lt': (self.x_coord(), self.y_coord()),
            'lb': (self.x_coord(), (self.y_coord() + self.height())),
            'rb': ((self.x_coord() + self.width()), (self.y_coord() + self.height())),
            'rt': ((self.x_coord() + self.width()), self.y_coord())
        }

    def bounds(self) -> GeoBounds:
        """ Returns two-point bounds coordinates of window position. """
        return GeoBounds(
            x_min=self.x_coord(),
            y_min=self.y_coord(),
            x_max=(self.x_coord() + self.width()),
            y_max=(self.y_coord() + self.height())
        )

    def is_within(self, bounds: GeoBounds) -> bool:
        """ Returns true if window is entirely within provided bounds. """
        window_bounds: GeoBounds = self.bounds()

        if (window_bounds.x_left < bounds.x_left) or (window_bounds.x_right > bounds.x_right):
            return False

        return not ((window_bounds.y_top < bounds.y_top) or (window_bounds.y_bottom > bounds.y_bottom))

    def is_partly_within(self, bounds: GeoBounds) -> bool:
        """ Returns true if any part of window is within provided bounds. """
        return is_intersecting_bounds(b1=self.bounds(), b2=bounds)

    def display_occupation(self, display: str) -> float:
        """ Returns percentage of window occupying display. """
        if (display is None) or (display.strip() == ""):
            return .0

        (x_min, y_min), (x_max, y_max) = win32_get_display_bounding_boxes()[display]
        display_bounds: GeoBounds = GeoBounds(x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max)
        window_bounds: GeoBounds = self.bounds()

        if not is_intersecting_bounds(b1=display_bounds, b2=window_bounds):
            return .0

        intersect_bounds: GeoBounds = find_intersect_bounds(b1=display_bounds, b2=window_bounds)

        window_area: int = (
            (window_bounds.x_right - window_bounds.x_left) * (window_bounds.y_bottom - window_bounds.y_top)
        )
        overlap_area: int = (
            (intersect_bounds.x_right - intersect_bounds.x_left) * (intersect_bounds.y_bottom - intersect_bounds.y_top)
        )

        return (overlap_area / window_area) * 100

    def is_vertically_resizable(self) -> bool:
        """ Returns true if user can resize window in vertical direction. """
        return self.__tk.resizable()[1] == 1

    def is_horizontally_resizable(self) -> bool:
        """ Returns true if user can resize window in horizontal direction. """
        return self.__tk.resizable()[0] == 1

    def is_minimized(self) -> bool:
        """ Returns true if window is minimized. """
        return self.__tk.state() == "iconic"

    def is_fullscreen(self) -> bool:
        """ Returns true if window is in fullscreen mode. """
        return bool(self.__tk.attributes('-fullscreen'))

    def is_always_topmost(self) -> bool:
        """ Returns true if window is configured to
        persistently remain on top of all others. """
        return bool(self.__tk.attributes('-topmost'))

    def is_maximized(self) -> bool:
        """ Returns true if window is maximized. """
        return self.__tk.state() == "zoomed"

    def is_on_screen(self) -> bool:
        """ Returns true if window is positioned on any display. """
        if self.is_minimized():
            return False

        displays: dict[str, tuple[tuple[int, int], tuple[int, int]]] = win32_get_display_bounding_boxes()

        for display, bounds in displays.items():
            if self.is_partly_within(GeoBounds(bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1])):
                return True

        return False

    def is_borderless(self) -> bool:
        """ Returns true if window contains
        no native windowing system controls. """
        return bool(self.__tk.overrideredirect())

    def display_name(self) -> str:
        """ Returns name of display window is located on. """
        occup_map: dict[str, float] = {}

        for name, _ in win32_get_display_bounding_boxes().items():
            occup_map[name] = self.display_occupation(display=name)

        return max(occup_map, key=occup_map.get)

    def display_resolution(self) -> tuple[int, int]:
        """ Returns resolution of display window is located on. """
        return win32_get_display_dimensions()[self.display_name()]

    def display_aspect_ratio(self) -> tuple[int, int]:
        """ Returns aspect ratio of display window is located on. """
        display_width, display_height = self.display_resolution()
        gcd: int = greatest_common_divisor(display_width, display_height)
        return display_width//gcd, display_height//gcd

    def spanning_displays(self) -> list[str]:
        """ Returns list of display names window is partially on. """
        if self.is_maximized() or self.is_fullscreen():
            return [self.display_name(),]

        displays: dict[str, tuple[tuple[int, int], tuple[int, int]]] = win32_get_display_bounding_boxes()
        spanning: list[str] = []

        for display, bounds in displays.items():
            if self.is_partly_within(GeoBounds(bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1])):
                spanning.append(display)

        return spanning

    def rel_mouse_x_coord(self) -> int:
        """ Returns mouse x-coordinate relative to window. """
        if WIN32_VERSION == "Windows 11":
            return self.__tk.winfo_pointerx() - self.x_coord()
        elif WIN32_VERSION == "Windows 10":
            return self.__tk.winfo_pointerx() - self.x_coord()

    def rel_mouse_y_coord(self) -> int:
        """ Returns mouse y-coordinate relative to window. """
        if WIN32_VERSION == "Windows 11":
            return (self.__tk.winfo_pointery() - self.y_coord()) - 38
        elif WIN32_VERSION == "Windows 10":
            return (self.__tk.winfo_pointery() - self.y_coord()) - 31

    def rel_mouse_coord(self) -> tuple[int, int]:
        """ Returns coordinates of mouse relative to window. """
        return self.rel_mouse_x_coord(), self.rel_mouse_y_coord()

    def has_mouse(self) -> bool:
        """ Returns true if mouse is within window bounds. """
        rel_x: int = self.rel_mouse_x_coord()
        rel_y: int = self.rel_mouse_y_coord()

        if (rel_x < 0) or (rel_x > self.width()):
            return False

        if (rel_y < 0) or (rel_y > self.height()):
            return False

        return True

    def set_title(self, title: str) -> None:
        """ Set window title. """
        self.__tk.title(title)

    def set_min_size(self, min_w: int, min_h: int) -> None:
        """ Set window minimum size. """
        self.__min_width = min_w if min_w > 2 else 2
        self.__min_height = min_h if min_h > 2 else 2
        self.__tk.minsize(width=self.__min_width, height=self.__min_height)

    def set_max_size(self, max_w: int, max_h: int) -> None:
        """ Set window maximum size. """
        self.__tk.maxsize(width=max_w, height=max_h)

    def set_size(self, width: int, height: int) -> None:
        """ Set window size. """
        self.__tk.geometry(f"{width}x{height}")

    def set_geometry(self, width: int, height: int, x: int, y: int) -> None:
        """ Set window geometry. """
        self.__tk.geometry(f"{width}x{height}+{x}+{y}")

    def set_width(self, width: int) -> None:
        """ Set window width. """
        self.__tk.geometry(f"{width}x{self.height()}")

    def set_height(self, height: int) -> None:
        """ Set window height. """
        self.__tk.geometry(f"{self.width()}x{height}")

    def set_scale(self, scale: float, aspect: tuple[int, int] = None) -> None:
        """ Set window size. """
        new_size: tuple[int, int] = self.__calculate_ratio_size(scale=scale, aspect=aspect)
        self.set_size(width=new_size[0], height=new_size[1])

    def set_resizability(self, horizontal: bool = None, vertical: bool = None) -> None:
        """ Set window resize capabilities. """
        h_resize, v_resize = self.__tk.resizable()

        if (horizontal is not None) and (bool(h_resize) != horizontal):
            h_resize = bool(horizontal)

        if (vertical is not None) and (bool(v_resize) != vertical):
            v_resize = bool(vertical)

        self.__tk.resizable(width=h_resize, height=v_resize)

    def toggle_resizability(self) -> None:
        """ Toggle complete window resizability. """
        h_resize, v_resize = self.__tk.resizable()

        if h_resize != v_resize:
            h_resize = False
            v_resize = False
        else:
            h_resize = not bool(h_resize)
            v_resize = not bool(v_resize)

        self.__tk.resizable(width=h_resize, height=v_resize)

    def set_position(self, x_coord: int, y_coord: int) -> None:
        """ Set window display position. """
        self.set_geometry(width=self.width(), height=self.height(), x=x_coord, y=y_coord)

    def set_x_coord(self, x_coord: int) -> None:
        """ Set window on-display x-coordinate. """
        self.set_geometry(width=self.width(), height=self.height(), x=x_coord, y=self.y_coord())

    def set_y_coord(self, y_coord: int) -> None:
        """ Set window on-display y-coordinate. """
        self.set_geometry(width=self.width(), height=self.height(), x=self.x_coord(), y=y_coord)

    def set_x_pad(self, x_padding: int) -> None:
        """ Set window x-padding. """
        self.__tk.config(padx=x_padding)

    def set_y_pad(self, y_padding: int) -> None:
        """ Set window y-padding. """
        self.__tk.config(pady=y_padding)

    def set_padding(self, x_padding: int, y_padding: int) -> None:
        """ Set window padding. """
        self.__tk.config(padx=x_padding, pady=y_padding)

    def set_background(self, color: str) -> None:
        """ Set window background color. """
        self.__tk.configure(bg=color)

    def center_on_display(self, display: str = None) -> None:
        """ Center window on display. """
        center_x: int = 0
        center_y: int = 0

        dimensions: dict[str, tuple[int, int]] = win32_get_display_dimensions()
        coord: dict[str, tuple[int, int]] = win32_get_display_coordinates()

        if display is None:
            center_x = (coord[self.display_name()][0] + int(dimensions[self.display_name()][0] / 2))
            center_x -= int(self.width() / 2)

            center_y = (coord[self.display_name()][1] + int(dimensions[self.display_name()][1] / 2))
            center_y -= int(self.height() / 2)
        else:
            center_x = (coord[display][0] + int(dimensions[display][0] / 2))
            center_x -= int(self.width() / 2)

            center_y = (coord[display][1] + int(dimensions[display][1] / 2))
            center_y -= int(self.height() / 2)

        self.set_position(center_x, center_y)

    def send_to_display(self, display: str, rel_x_coord: int = None, rel_y_coord: int = None) -> None:
        """ Send window to provided display. """
        if (rel_x_coord is None) and (rel_y_coord is None):
            return self.center_on_display(display=display)

        rel_x_coord = 0 if rel_x_coord is None else rel_x_coord
        rel_y_coord = 0 if rel_y_coord is None else rel_y_coord

        display_x_left, display_y_top = win32_get_display_coordinates()[display]

        self.set_position(
            x_coord=(display_x_left + rel_x_coord),
            y_coord=(display_y_top + rel_y_coord)
        )

    def enable_always_on_top(self) -> None:
        """ Set application window to persistently be topmost. """
        if not self.is_always_topmost():
            self.__tk.attributes('-topmost', True)

    def disable_always_on_top(self) -> None:
        """ Remove application window topmost configuration. """
        if self.is_always_topmost():
            self.__tk.attributes('-topmost', False)

    def bring_to_foreground(self, force: bool = False) -> None:
        """ Raise application window above all other open windows. """
        self.__tk.lift()

        if force:
            self.enable_always_on_top()
            self.disable_always_on_top()

    def send_to_background(self) -> None:
        """ Lower application window to bottom of window stack order. """
        self.__tk.lower()

    def enter_fullscreen(self) -> None:
        """ Enter fullscreen mode. """
        if not self.is_fullscreen():
            self.__tk.attributes("-fullscreen", True)

    def exit_fullscreen(self) -> None:
        """ Exit fullscreen mode. """
        if self.is_fullscreen():
            self.__tk.attributes("-fullscreen", False)

    def maximize(self) -> None:
        """ Maximize window. """
        self.__tk.state("zoomed")

    def restore_down(self) -> None:
        """ Restore window. """
        self.__tk.state("normal")

    def minimize(self) -> None:
        """ Minimize window. """
        self.__tk.iconify()

    def close(self, **kwargs) -> None:
        """ Close window. """
        self.__tk_exit(**kwargs)

    def hide(self) -> None:
        """ Hide window. """
        self.__tk.withdraw()

    def show(self) -> None:
        """ Show window. """
        self.__tk.deiconify()

    def enable_native_controls(self) -> None:
        """ Enable native windowing system controls. """
        if self.is_borderless():
            self.__tk.overrideredirect(False)

    def disable_native_controls(self) -> None:
        """ Disable native windowing system controls. """
        if not self.is_borderless():
            self.__tk.overrideredirect(True)

    def __calculate_ratio_size(self, scale: float, aspect: tuple[int, int]) -> tuple[int, int]:
        screen_width, screen_height = self.display_resolution()

        new_width: int = 1
        new_height: int = 1

        if aspect is None:
            new_width = int(screen_width * scale)
            new_height = int(screen_height * scale)
        else:
            aspect_width: int = aspect[0]
            aspect_height: int = aspect[1]
            aspect_ratio: float = (aspect_width / aspect_height)

            if (screen_width / screen_height) > aspect_ratio:
                new_height = int(screen_height * scale)
                new_width = int(new_height * aspect_ratio)
            else:
                new_width = int(screen_width * scale)
                new_height = int(new_width / aspect_ratio)

        return new_width, new_height
