
""" Application Window View Apparatus """


#   EXTERNAL IMPORTS
from tkinter import Tk, Frame


#   INTERNAL IMPORTS
from view import Viewport
from view.view_controller import ViewController


class WindowViewApparatus:
    def __init__(self, window: Tk, service) -> None:
        self.__tk: Tk = window if issubclass(type(window), Tk) else None
        self.__service_call = service if callable(service) else None
        self.__viewports: dict[str, tuple[bool, Viewport]] = {}
        self.__current_viewport: str = None
        self.__root_view: Frame = Frame(self.__tk)
        self.__view_enabled: bool = True
        self.__pack_args: dict = {
            'expand': True,
        }

        self.__controller: ViewController = ViewController(
            view=self.__root_view,
            service=service,
            parent=None
        )

        self.__configure_root_view()

    @property
    def control(self) -> ViewController:
        return self.__controller

    def top_level(self) -> Tk:
        return self.__tk

    def set_background(self, color: str) -> None:
        self.__root_view.config(bg=color)

    def is_enabled(self) -> bool:
        return self.__view_enabled

    def enable_view(self) -> None:
        if self.__view_enabled is True:
            return

        self.__configure_root_view()
        self.__view_enabled = True

    def disable_view(self) -> None:
        if self.__view_enabled is False:
            return

        self.__root_view.pack_forget()
        self.__view_enabled = False

    def viewports(self, **kwargs) -> list[str]:
        if kwargs.get('key', 0) == self.__owner_hash:
            return [view_id for view_id in self.__viewports.keys()]

        return [view_id for view_id in self.__viewports.keys() if self.__viewports[view_id][0] is False]

    def show_viewport(self, view_id: str) -> bool:
        if (self.__current_viewport is not None) and (view_id == self.__current_viewport):
            return True

        if not self.__is_existing_viewport_id(view_id):
            return False

        if self.__viewports[view_id][0] is True:
            return False

        if self.__current_viewport is not None:
            self.__viewports[self.__current_viewport][1].pack_forget()

        self.__current_viewport = view_id
        self.__viewports[view_id][1].pack(**self.__pack_args)

    def get_viewport(self, view_id: str, **kwargs) -> Viewport:
        if not self.__is_existing_viewport_id(view_id):
            return None

        if (self.__viewports[view_id][0] is True) and (kwargs.get('key', 0) != self.__owner_hash):
            return None

        return self.__viewports[view_id][1]

    def include_viewport(self, view_id: str, viewport_type: type, **viewport_args) -> bool:
        if self.__is_existing_viewport_id(view_id):
            return False

        secure: bool = False
        show: bool = False

        if viewport_args.get('secure') is not None:
            secure = viewport_args.get('secure') if type(viewport_args.get('secure')) is bool else False
            viewport_args.pop('secure')

        if viewport_args.get('show') is not None:
            show = viewport_args.get('show') if type(viewport_args.get('show')) is bool else False
            viewport_args.pop('show')

        self.__viewports[view_id] = (
            secure,
            viewport_type(
                master=self.__root_view,
                service=self.__service_call,
                **viewport_args
            )
        )

        if (show is True) and (secure is False):
            self.show_viewport(view_id)

        return True

    def set_pack_args(self, **pack_args) -> None:
        self.__pack_args = pack_args

    def release_viewport(self, view_id: str, key: int) -> bool:
        if not self.__is_existing_viewport_id(view_id):
            return False

        if key != self.__owner_hash:
            return False

        temp: Viewport = self.__viewports[view_id][1]
        self.__viewports[view_id] = (False, temp)

    def __configure_root_view(self) -> None:
        self.__root_view.pack_propagate(False)
        self.__root_view.pack(fill="both", expand=True)

    def __is_existing_viewport_id(self, view_id: str) -> bool:
        return view_id in [v_id for v_id in self.__viewports.keys()]
