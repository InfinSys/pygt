
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
    def __init__(self, page: Page, page_id: str, restrict: bool = False, **kwargs) -> None:
        super().__init__(
            view_type=Page,
            view=page,
            view_id=page_id,
            restrict=restrict,
            **kwargs
        )

    def page(self) -> Page:
        """ Returns underlying page instance. """
        return self.view()
