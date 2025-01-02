
""" Application Operating System Utility """


#   EXTERNAL IMPORTS
import platform
import sys


# Constants
WINDOWS_10: str = "Windows 10"
WINDOWS_11: str = "Windows 11"


def is_windows_platform() -> bool:
    return sys.platform == "win32"


def get_windows_version() -> str:
    if not is_windows_platform():
        return None

    build: int = int(platform.version().split('.')[2])

    if build >= 22000:
        return WINDOWS_11
    elif (build >= 10240) and (build < 22000):
        return WINDOWS_10

    return None
