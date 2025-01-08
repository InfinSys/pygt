
""" Base Application Window Instance """


#   EXTERNAL IMPORTS
import tkinter as tk


#   INTERNAL IMPORTS
from pygt.window.controller import WindowController
from pygt.event.handler import ViewEventHandler
from pygt.window.service import WindowServiceBroker, ServiceEndpoint, \
    CoreSvcKeys
from pygt.window.view import WindowViewApparatus


#   GLOBAL DEFINITIONS
WIN32_DPI_AWARENESS: bool = False


# Application DPI awareness
try:
    # Windows Platform
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    WIN32_DPI_AWARENESS = True
except Exception:
    WIN32_DPI_AWARENESS = False


#   CLASSES
class Window(tk.Tk):
    """ Base main application window class. """
    def __init__(self, width: int = None, height: int = None) -> None:
        super().__init__()

        self.__controller: WindowController = WindowController(
            window=self,
            window_exit=self.window_exit,
            width=width,
            height=height
        )

        self.__event_handler: ViewEventHandler = ViewEventHandler(
            bind_call=self.bind,
            schedule_call=self.after
        )

        self.__service_broker: WindowServiceBroker = WindowServiceBroker()

        self.__publish_control_services()
        self.__publish_event_handler_services()

        self.__view_apparatus: WindowViewApparatus = WindowViewApparatus(
            window=self,
            service_call=self.service_broker
        )

        # TODO: Implement SubwindowDispatcher class for Window class

        self.__publish_view_apparatus_services()
        self.__publish_subwindow_dispatcher_services()

        # TODO: Implement ApplicationExitHandler class for Window class
        # self.__exit_prerequisites: list[ServiceEndpoint] = []

        self.__configure()

    @property
    def control(self) -> WindowController:
        return self.__controller

    @property
    def event(self) -> ViewEventHandler:
        return self.__event_handler

    @property
    def service(self) -> WindowServiceBroker:
        return self.__service_broker

    @property
    def view(self) -> WindowViewApparatus:
        return self.__view_apparatus

    def controller(self) -> WindowController:
        """ Returns window controller. """
        return self.__controller

    def view_apparatus(self) -> WindowViewApparatus:
        """ Returns window view apparatus. """
        return self.__view_apparatus

    def event_handler(self) -> ViewEventHandler:
        """ Returns window event handler. """
        return self.__event_handler

    def service_broker(self) -> WindowServiceBroker:
        return self.__service_broker

    #def add_window_exit_prerequisite(self, func, **func_args) -> None:
    #    self.__exit_prerequisites.append(ServiceEndpoint(func, **func_args))

    def window_exit(self, prereq_override: bool = False) -> None:
        if prereq_override is True:
            return self.__disassemble()

        #for prereq in self.__exit_prerequisites:
        #    prereq.execute()

        self.__disassemble()

    @staticmethod
    def is_win32_dpi_aware() -> bool:
        """ Returns true is window is aware of high DPI environment. """
        return WIN32_DPI_AWARENESS

    def __publish_control_services(self) -> None:
        """ Commit window control services to global window service endpoints.  """
        services: dict[str, any] = self.__get_controller_services_definition()

        for service_key, func in services.items():
            self.service.new(identifier=service_key, service=ServiceEndpoint(func=func))

    def __publish_event_handler_services(self) -> None:
        """ Commit window event handler services to
        global window service endpoints.  """
        services: dict[str, any] = self.__get_event_handler_services_definition()

        for service_key, func in services.items():
            self.service.new(identifier=service_key, service=ServiceEndpoint(func=func))

    def __publish_view_apparatus_services(self) -> None:
        """ Commit window view apparatus services
        to global window service endpoints.  """
        services: dict[str, any] = self.__get_view_apparatus_services_definition()

        for service_key, func in services.items():
            self.service.new(identifier=service_key, service=ServiceEndpoint(func=func))

    def __publish_subwindow_dispatcher_services(self) -> None:
        """ Commit window subwindow dispatcher services
        to global window service endpoints.  """
        services: dict[str, any] = {}

        for service_key, func in services.items():
            self.service.new(identifier=service_key, service=ServiceEndpoint(func=func))

    def __get_controller_services_definition(self) -> dict[str, any]:
        """ Returns window controller bound services. """
        return {
            CoreSvcKeys.WINDOW_WIDTH: self.control.width,
            CoreSvcKeys.WINDOW_HEIGHT: self.control.height,
            CoreSvcKeys.WINDOW_X: self.control.x_coord,
            CoreSvcKeys.WINDOW_Y: self.control.y_coord,
            CoreSvcKeys.WINDOW_COORD: self.control.coord,
            CoreSvcKeys.WINDOW_VERTICES: self.control.vertices,
            CoreSvcKeys.WINDOW_BOUNDS: self.control.bounds,
            CoreSvcKeys.WINDOW_IS_WITHIN: self.control.is_within,
            CoreSvcKeys.WINDOW_IS_PARTLY_WITHIN: self.control.is_partly_within,
            CoreSvcKeys.WINDOW_DISPLAY_OCCUP: self.control.display_occupation,
            CoreSvcKeys.WINDOW_IS_MINIMIZED: self.control.is_minimized,
            CoreSvcKeys.WINDOW_IS_FULLSCREEN: self.control.is_fullscreen,
            CoreSvcKeys.WINDOW_IS_MAXIMIZED: self.control.is_maximized,
            CoreSvcKeys.WINDOW_IS_ON_SCREEN: self.control.is_on_screen,
            CoreSvcKeys.WINDOW_IS_BORDERLESS: self.control.is_borderless,
            CoreSvcKeys.DISPLAY_NAME: self.control.display_name,
            CoreSvcKeys.DISPLAY_RESOLUTION: self.control.display_resolution,
            CoreSvcKeys.DISPLAY_ASPECT_RATIO: self.control.display_aspect_ratio,
            CoreSvcKeys.SPANNING_DISPLAYS: self.control.spanning_displays,
            CoreSvcKeys.WINDOW_REL_MOUSE_X: self.control.rel_mouse_x_coord,
            CoreSvcKeys.WINDOW_REL_MOUSE_Y: self.control.rel_mouse_y_coord,
            CoreSvcKeys.WINDOW_REL_MOUSE_COORD: self.control.rel_mouse_coord,
            CoreSvcKeys.WINDOW_HAS_MOUSE: self.control.has_mouse,
            CoreSvcKeys.SET_WINDOW_TITLE: self.control.set_title,
            CoreSvcKeys.CENTER_WINDOW: self.control.center_on_display,
            CoreSvcKeys.WINDOW_TO_DISPLAY: self.control.send_to_display,
            CoreSvcKeys.FULLSCREEN_WINDOW: self.control.enter_fullscreen,
            CoreSvcKeys.FULLSCREEN_WINDOW_EXIT: self.control.exit_fullscreen,
            CoreSvcKeys.MAXIMIZE_WINDOW: self.control.maximize,
            CoreSvcKeys.RESTORE_WINDOW: self.control.restore_down,
            CoreSvcKeys.MINIMIZE_WINDOW: self.control.minimize,
            CoreSvcKeys.WINDOW_EXIT: self.window_exit,
            CoreSvcKeys.HIDE_WINDOW: self.control.hide,
            CoreSvcKeys.SHOW_WINDOW: self.control.show,
            CoreSvcKeys.ENABLE_NATIVE_WINDOW: self.control.enable_native_controls,
            CoreSvcKeys.DISABLE_NATIVE_WINDOW: self.control.disable_native_controls,
        }

    def __get_event_handler_services_definition(self) -> dict[str, any]:
        """ Returns window event handler bound services. """
        return {
            CoreSvcKeys.WINDOW_BOUND_SEQUENCES: self.event.bound_sequences,
            CoreSvcKeys.WINDOW_FORWARD_SEQUENCES: self.event.forwarded_sequences,
            CoreSvcKeys.WINDOW_BINDINGS: self.event.bindings,
            CoreSvcKeys.WINDOW_FORWARD_BINDINGS: self.event.forwarded_bindings,
            CoreSvcKeys.WINDOW_BINDING_DEFINITION: self.event.get_binding_definition,
            CoreSvcKeys.GET_WINDOW_BINDING: self.event.get_binding,
            CoreSvcKeys.BIND_TO_WINDOW: self.event.bind,
            CoreSvcKeys.WINDOW_HAS_BINDING: self.event.is_existing_identifier,
            CoreSvcKeys.FORWARD_WINDOW_BIND: self.event.forward,
            CoreSvcKeys.SCHEDULE: self.event.schedule,
        }

    def __get_view_apparatus_services_definition(self) -> dict[str, any]:
        """ Returns window view apparatus bound services. """
        return {
            CoreSvcKeys.WINDOW_VIEW_IS_ENABLED: self.__view_apparatus.is_enabled,
            CoreSvcKeys.ENABLE_WINDOW_VIEW: self.__view_apparatus.enable_window_view,
            CoreSvcKeys.DISABLE_WINDOW_VIEW: self.__view_apparatus.disable_window_view,
            CoreSvcKeys.WINDOW_VIEWPORTS: self.__view_apparatus.view.viewports,
            CoreSvcKeys.SHOW_WINDOW_VIEWPORT: self.__view_apparatus.view.switch,
            CoreSvcKeys.GET_WINDOW_VIEWPORT: self.__view_apparatus.view.get_viewport,
            CoreSvcKeys.ATTACH_WINDOW_VIEWPORT: self.__view_apparatus.view.attach,
            CoreSvcKeys.RELEASE_WINDOW_VIEWPORT: self.__view_apparatus.view.release
        }

    def __get_subwindow_dispatcher_services_definition(self) -> dict[str, any]:
        """ Returns subwindow dispatcher bound services. """
        pass

    def __configure(self) -> None:
        """ Prepapre application window. """
        self.protocol("WM_DELETE_WINDOW", self.window_exit)

    def __disassemble(self) -> None:
        """ Destroy application window. """
        self.destroy()

    def __key(self) -> int:
        return self.__hash__() + self.winfo_id()
