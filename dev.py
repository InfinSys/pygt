
#   IMPORTS
import pygt
from pygt.window import Window
from pygt_tests import WindowTests


if __name__ == "__main__":
    print("\n| Dev Script |\n")

    window: Window = Window(width=300, height=200)

    #window.event.bind(
    #    sequence="Button-1",
    #    cmd=lambda e: print(f"On display: {window.control.display_name()}"),
    #    identifier="id_display"
    #)
    #window.event.bind(
    #    sequence="Button-2",
    #    cmd=lambda e: print(f"Rel. mouse: {window.control.rel_mouse_coord()}"),
    #    identifier="id_mouse_coord"
    #)
    #window.event.bind(
    #    sequence="Button-3",
    #    cmd=lambda e: print(f"On displays: {window.control.spanning_displays()}"),
    #    identifier="id_displays"
    #)

    #WindowTests.live_window_controller_test(window)
    #WindowTests.interactive_window_event_handler_test(window)

    window.mainloop()

    print("\n| Complete |")
