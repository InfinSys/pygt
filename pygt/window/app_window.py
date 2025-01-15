
""" Base Application Window Instance """


#   EXTERNAL IMPORTS
from tkinter import Tk


#   INTERNAL IMPORTS
from .subwindow_dispatcher import SubwindowDispatcher
from pygt.window.controller import WindowController
from pygt.event.handler import ViewEventHandler, ExitHandler
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
class Window(Tk):
    """ Base main application window class. """
    def __init__(self, width: int = None, height: int = None) -> None:
        super().__init__()

        self.__controller: WindowController = WindowController(
            window=self,
            width=width,
            height=height,
            window_exit_call=self.window_exit
        )

        self.__event_handler: ViewEventHandler = ViewEventHandler(
            bind_call=self.bind,
            unbind_call=self.unbind,
            schedule_call=self.after
        )

        self.__service_broker: WindowServiceBroker = WindowServiceBroker()

        self.__publish_control_services()
        self.__publish_event_handler_services()

        self.__view_apparatus: WindowViewApparatus = WindowViewApparatus(
            window=self,
            service_call=self.service_broker
        )

        self.__subwindow_dispatcher: SubwindowDispatcher = SubwindowDispatcher(
            window=self,
            service_call=self.service_broker
        )

        # TODO: Implement WindowThreadManager class for Window class

        self.__publish_view_apparatus_services()
        self.__publish_subwindow_dispatcher_services()

        self.__exit_handler: ExitHandler = ExitHandler(
            final_call=self.destroy,
            post_exit_call=exit
        )

        self.__publish_window_exit_handler_services()
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
        return self.__service_broker

    @property
    def view(self) -> WindowViewApparatus:
        """ Window view apparatus. """
        return self.__view_apparatus

    @property
    def window(self) -> SubwindowDispatcher:
        """ Window subwindow dispatcher. """
        return self.__subwindow_dispatcher

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

    def service_broker(self) -> WindowServiceBroker:
        """ Returns window services broker. """
        return self.__service_broker

    def subwindow_dispatcher(self) -> SubwindowDispatcher:
        """ Returns window subwindow dispatcher. """
        return self.__subwindow_dispatcher

    def launch_mainloop(self) -> int:
        """ Start application mainloop. """
        try:
            self.mainloop()
        except Exception as e:
            print(f"Application failure - {e}")
            return 1

        return 0

    def window_exit(self, prereq_override: bool = False, exit_status: int = None) -> None:
        """ Inititate window exit sequence. """
        if (prereq_override is True) and (exit_status is None):
            return self.__exit_handler.post_exit(
                code=self.__exit_handler.do_forceful_exit()
            )
        elif (prereq_override is False) and (exit_status is None):
            return self.__exit_handler.post_exit(
                code=self.__exit_handler.do_graceful_exit()
            )
        elif prereq_override is True:
            self.__exit_handler.do_forceful_exit()
            return self.__exit_handler.post_exit(code=exit_status)
        else:
            self.__exit_handler.do_graceful_exit()
            return self.__exit_handler.post_exit(code=exit_status)

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
        services: dict[str, any] = self.__get_subwindow_dispatcher_services_definition()

        for service_key, func in services.items():
            self.service.new(identifier=service_key, service=ServiceEndpoint(func=func))

    def __publish_window_exit_handler_services(self) -> None:
        """ Commit window exit handler services to global
         window service endpoints. """
        services: dict[str, any] = self.__get_window_exit_handler_services_definition()

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
            CoreSvcKeys.WINDOW_IS_X_RESIZABLE: self.control.is_horizontally_resizable,
            CoreSvcKeys.WINDOW_IS_Y_RESIZABLE: self.control.is_vertically_resizable,
            CoreSvcKeys.WINDOW_IS_MINIMIZED: self.control.is_minimized,
            CoreSvcKeys.WINDOW_IS_FULLSCREEN: self.control.is_fullscreen,
            CoreSvcKeys.WINDOW_IS_ALWAYS_TOPMOST: self.control.is_always_topmost,
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
            CoreSvcKeys.SET_WINDOW_RESIZABILITY: self.control.set_resizability,
            CoreSvcKeys.TOGGLE_WINDOW_RESIZABILITY: self.control.toggle_resizability,
            CoreSvcKeys.CENTER_WINDOW: self.control.center_on_display,
            CoreSvcKeys.WINDOW_TO_DISPLAY: self.control.send_to_display,
            CoreSvcKeys.ENABLE_ALWAYS_TOPMOST_WINDOW: self.control.enable_always_on_top,
            CoreSvcKeys.DISABLE_ALWAYS_TOPMOST_WINDOW: self.control.disable_always_on_top,
            CoreSvcKeys.WINDOW_TO_FOREGROUND: self.control.bring_to_foreground,
            CoreSvcKeys.WINDOW_TO_BACKGROUND: self.control.send_to_background,
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
            CoreSvcKeys.UNBIND_WINDOW_EVENT: self.event.unbind,
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
        return {
            CoreSvcKeys.WINDOW_SUBWINDOWS: self.window.subwindows,
            CoreSvcKeys.GET_WINDOW_SUBWINDOW: self.window.get_subwindow,
            CoreSvcKeys.SUBWINDOW_DISPATCH: self.window.dispatch,
            CoreSvcKeys.SUBWINDOW_CLOSE: self.window.close,
        }

    def __get_window_exit_handler_services_definition(self) -> dict[str, any]:
        """ Returns window exit handler bound services. """
        return {
            CoreSvcKeys.ADD_WINDOW_EXIT_PREREQ: self.exit.add_exit_prerequisite,
            CoreSvcKeys.REMOVE_WINDOW_EXIT_PREREQ: self.exit.remove_exit_prerequisite,
        }

    def __configure(self) -> None:
        """ Prepapre application window. """
        self.protocol("WM_DELETE_WINDOW", self.window_exit)

    def __key(self) -> int:
        return self.__hash__() + self.winfo_id()
