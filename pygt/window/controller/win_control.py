
""" Application Window Instance Controller """


#   EXTERNAL IMPORTS
from tkinter import Tk


#   INTERNAL IMPORTS
from pygt.utility.platform import get_windows_version,  \
    win32_get_display_bounds, win32_get_display_bounding_boxes, \
    win32_get_display_dimensions, win32_get_display_coordinates


# This class should be able to...
#   -> [] ...


# Constants
WIN32_VERSION: str = get_windows_version()


class WindowController:
    def __init__(self, window: Tk, window_exit, width: int, height: int) -> None:
        self.__tk: Tk = window if issubclass(type(window), Tk) else None
        self.__tk_exit = window_exit if callable(window_exit) else None
        self.__min_width: int = width if width is not None else 250
        self.__min_height: int = height if height is not None else 250
        self.__is_borderless: bool = False

        for func in [self.__tk.config, self.__tk.minsize]:
            func(width=self.__min_width, height=self.__min_height)

    def width(self) -> int:
        if self.__tk.winfo_width() < 2:
            return self.__min_width

        return self.__tk.winfo_width()

    def height(self) -> int:
        if self.__tk.winfo_height() < 2:
            return self.__min_height

        return self.__tk.winfo_height()

    def x_coord(self) -> int:
        return self.__tk.winfo_x() + 8

    def y_coord(self) -> int:
        return self.__tk.winfo_y()

    def bounds(self) -> dict:
        return {
            'lt': (self.x_coord(), self.y_coord()),
            'lb': (self.x_coord(), (self.y_coord() + self.height())),
            'rb': ((self.x_coord() + self.width()), (self.y_coord() + self.height())),
            'rt': ((self.x_coord() + self.width()), self.y_coord())
        }

    def bounds_box(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return (self.x_coord(), self.y_coord()), ((self.x_coord() + self.width()), (self.y_coord() + self.height()))

    def is_within_bounds(self, bounds: dict[str, tuple[int, int]]) -> bool:
        win_bounds: dict[str, tuple[int, int]] = self.bounds()

        if (win_bounds['lt'][0] < bounds['lt'][0]) or (win_bounds['lt'][1] < bounds['lt'][1]):
            return False

        if (win_bounds['rb'][0] > bounds['rb'][0]) or (win_bounds['rb'][1] > bounds['rb'][1]):
            return False

        return True

    def is_within(self, bbox: tuple[tuple[int, int], tuple[int, int]]) -> bool:
        bounds: tuple[tuple[int, int], tuple[int, int]] = self.bounds_box()

        if (bounds[0][0] < bbox[0][0]) or (bounds[0][1] < bbox[0][1]):
            return False
        elif (bounds[1][0] > bbox[1][0]) or (bounds[1][1] > bbox[1][1]):
            return False

        return True

    def is_partially_within(self, bbox: tuple[tuple[int, int], tuple[int, int]]) -> bool:
        bounds: tuple[tuple[int, int], tuple[int, int]] = self.bounds_box()

        if (bounds[1][0] < bbox[0][0]) or (bounds[0][0] > bbox[1][0]):
            return False
        elif (bounds[1][1] < bbox[0][1]) or (bounds[0][1] > bbox[1][1]):
            return False

        return True

    def is_minimized(self) -> bool:
        return self.__tk.state() == "iconic"

    def is_maximized(self) -> bool:
        return self.__tk.state() == "zoomed"

    def is_on_screen(self) -> bool:
        if self.__tk.state() == "iconic":
            return False

        display_bbox: dict[str, tuple[tuple[int, int], tuple[int, int]]] = win32_get_display_bounding_boxes()

        for name, bbox in display_bbox.items():
            if self.is_partially_within(bbox):
                return True

        return False

    def display_name(self) -> str:
        displays: dict[str, tuple[tuple[int, int], tuple[int, int]]] = win32_get_display_bounding_boxes()

        for name, bounds in displays.items():
            if self.is_within(bounds):
                return name

        for name, bounds in displays.items():
            if self.is_partially_within(bounds):
                return name

    def display_resolution(self) -> tuple[int, int]:
        return win32_get_display_dimensions()[self.display_name()]

    def spanning_displays(self) -> list[str]:
        displays: list[str] = []
        dimensions: dict[str, tuple[tuple[int, int], tuple[int, int]]] = win32_get_display_bounding_boxes()

        for name, bounds in dimensions.items():
            if self.is_partially_within(bounds):
                displays.append(name)

        return displays

    def is_borderless(self) -> bool:
        return self.__is_borderless

    def rel_mouse_x_coord(self) -> int:
        if WIN32_VERSION == "Windows 11":
            return self.__tk.winfo_pointerx() - self.x_coord()
        elif WIN32_VERSION == "Windows 10":
            return self.__tk.winfo_pointerx() - self.x_coord()

    def rel_mouse_y_coord(self) -> int:
        if WIN32_VERSION == "Windows 11":
            return (self.__tk.winfo_pointery() - self.y_coord()) - 38
        elif WIN32_VERSION == "Windows 10":
            return (self.__tk.winfo_pointery() - self.y_coord()) - 31

    def has_mouse(self) -> bool:
        rel_x: int = self.rel_mouse_x_coord()
        rel_y: int = self.rel_mouse_y_coord()

        if (rel_x < 0) or (rel_x > self.width()):
            return False

        if (rel_y < 0) or (rel_y > self.height()):
            return False

        return True

    def set_title(self, title: str) -> None:
        self.__tk.title(title)

    def set_min_size(self, min_w: int, min_h: int) -> None:
        self.__min_width = min_w if min_w > 2 else 2
        self.__min_height = min_h if min_h > 2 else 2
        self.__tk.minsize(width=self.__min_width, height=self.__min_height)

    def set_max_size(self, max_w: int, max_h: int) -> None:
        self.__tk.maxsize(width=max_w, height=max_h)

    def set_size(self, width: int, height: int) -> None:
        self.__tk.geometry(f"{width}x{height}")

    def set_geometry(self, width: int, height: int, x: int, y: int) -> None:
        self.__tk.geometry(f"{width}x{height}+{x}+{y}")

    def set_width(self, width: int) -> None:
        self.__tk.geometry(f"{width}x{self.height()}")

    def set_height(self, height: int) -> None:
        self.__tk.geometry(f"{self.width()}x{height}")

    def set_scale(self, scale: float, aspect: tuple[int, int] = None) -> None:
        new_size: tuple[int, int] = self.__calculate_ratio_size(scale, aspect)
        self.set_size(width=new_size[0], height=new_size[1])

    def set_position(self, x_coord: int, y_coord: int) -> None:
        self.set_geometry(width=self.width(), height=self.height(), x=x_coord, y=y_coord)

    def set_x_coord(self, x_coord: int) -> None:
        self.set_geometry(width=self.width(), height=self.height(), x=x_coord, y=self.y_coord())

    def set_y_coord(self, y_coord: int) -> None:
        self.set_geometry(width=self.width(), height=self.height(), x=self.x_coord(), y=y_coord)

    def set_x_pad(self, x_padding: int) -> None:
        self.__tk.config(padx=x_padding)

    def set_y_pad(self, y_padding: int) -> None:
        self.__tk.config(pady=y_padding)

    def set_padding(self, x_padding: int, y_padding: int) -> None:
        self.__tk.config(padx=x_padding, pady=y_padding)

    def set_background(self, color: str) -> None:
        self.__tk.config(bg=color)

    def center_on_display(self, display: str = None) -> None:
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

    def maximize(self) -> None:
        self.__tk.state("zoomed")

    def restore_down(self) -> None:
        self.__tk.state("normal")

    def minimize(self) -> None:
        self.__tk.iconify()

    def close(self, **kwargs) -> None:
        self.__tk_exit(**kwargs)

    def hide(self) -> None:
        self.__tk.withdraw()

    def show(self) -> None:
        self.__tk.deiconify()

    def enable_native_controls(self) -> None:
        if self.__is_borderless:
            self.__tk.overrideredirect(False)
            self.__is_borderless = True

    def disable_native_controls(self) -> None:
        if not self.__is_borderless:
            self.__tk.overrideredirect(True)
            self.__is_borderless = False

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
