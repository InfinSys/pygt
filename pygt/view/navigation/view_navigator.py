
""" Base Application Window View Navigator """


#   EXTERNAL IMPORTS
from abc import ABC, abstractmethod


#   INTERNAL IMPORTS
from pygt.view.navigation.utility.view_context import ViewContext
from pygt.widget.utility.widget_manager import WidgetManager


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ViewNavigator(ABC):
    """ Base application view navigator. """
    def __init__(self, default_view_args: dict[str, any], widget_manager: WidgetManager, proxy_type: type = None) -> None:
        self.__default_view_args: dict[str, any] = default_view_args
        self.__view_widget_manager: WidgetManager = widget_manager
        self.__views: dict[str, ViewContext] = {}
        self.__current_view: str = None
        self.__pack_args: dict[str, any] = {
            'expand': True,
        }

        if proxy_type is not None:
            self.__configure_control_proxy(proxy_type)

    @property
    def widget(self) -> WidgetManager:
        """ View navigator widget manager. """
        return self.__view_widget_manager

    def views(self) -> list[str]:
        """ Returns list of view identifiers. """
        return [identifier for identifier in self.__views.keys()]

    def view_structure(self) -> dict[str, ViewContext]:
        """ Returns underlying view data structure. """
        return self.__views

    def current_view(self) -> str:
        """ Returns identifier of current view. """
        return self.__current_view

    def is_existing_view(self, identifier: str) -> bool:
        """ Returns true if a view context exist
        for provided identifier. """
        return identifier in self.__views.keys()

    def view_pack_args(self) -> dict[str, any]:
        """ Returns view packing arguments. """
        return self.__pack_args

    def view_widget_manager(self) -> WidgetManager:
        """ Returns view widget manager. """
        return self.__view_widget_manager

    def get_view_context(self, identifier: str) -> ViewContext:
        """ Returns context of requested view. """
        if not self.is_existing_view(identifier):
            return None

        return self.__views[identifier]

    def get_current_context(self) -> ViewContext:
        """ Returns context of current view. """
        if self.__current_view is None:
            return None

        return self.__views[self.__current_view]

    def set_pack_args(self, **pack_args) -> None:
        """ Add or update arguments in view packing process. """
        self.__pack_args.update(pack_args)

    def remove_pack_args(self, *args) -> None:
        """ Remove arguments from view packing process. """
        for arg_key in args:
            self.__pack_args.pop(str(arg_key), None)

    def update_view_info(self, **view_info) -> None:
        """ Update view navigation information. """
        current_view: str = view_info.pop('current', self.__current_view)
        self.__current_view = current_view

    @abstractmethod
    def switch(self, view_id: str) -> bool:
        """ Switch to requested view. """
        pass

    def attach(self, view_type: type, context_type: type, view_arg: str, identifier: str, **view_init_args) -> bool:
        """ Include new view in this view. """
        if self.is_existing_view(identifier):
            return False

        load: bool = view_init_args.pop('load', True)
        restrict: bool = view_init_args.pop('restrict', False)
        condition = view_init_args.pop('condition', None)
        show: bool = view_init_args.pop('show', False)
        restrict = restrict if type(restrict) is bool else False
        condition = condition if callable(condition) else None
        show = show if restrict is False else False

        view_init_args.update(self.__default_view_args)

        if load:
            context_init_args: dict[str, any] = {
                f"{view_arg}": view_type(**view_init_args),
                f"{view_arg}_id": identifier,
                "view_type": view_type,
                'restrict': restrict,
                'condition': condition
            }
        else:
            context_init_args: dict[str, any] = {
                f"{view_arg}": None,
                f"{view_arg}_id": identifier,
                "view_type": view_type,
                "init_args": view_init_args,
                "restrict": restrict,
                "condition": condition
            }

        self.__views[identifier] = context_type(**context_init_args)
        self.__view_widget_manager.new(
            identifier=f"{identifier}_{view_arg}",
            widget=self.get_view_context(identifier).view()
        )

        if show:
            self.switch(identifier)

        return True

    def release(self, view_arg: str, identifier: str) -> bool:
        """ Remove view from this view. """
        if not self.is_existing_view(identifier):
            return False

        if not self.__view_widget_manager.remove(identifier=f"{identifier}_{view_arg}"):
            return False

        del self.__views[identifier]
        return True

    def __configure_control_proxy(self, proxy_type: type) -> None:
        """ Setup navigator control proxy for encompassing views. """
        self.__default_view_args.update(
            {
                'control_proxy': proxy_type(
                    navigator=self
                )
            }
        )
