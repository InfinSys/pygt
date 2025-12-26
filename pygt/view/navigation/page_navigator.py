
""" Window Viewport Page Navigator """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
from .view_navigator import ViewNavigator
from pygt.view import Page
from pygt.view.navigation.utility.page_context import PageContext
from pygt.view.utility.viewport_proxy import ViewportProxy
from pygt.widget.utility.widget_manager import WidgetManager


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class PageNavigator(ViewNavigator):
    """ Viewport page navigator. """
    def __init__(self, default_page_args: dict[str, any], widget_manager: WidgetManager) -> None:
        super().__init__(
            default_view_args=default_page_args,
            widget_manager=widget_manager,
            proxy_type=ViewportProxy
        )

    def pages(self) -> list[str]:
        """ Returns list of page identifiers. """
        return self.views()

    def current_page(self) -> str:
        """ Returns identifier of current viewport page. """
        return self.current_view()

    def is_existing_page(self, identifier: str) -> bool:
        """ Returns true if a page context exist
        for provided identifier. """
        return self.is_existing_view(identifier)

    def page_pack_args(self) -> dict[str, any]:
        """ Returns viewport page packing arguments. """
        return self.view_pack_args()

    def get_page_context(self, identifier: str) -> PageContext:
        """ Returns context of requested page. """
        return self.get_view_context(identifier)

    def get_current_context(self) -> PageContext:
        """ Returns context of current viewport page. """
        return super().get_current_context()

    def get_page(self, identifier: str) -> Page:
        """ Returns requested page instance. """
        if not self.is_existing_view(identifier):
            return None

        return self.get_page_context(identifier).page()

    def get_pages(self, *page_ids) -> list[Page]:
        """ Returns requested page instances or
        all if no identifiers specified. """
        requested: list[Page] = []

        for identifier, page_context in self.view_structure().items():
            if not page_context.is_restricted():
                if (page_ids and (identifier in page_ids)) or (not page_ids):
                    requested.append(page_context.view())

        return requested

    def get_current_page(self) -> Page:
        """ Returns current viewport page instance. """
        return self.get_current_context().page()

    def switch(self, page_id: str) -> bool:
        """ Switch to requested page in viewport. """
        if not self.is_existing_view(page_id):
            return False

        if self.get_view_context(page_id).is_restricted():
            return False

        if self.current_view() is not None:
            self.get_current_page().pack_forget()

        self.get_page_context(page_id).show(
            widget_manager=self.view_widget_manager(),
            view_arg="page",
            **self.view_pack_args()
        )
        self.update_view_info(current=page_id)
        return True
    
    def load_page(self, identifier: str) -> bool:
        """ Construct specified page into memory. """
        pg_ctx_ref: PageContext = self.get_view_context(identifier)
        pg_ctx_ref.load(
            widget_manager=self.view_widget_manager(),
            view_arg="page"
        )

    def attach(self, identifier: str, page_type: type, **init_args) -> bool:
        """ Include new page in viewport. """
        return super().attach(
            view_type=page_type,
            context_type=PageContext,
            view_arg="page",
            identifier=identifier,
            **init_args
        )

    def release_page(self, identifier: str) -> bool:
        """ Remove page from viewport. """
        return self.release(
            view_arg="page",
            identifier=identifier
        )
