
""" Base Application Window View Context """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
from pygt.view.view_interface import ViewInterface
from pygt.widget.utility.widget_manager import WidgetManager


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ViewContext:
    """ Base application view context. """
    def __init__(self, view_type: type, view: ViewInterface, view_id: str, restrict: bool = False, **kwargs) -> None:
        self.__view_type: type = view_type
        self.__view_identifier: str = view_id
        self.__view_init_args: dict[str, any] = kwargs.get('init_args', {})
        self.__restrict_conditional: any = kwargs.get('condition', None)
        self.__restrict_view: bool = restrict if self.__restrict_conditional is not None else False
        self.__view: ViewInterface = view if issubclass(type(view), ViewInterface) else None

    def is_restricted(self) -> bool:
        """ Returns true is view is currently restricted. """
        if self.__restrict_view and (not self.__has_clearance()):
            return True

        self.__restrict_view = False
        return False

    def is_loaded(self) -> bool:
        """ Returns true if view is currently in memory. """
        return self.__view is not None

    def view_type(self) -> type:
        """ Returns this views specific type. """
        return self.__view_type

    def show(self, widget_manager: WidgetManager, view_arg: str, **pack_args) -> bool:
        """ Show view. """
        if self.is_restricted():
            return False

        if not self.is_loaded():
            self.load(widget_manager, view_arg)

        widget_manager.pack(
            identifier=f"{self.__view_identifier}_{view_arg}",
            **pack_args
        )
        return True

    def load(self, widget_manager: WidgetManager, view_arg: str) -> ViewInterface:
        self.__view = self.__view_type(**self.__view_init_args)
        widget_manager.update(
            identifier=f"{self.__view_identifier}_{view_arg}",
            widget=self.__view
        )
        return self.__view

    def view(self) -> ViewInterface:
        """ Returns underlying view instance. """
        if self.is_restricted() or (not self.is_loaded()):
            return None

        return self.__view

    def __has_clearance(self) -> bool:
        """ Returns true if application has clearance to view. """
        if not self.__restrict_view:
            return True

        return self.__restrict_conditional()
