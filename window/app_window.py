
""" Base Application Window """


#   EXTERNAL IMPORTS
import tkinter as tk


#   INTERNAL IMPORTS
from window.window_controller import WindowController
from window.window_event import WindowEventHandler
from window.window_service import WindowServiceBroker, WindowService
#from window.window_view import WindowViewApparatus
import window.window_service.service_keys as SvcKey


# Application DPI awareness
try:
    # Windows Platform
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

except Exception as e:
    print(f"Failed to enable DPI awareness:\n{e}")


class AppWindow(tk.Tk):
    def __init__(self, width: int = None, height: int = None) -> None:
        super().__init__()

        self.__controller: WindowController = WindowController(
            window=self,
            window_exit=self.window_exit,
            width=width,
            height=height
        )

        self.__event_handler: WindowEventHandler = WindowEventHandler(
            bind_func=self.bind,
            schedule_func=self.after
        )

        self.__service_broker: WindowServiceBroker = WindowServiceBroker(
            instance_hash=self.__key()
        )

        self.__publish_control_services()
        self.__publish_event_services()

        #self.__view_apparatus: WindowViewApparatus = WindowViewApparatus(
        #    window=self,
        #    instance_hash=self.__key(),
        #    service=self.service_broker
        #)

        self.__exit_prerequisites: list[WindowService] = []

        #self.__publish_view_services()
        self.__configure()

    @property
    def control(self) -> WindowController:
        return self.__controller

    @property
    def event(self) -> WindowEventHandler:
        return self.__event_handler

    @property
    def service(self) -> WindowServiceBroker:
        return self.__service_broker

    #@property
    #def view(self) -> WindowViewApparatus:
    #    return self.__view_apparatus

    def service_broker(self) -> WindowServiceBroker:
        return self.__service_broker

    def add_window_exit_prerequisite(self, func, **func_args) -> None:
        self.__exit_prerequisites.append(WindowService(func, **func_args))

    def window_exit(self, prereq_override: bool = False) -> None:
        if prereq_override is False:
            for prereq in self.__exit_prerequisites:
                prereq.execute()

        self.destroy()

    def __configure(self) -> None:
        self.protocol("WM_DELETE_WINDOW", self.window_exit)

    def __publish_control_services(self) -> None:
        services: dict[str, any] = {
            SvcKey.WINDOW_WIDTH: self.control.width,
            SvcKey.WINDOW_HEIGHT: self.control.height,
            SvcKey.WINDOW_X: self.control.x_coord,
            SvcKey.WINDOW_Y: self.control.y_coord,
            SvcKey.WINDOW_BOUNDS: self.control.bounds,
            SvcKey.WINDOW_BBOX: self.control.bounds_box,
            SvcKey.WINDOW_IS_WITHIN: self.control.is_within,
            SvcKey.WINDOW_IS_PARTLY_WITHIN: self.control.is_partially_within,
            SvcKey.WINDOW_IS_MINIMIZED: self.control.is_minimized,
            SvcKey.WINDOW_IS_MAXIMIZED: self.control.is_maximized,
            SvcKey.WINDOW_IS_ON_SCREEN: self.control.is_on_screen,
            SvcKey.DISPLAY_NAME: self.control.display_name,
            SvcKey.DISPLAY_RESOLUTION: self.control.display_resolution,
            SvcKey.SPANNING_DISPLAYS: self.control.spanning_displays,
            SvcKey.WINDOW_IS_BORDERLESS: self.control.is_borderless,
            SvcKey.WINDOW_REL_MOUSE_X: self.control.rel_mouse_x_coord,
            SvcKey.WINDOW_REL_MOUSE_Y: self.control.rel_mouse_y_coord,
            SvcKey.WINDOW_HAS_MOUSE: self.control.has_mouse,
            SvcKey.SET_WINDOW_TITLE: self.control.set_title,
            SvcKey.CENTER_WINDOW: self.control.center_on_display,
            SvcKey.MAXIMIZE_WINDOW: self.control.maximize,
            SvcKey.RESTORE_WINDOW: self.control.restore_down,
            SvcKey.MINIMIZE_WINDOW: self.control.minimize,
            SvcKey.HIDE_WINDOW: self.control.hide,
            SvcKey.SHOW_WINDOW: self.control.show,
            SvcKey.ENABLE_NATIVE_WINDOW: self.control.enable_native_controls,
            SvcKey.DISABLE_NATIVE_WINDOW: self.control.disable_native_controls,
        }

        for service, func in services.items():
            self.service.new_service(name=service, service=WindowService(func=func))

    def __publish_event_services(self) -> None:
        services: dict[str, any] = {
            SvcKey.BIND_TO_WINDOW: self.event.bind,
            SvcKey.FORWARD_WINDOW_BIND: self.event.forward_binding,
            SvcKey.SCHEDULE: self.event.schedule
        }

        for service, func in services.items():
            self.service.new_service(name=service, service=WindowService(func=func))

    def __publish_view_services(self) -> None:
        services: dict[str, any] = {
            SvcKey.WINDOW_VIEW_IS_ENABLED: self.view.is_enabled,
            SvcKey.ENABLE_WINDOW_VIEW: self.view.enable_view,
            SvcKey.DISABLE_WINDOW_VIEW: self.view.disable_view,
            SvcKey.WINDOW_VIEWPORTS: self.view.viewports,
            SvcKey.SHOW_WINDOW_VIEWPORT: self.view.show_viewport,
            SvcKey.GET_WINDOW_VIEWPORT: self.view.get_viewport,
            SvcKey.NEW_WINDOW_VIEWPORT: self.view.include_viewport
        }

        for service, func in services.items():
            self.service.new_service(name=service, service=WindowService(func=func))

    def __key(self) -> int:
        return self.__hash__() + self.winfo_id()
