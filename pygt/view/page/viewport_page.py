
""" Base Window Viewport Page """


#   EXTERNAL IMPORTS
from tkinter import Frame


#   INTERNAL IMPORTS
from pygt.view.view_interface import ViewInterface
from pygt.widget.utility.widget_container import WidgetContainer
from pygt.widget.utility.viewport_proxy import ViewportProxy


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class Page(ViewInterface):
    """ Base window viewport page. """
    def __init__(self, viewport: Frame, control_proxy: ViewportProxy, service_call) -> None:
        super().__init__(parent=viewport, service_call=service_call)

        self.__viewport_proxy: ViewportProxy = control_proxy
        pass

    @property
    def host(self) -> ViewportProxy:
        """ Page viewport proxy. """
        return self.__viewport_proxy
