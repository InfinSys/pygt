
#   IMPORTS
import pygt
from pygt.window import Window
from pygt.view import Viewport, Page
from pygt_tests import WindowTests


if __name__ == "__main__":
    print("\n| Dev Script |\n")

    # Create application window
    window: Window = Window(width=800, height=400)
    window.control.set_background(color="#000000")
    window.view.control.set_background(color="#232323")

    # Attach new viewport to window
    window.view.view.attach(identifier="dev_viewport", viewport_type=Viewport, show=True)
    dev_viewport: Viewport = window.view.view.get_viewport(identifier="dev_viewport")
    window.view.event.bind(
        identifier="dev_vp_sizing",
        sequence="Configure",
        cmd=lambda e: dev_viewport.control.set_scale(scale=.9, aspect=(16, 9))
    )
    dev_viewport.control.set_background(color="#ffffff")

    # Attach new page to viewport
    dev_viewport.view.attach(identifier="dev_page", page_type=Page, show=True)
    dev_page: Page = dev_viewport.view.get_page(identifier="dev_page")
    dev_viewport.event.bind(
        identifier="dev_page_sizing",
        sequence="Configure",
        cmd=lambda e: dev_page.control.set_scale(scale=.5, aspect=(2, 1))
    )
    dev_page.control.set_background(color="#df567e")

    pass

    window.mainloop()

    print("\n| Complete |")
