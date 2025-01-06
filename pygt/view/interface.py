
""" Application Window View Base Interface """


#   EXTERNAL IMPORTS
from tkinter import Frame, Widget


#   INTERNAL IMPORTS
from pygt.window.service import WindowServiceBroker
from pygt.view.controller import ViewController
from pygt.event.handler import ViewEventHandler


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ViewInterface(Frame):
    """ Base application window view interface. """
    def __init__(self, parent: Widget, service_call) -> None:
        super().__init__(master=parent)

        self.__parent_ref = parent
        self.__service_call = service_call if callable(service_call) else None

        self.__controller: ViewController = ViewController(
            view=self,
            view_parent=parent,
            service_call=service_call
        )

        self.__event_handler: ViewEventHandler = ViewEventHandler(
            bind_call=self.bind,
            schedule_call=self.after
        )

    @property
    def control(self) -> ViewController:
        """ View controller. """
        return self.__controller

    @property
    def event(self) -> ViewEventHandler:
        """ View event handler. """
        return self.__event_handler

    @property
    def service(self) -> WindowServiceBroker:
        """ View window services. """
        return self.__service_call()
