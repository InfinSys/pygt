
#   IMPORTS
import pygt
from pygt.window import AppWindow
from pygt_tests import WindowTests


if __name__ == "__main__":
    print("\n| Dev Script |\n")

    window: AppWindow = AppWindow(width=300, height=200)

    window.event.bind(sequence="<Button-1>", func=lambda e: print(f"On display: {window.control.display_name()}"))
    window.event.bind(sequence="<Button-2>", func=lambda e: print(f"Rel. mouse: {window.control.rel_mouse_coord()}"))
    window.event.bind(sequence="<Button-3>", func=lambda e: print(f"On displays: {window.control.spanning_displays()}"))

    WindowTests.live_window_controller_test(window)

    window.mainloop()

    print("\n| Complete |")
