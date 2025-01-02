
""" Application System Graphical Utility """


#   EXTERNAL IMPORTS
from screeninfo import get_monitors


#   INTERNAL IMPORTS
from pygt.utility.platform import is_windows_platform


def win32_get_total_displays() -> int:
    if not is_windows_platform():
        return None

    return len(get_monitors())


def win32_get_display_names() -> list[str]:
    if not is_windows_platform():
        return None

    return [monitor.name.lstrip('\\.') for monitor in get_monitors()]


def win32_get_display_dimensions() -> dict[str, tuple[int, int]]:
    if not is_windows_platform():
        return None

    return {monitor.name.lstrip('\\.'): (monitor.width, monitor.height) for monitor in get_monitors()}


def win32_get_display_coordinates() -> dict[str, tuple[int, int]]:
    if not is_windows_platform():
        return None

    return {monitor.name.lstrip('\\.'): (monitor.x, monitor.y) for monitor in get_monitors()}


def win32_get_display_bounds() -> dict[str, dict[str, tuple]]:
    if not is_windows_platform():
        return None

    display_dimensions: dict = win32_get_display_dimensions()
    display_coord: dict = win32_get_display_coordinates()
    display_bounds: dict[str, dict[str, tuple]] = {}

    for name, coord in display_coord.items():
        display_bounds[name] = {
            'lt': (display_coord[name][0], display_coord[name][1]),
            'lb': (display_coord[name][0], (display_coord[name][1] + display_dimensions[name][1])),
            'rb': ((display_coord[name][0] + display_dimensions[name][0]), (display_coord[name][1] + display_dimensions[name][1])),
            'rt': ((display_coord[name][0] + display_dimensions[name][0]), display_coord[name][1])
        }

    return display_bounds


def win32_get_display_bounding_boxes() -> dict[str, tuple[tuple[int, int], tuple[int, int]]]:
    if not is_windows_platform():
        return None

    display_dimensions: dict = win32_get_display_dimensions()
    display_coord: dict = win32_get_display_coordinates()
    display_boxes: dict[str, dict[str, tuple]] = {}

    for name, coord in display_coord.items():
        display_boxes[name] = (
            (display_coord[name][0], display_coord[name][1]),
            ((display_coord[name][0] + display_dimensions[name][0]),
             (display_coord[name][1] + display_dimensions[name][1]))
        )

    return display_boxes
