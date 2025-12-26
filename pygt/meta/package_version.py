
""" Python Graphical User Interface Toolkit Package Version Information """


#   DEFINITIONS
VERSION_MAJOR: int = 2
""" PyGT version number major. """

VERSION_MINOR: int = 1
""" PyGT version number minor. """

VERSION_PATCH: int = 0
""" PyGT version number patch. """

VERSION_TWEAK: int = 3
""" PyGT version number tweak. """


def get_pygt_version() -> str:
    """ Returns PyGT package version number as string. """
    return f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}.{VERSION_TWEAK}"


def get_pygt_github_version_tag() -> str:
    """ Returns this PyGT GitHub version tag. """
    return f"v{get_pygt_version()}"
