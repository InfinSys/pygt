
"""
Python GUI Toolkit Live Window Controller Tests
"""


#   EXTERNAL IMPORTS
from tkinter import Event


#   INTERNAL IMPORTS
pass


#   PACKAGE IMPORTS
from pygt.window import Window


#   GLOBAL DEFINITIONS
pass


#   HELPER FUNCTIONS
def __test_forward_function(event: Event) -> None:
    print(f"Successfully forwarded window event: {event}")


#   TEST FUNCTIONS
def interactive_window_event_handler_test(instance: Window) -> None:
    """
    Interact with window event handler in mainloop.

    :param instance: Application window
    """
    instance.event.bind(
        sequence="Button-1",
        cmd=lambda event: print(f"Left-click"),
        identifier="left_click"
    )
    instance.event.bind(
        sequence="Button-2",
        cmd=lambda e: print(f"Scroll-wheel click"),
        identifier="scroll_click"
    )
    instance.event.bind(
        sequence="Button-3",
        cmd=lambda e: print(f"Right-click"),
        identifier="right_click"
    )
    instance.event.bind(
        sequence="MouseWheel",
        cmd=lambda e: print(f"Scrolling..."),
        identifier="scroll"
    )

    instance.event.forward(
        sequence="Button-2",
        func=__test_forward_function
    )

    bind_keys: str = "abcdefghijklmnopqrstuvwxyz"

    for key in bind_keys:
        instance.event.bind(
            sequence=key,
            cmd=lambda e, key_pressed: print(f"You pressed {key_pressed}"),
            identifier=f"{key}_key_listener",
            args={'key_pressed': key}
        )
