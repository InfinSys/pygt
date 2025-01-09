
#   IMPORTS
import tkinter as tk
from pygt.window import Window
from pygt.view import Viewport, Page
from pygt.widget import ButtonTypes
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

    # Place controls on new page
    dev_page.widget.new(identifier="page_label", widget=tk.Label(master=dev_page, text="Developer Page"))
    dev_page.widget.pack(identifier="page_label", side=tk.TOP, expand=True)
    dev_page.widget.set_background_of(identifier="page_label", color="#df567e")
    dev_page.widget.set_foreground_of(identifier="page_label", color="#ffffff")
    dev_page.widget.new(identifier="switch_btn", widget=tk.Button(master=dev_page, text="Next", command=lambda: dev_viewport.view.switch('dev_page2')))
    dev_page.widget.pack(identifier="switch_btn", side=tk.TOP, expand=True)

    # Attach another page to viewport
    dev_viewport.view.attach(identifier="dev_page2", page_type=Page)
    dev_page2: Page = dev_viewport.view.get_page(identifier="dev_page2")
    dev_viewport.event.bind(
        identifier="dev_page2_sizing",
        sequence="Configure",
        cmd=lambda e: dev_page2.control.set_scale(scale=.85, aspect=(2, 1))
    )
    dev_page2.control.set_background(color="#000000")
    dev_page2.widget.new(identifier="page_label", widget=tk.Label(master=dev_page2, text="Developer Page 2"))
    dev_page2.widget.pack(identifier="page_label", side=tk.TOP, expand=True)
    dev_page2.widget.set_background_of(identifier="page_label", color="#000000")
    dev_page2.widget.set_foreground_of(identifier="page_label", color="#ffffff")
    dev_page2.widget.new(identifier="switch_btn", widget=tk.Button(master=dev_page2, text="Back", command=lambda: dev_viewport.view.switch('dev_page')))
    dev_page2.widget.pack(identifier="switch_btn", side=tk.TOP, expand=True)

    dev_page.widget.new(
        identifier="flat_btn",
        widget=ButtonTypes.FlatButton(
            master=dev_page,
            text="Click Me",
            fit_to_size=True,
            hover_bg="lightblue"
        )
    )
    dev_page.widget.pack(identifier="flat_btn", side=tk.TOP, expand=True)

    window.control.center_on_display(display="DISPLAY1")
    window.control.maximize()
    window.launch_mainloop()

    print("\n| Complete |")
