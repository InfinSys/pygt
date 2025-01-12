
""" Base Application Subwindow Instance """


#   EXTERNAL IMPORTS
from tkinter import Toplevel, Tk


#   INTERNAL IMPORTS
from pygt.window.controller import WindowController
from pygt.event.handler import ViewEventHandler, ExitHandler
from pygt.window.service import WindowServiceBroker, ServiceEndpoint
from pygt.window.view import WindowViewApparatus


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class Subwindow(Toplevel):
    """ Base application subwindow class. """
    def __init__(self, master: Tk, service_call, width: int = None, height: int = None, **kwargs) -> None:
        super().__init__()

        self.__parent_window: Tk = master if issubclass(type(master), Tk) else None
        self.__service_call = service_call if callable(service_call) else None
        self.__closure_call = kwargs.get('closure_call', None)
        self.__closure_call = self.__closure_call if callable(self.__closure_call) else None

        self.__controller: WindowController = WindowController(
            window=self,
            width=width,
            height=height,
            window_exit_call=self.window_exit
        )

        self.__event_handler: ViewEventHandler = ViewEventHandler(
            bind_call=self.bind,
            schedule_call=self.after
        )

        self.__view_apparatus: WindowViewApparatus = WindowViewApparatus(
            window=self,
            service_call=service_call
        )

        self.__exit_handler: ExitHandler = ExitHandler(final_call=self.destroy)

        if self.has_managed_exit():
            self.exit.add_exit_prerequisite(
                identifier="master_exit_notify",
                task=ServiceEndpoint(func=self.__closure_call)
            )

        self.__configure()

    @property
    def control(self) -> WindowController:
        """ Window controller. """
        return self.__controller

    @property
    def event(self) -> ViewEventHandler:
        """ Window event handler. """
        return self.__event_handler

    @property
    def service(self) -> WindowServiceBroker:
        """ Window services broker. """
        return self.__service_call()

    @property
    def view(self) -> WindowViewApparatus:
        """ Window view apparatus. """
        return self.__view_apparatus

    @property
    def exit(self) -> ExitHandler:
        """ Window exit handler. """
        return self.__exit_handler

    def controller(self) -> WindowController:
        """ Returns window controller. """
        return self.__controller

    def view_apparatus(self) -> WindowViewApparatus:
        """ Returns window view apparatus. """
        return self.__view_apparatus

    def event_handler(self) -> ViewEventHandler:
        """ Returns window event handler. """
        return self.__event_handler

    def has_managed_exit(self) -> bool:
        """ Returns true if subwindow is configured
        to update status on exit. """
        return self.__closure_call is not None

    def window_exit(self, prereq_override: bool = False, exit_status: int = None) -> int:
        """ Inititate window exit sequence. """
        if (prereq_override is True) and (exit_status is None):
            return self.__exit_handler.do_forceful_exit()
        elif (prereq_override is False) and (exit_status is None):
            return self.__exit_handler.do_graceful_exit()
        elif prereq_override is True:
            self.__exit_handler.do_forceful_exit()
            return exit_status
        else:
            self.__exit_handler.do_graceful_exit()
            return exit_status

    def __configure(self) -> None:
        """ Prepapre application window. """
        self.protocol("WM_DELETE_WINDOW", self.window_exit)

    def __key(self) -> int:
        return self.__hash__() + self.winfo_id()
