
""" Application Viewport Context """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
from pygt.view import Viewport
from .view_context import ViewContext


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ViewportContext(ViewContext):
    """ Application viewport context. """
    def __init__(self, viewport: Viewport, restrict: bool = False, **kwargs) -> None:
        super().__init__(
            view_type=Viewport,
            view=viewport,
            restrict=restrict,
            **kwargs
        )

    def viewport(self) -> Viewport:
        """ Returns underlying viewport instance. """
        return self.view()
