
""" Window Viewport Page Context """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
from pygt.view import Page
from .view_context import ViewContext


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class PageContext(ViewContext):
    """ Viewport page context. """
    def __init__(self, page: Page, restrict: bool = False, **kwargs) -> None:
        super().__init__(
            view_type=Page,
            view=page,
            restrict=restrict,
            **kwargs
        )

    def page(self) -> Page:
        """ Returns underlying page instance. """
        return self.view()
