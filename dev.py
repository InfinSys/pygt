
#   IMPORTS
from pygt.window import Window, Subwindow
from pygt_tests import WindowTests


if __name__ == "__main__":
    print("\n| Dev Script |\n")

    window: Window = Window(width=800, height=400)
    window.control.set_background(color="#000000")
    window.view.control.set_background(color="#232323")

    window.launch_mainloop()

    print("\n| Complete |")
