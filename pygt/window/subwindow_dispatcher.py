
""" Base Application Subwindow Instance """


#   EXTERNAL IMPORTS
from tkinter import Tk


#   INTERNAL IMPORTS
from .subwindow import Subwindow


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class SubwindowDispatcher:
    """ Application subwindow dispatcher. """
    def __init__(self, window: Tk, service_call) -> None:
        self.__main_window: Tk = window if issubclass(type(window), Tk) else None
        self.__service_call = service_call if callable(service_call) else None
        self.__subwindows: dict[str, Subwindow] = {}

    def subwindows(self) -> list[str]:
        """ Returns list of current subwindow identifiers. """
        return [subwindow_id for subwindow_id in self.__subwindows.keys()]

    def is_existing_subwindow(self, identifier: str) -> bool:
        """ Returns true if a subwindow is associated
        with provided identifier. """
        return identifier in self.__subwindows.keys()

    def get_subwindow(self, identifier: str) -> Subwindow:
        """ Returns requested subwindow. """
        return self.__subwindows.get(identifier, None)

    def dispatch(self, identifier: str, subwindow_type: type, **init_args) -> Subwindow:
        """ Dispatch new subwindow instance. """
        if self.is_existing_subwindow(identifier):
            return None

        self.__subwindows[identifier] = subwindow_type(
            master=self.__main_window,
            service_call=self.__service_call,
            closure_call=lambda: self.__release_subwindow(identifier),
            **init_args
        )

        return self.__subwindows[identifier]

    def close(self, identifier: str, **kwargs) -> bool:
        """ Close specified subwindow instance. """
        if not self.is_existing_subwindow(identifier):
            return False

        self.__subwindows[identifier].control.close(**kwargs)

    def __release_subwindow(self, identifier: str) -> None:
        """ Remove subwindow from dispatcher management. """
        if not self.is_existing_subwindow(identifier):
            return

        del self.__subwindows[identifier]
