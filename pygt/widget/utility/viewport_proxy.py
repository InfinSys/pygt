
""" Window Viewport Proxy """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ViewportProxy:
    """ Window viewport proxy. """
    def __init__(self, page_navigator) -> None:
        self.__navigator = page_navigator

    def pages(self) -> list[str]:
        """ Returns list of page identifiers. """
        return self.__navigator.pages()

    def current_page(self) -> str:
        """ Returns identifier of current viewport page. """
        return self.__navigator.current_page()

    def attach(self, identifier: str, page_type: type, **init_args) -> bool:
        """ Include new page in viewport. """
        return self.__navigator.attach(identifier=identifier, page_type=page_type, **init_args)

    def switch(self, page_id: str) -> bool:
        """ Switch to requested page in viewport. """
        return self.__navigator.switch(page_id=page_id)
