
""" Base Application Window Viewport """


#   EXTERNAL IMPORTS
from tkinter import Frame


#   INTERNAL IMPORTS
from pygt.view.view_interface import ViewInterface
from pygt.view.navigation.page_navigator import PageNavigator


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class Viewport(ViewInterface):
    """ Base application window viewport. """
    def __init__(self, parent: Frame, service_call) -> None:
        super().__init__(parent=parent, service_call=service_call)

        self.__page_navigator: PageNavigator = PageNavigator(
            default_page_args={
                'viewport': self,
                'service_call': service_call,
            },
            widget_manager=self.widget_manager()
        )

    @property
    def view(self) -> PageNavigator:
        """ Viewport page navigator. """
        return self.__page_navigator
