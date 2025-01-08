
""" Application Window Viewport Navigator """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
from .view_navigator import ViewNavigator
from pygt.view import Viewport
from pygt.view.navigation.utility.viewport_context import ViewportContext


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ViewportNavigator(ViewNavigator):
    """ Window viewport navigator. """
    def __init__(self, default_viewport_args: dict[str, any]) -> None:
        super().__init__(default_view_args=default_viewport_args)

    def viewports(self) -> list[str]:
        """ Returns list of viewport identifiers. """
        return self.views()

    def current_viewport(self) -> str:
        """ Returns identifier of current viewport. """
        return self.current_view()

    def is_existing_viewport(self, identifier: str) -> bool:
        """ Returns true if a viewport context exist
        for provided identifier. """
        return self.is_existing_view(identifier)

    def viewport_pack_args(self) -> dict[str, any]:
        """ Returns viewport placement packing arguments. """
        return self.view_pack_args()

    def get_viewport_context(self, identifier: str) -> ViewportContext:
        """ Returns context of requested viewport. """
        return self.get_view_context(identifier)

    def get_current_context(self) -> ViewportContext:
        """ Returns context of current viewport. """
        return super().get_current_context()

    def get_viewport(self, identifier: str) -> Viewport:
        """ Returns requested viewport instance. """
        if not self.is_existing_view(identifier):
            return None

        return self.get_viewport_context(identifier).viewport()

    def get_viewports(self, *viewport_ids) -> list[Viewport]:
        """ Returns requested viewport instances or
        all if no identifiers specified. """
        requested: list[Viewport] = []

        for identifier, viewport_context in self.view_structure().items():
            if not viewport_context.is_restricted():
                if (viewport_ids and (identifier in viewport_ids)) or (not viewport_ids):
                    requested.append(viewport_context.view())

        return requested

    def get_current_viewport(self) -> Viewport:
        """ Returns current viewport instance. """
        return self.get_current_context().viewport()

    def switch(self, viewport_id: str) -> bool:
        """ Switch to requested view. """
        if not self.is_existing_view(viewport_id):
            return False

        if self.get_view_context(viewport_id).is_restricted():
            return False

        if self.current_view() is not None:
            self.get_current_viewport().pack_forget()

        self.get_viewport_context(viewport_id).show(**self.view_pack_args())
        self.update_view_info(current=viewport_id)
        return True

    def attach(self, identifier: str, viewport_type: type, **init_args) -> bool:
        """ Include new viewport in view. """
        return super().attach(
            view_type=viewport_type,
            context_type=ViewportContext,
            view_arg="viewport",
            identifier=identifier,
            **init_args
        )
