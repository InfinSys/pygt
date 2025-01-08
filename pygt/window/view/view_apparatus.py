
""" Application Window View Apparatus """


#   EXTERNAL IMPORTS
from tkinter import Tk, Frame


#   INTERNAL IMPORTS
from pygt.view.view_interface import ViewInterface
from pygt.view.navigation.viewport_navigator import ViewportNavigator


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class WindowViewApparatus(ViewInterface):
    """ Application window view apparatus. """
    def __init__(self, window: Tk, service_call) -> None:
        super().__init__(parent=window, service_call=service_call)

        self.__viewport_navigator: ViewportNavigator = ViewportNavigator(
            default_viewport_args={
                'parent': self,
                'service_call': service_call,
            },
            widget_manager=self.widget_manager()
        )
        self.__view_enabled: bool = True
        self.__configure_view()

    @property
    def view(self) -> ViewportNavigator:
        """ Window view apparatus viewport navigator. """
        return self.__viewport_navigator

    def is_enabled(self) -> bool:
        """ Returns true if window view apparatus is enabled. """
        return self.__view_enabled

    def enable_window_view(self) -> None:
        """ Enable window view apparatus. """
        if not self.__view_enabled:
            self.__configure_view()
            self.__view_enabled = True

    def disable_window_view(self) -> None:
        """ Disable window view apparatus. """
        if self.__view_enabled:
            self.pack_forget()
            self.__view_enabled = False

    def __configure_view(self) -> None:
        """ Prepare view apparatus. """
        self.pack_propagate(False)
        self.pack(fill='both', expand=True)
