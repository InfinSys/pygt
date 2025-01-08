
"""
Python GUI Toolkit Live Window Services Tests
"""


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
pass


#   PACKAGE IMPORTS
from pygt.window import Window
from pygt.window.service import CoreSvcKeys


#   GLOBAL DEFINITIONS
LIVE_SERVICE_TEST_COMMANDS: list[dict] = []


#   HELPER FUNCTIONS
def __add_lstc(func, delay) -> int:
    """ Add live service test command. """
    LIVE_SERVICE_TEST_COMMANDS.append({'ms': delay, 'func': func})
    return delay + 1000


def __build_live_service_test_commands(instance: Window) -> None:
    LIVE_SERVICE_TEST_COMMANDS.clear()
    cmd_delay: int = 3000
    cmd_delay = __add_lstc(
        func=lambda: print(f"Window width: {instance.service.request(CoreSvcKeys.WINDOW_WIDTH).execute()}"),
        delay=cmd_delay
    )


#   TEST FUNCTIONS
def live_window_services_test(instance: Window) -> None:
    """
    Test window services while in mainloop.

    :param instance: Application window
    """
    __build_live_service_test_commands(instance)
    for scheduled_command in LIVE_SERVICE_TEST_COMMANDS:
        instance.after(**scheduled_command)
