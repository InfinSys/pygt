
"""
Python GUI Toolkit Live Window Controller Tests
"""


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
pass


#   PACKAGE IMPORTS
from pygt.window import Window


#   GLOBAL DEFINITIONS
LIVE_CONTROLLER_TEST_COMMANDS: list[dict] = []


#   HELPER FUNCTIONS
def __add_lctc(func, delay) -> int:
    LIVE_CONTROLLER_TEST_COMMANDS.append({'ms': delay, 'func': func})
    return delay + 700


def __build_live_controller_test_commands(instance: Window) -> None:
    LIVE_CONTROLLER_TEST_COMMANDS.clear()
    cmd_delay: int = 3000
    cmd_delay = __add_lctc(func=lambda: instance.control.disable_native_controls(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.center_on_display(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.enable_native_controls(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.minimize(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.restore_down(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_size(width=500, height=500), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.center_on_display(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_scale(.5, (16, 9)), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.center_on_display(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_title("Testing"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_title("TESTING"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_title("TESTING!!!!!!"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_title("tk"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.enter_fullscreen(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_background("red"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_background("green"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_background("blue"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_background("#000000"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_background("#ffffff"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.exit_fullscreen(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.hide(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.show(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.center_on_display(display="DISPLAY1"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.maximize(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.restore_down(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.center_on_display(display="DISPLAY2"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.maximize(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.restore_down(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.center_on_display(display="DISPLAY3"), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.maximize(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.restore_down(), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_width(500), delay=cmd_delay)
    cmd_delay = __add_lctc(func=lambda: instance.control.set_height(250), delay=cmd_delay)
    __add_lctc(func=lambda: instance.control.center_on_display(), delay=cmd_delay)
    cmd_delay += 500
    __add_lctc(func=lambda: print("Window controller test complete!"), delay=cmd_delay)
    cmd_delay += 500
    __add_lctc(func=lambda: instance.control.set_title("Test Complete!"), delay=cmd_delay)
    cmd_delay += 3000
    __add_lctc(func=lambda: instance.control.set_title("Window Controller Tests"), delay=cmd_delay)
    cmd_delay += 3000
    __add_lctc(func=lambda: instance.control.set_title("Test Complete!"), delay=cmd_delay)
    cmd_delay += 3000
    __add_lctc(func=lambda: instance.control.set_title("Window Controller Tests"), delay=cmd_delay)
    cmd_delay += 3000
    __add_lctc(func=lambda: instance.control.set_title("Test Complete!"), delay=cmd_delay)


#   TEST FUNCTIONS
def live_window_controller_test(instance: Window) -> None:
    """
    Test window controller while in mainloop.

    :param instance: Application window
    """
    __build_live_controller_test_commands(instance=instance)
    for scheduled_command in LIVE_CONTROLLER_TEST_COMMANDS:
        instance.after(**scheduled_command)
