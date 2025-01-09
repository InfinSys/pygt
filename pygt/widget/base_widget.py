
""" Base PyGT Widget Class """


#   EXTERNAL IMPORTS
from tkinter import Widget
from customtkinter import CTkFrame
from pygt.widget.utility.widget_manager import WidgetManager


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
DEFAULT_WIDGET_WIDTH: int = 1
DEFAULT_WIDGET_HEIGHT: int = 1


#   CLASSES
class PyGTWidget(CTkFrame):
    """ Base Python GUI toolkit widget class. """
    def __init__(self, master: Widget, **kwargs) -> None:
        self.__foreground_clr: str = kwargs.get('fg', None)
        self.__background_clr: str = kwargs.get('bg', "transparent")
        self.__corner_background_clr: str = kwargs.get('corner_bg', None)
        self.__border_clr: str = kwargs.get('border_fg', None)
        self.__border_width: int = kwargs.get('border', 0)
        self.__corner_radius: int = kwargs.get('corner_radius', 0)

        super().__init__(
            master=master,
            width=kwargs.get('width', DEFAULT_WIDGET_WIDTH),
            height=kwargs.get('height', DEFAULT_WIDGET_HEIGHT),
            corner_radius=self.__corner_radius,
            border_width=self.__border_width,
            bg_color=self.__background_clr,
            fg_color=self.__foreground_clr,
            border_color=self.__border_clr,
            background_corner_colors=self.__corner_background_clr,
            overwrite_preferred_drawing_method=None
        )

        self.__child_manager: WidgetManager = WidgetManager()

        self.pack_propagate(flag=kwargs.get('propogate', False))
        self.grid_propagate(flag=kwargs.get('propogate', False))

    @property
    def interface(self) -> WidgetManager:
        """ Widget child manager. """
        return self.__child_manager

    def foreground_color(self) -> str:
        """ Returns widget foreground color. """
        return self.__foreground_clr

    def background_color(self) -> str:
        """ Returns widget background color. """
        return self.__background_clr

    def is_multi_corner_backgrounds(self) -> bool:
        """ Returns true if widget corners have different background colors. """
        return type(self.__corner_background_clr) is tuple

    def corner_background_color(self) -> str:
        """ Returns widget corner background color(s). """
        return self.__corner_background_clr

    def border_color(self) -> str:
        """ Returns widget border color. """
        return self.__border_clr

    def border_width(self) -> int:
        """ Returns widget border width. """
        return self.__border_width

    def corner_radius(self) -> int:
        """ Returns widget corner radius. """
        return self.__corner_radius

    def width(self) -> int:
        """ Returns widget width. """
        return self.winfo_width()

    def height(self) -> int:
        """ Returns widget height. """
        return self.winfo_height()

    def size(self) -> tuple[int, int]:
        """ Returns widget size as tuple. """
        return self.winfo_width(), self.winfo_height()

    def set_foreground_color(self, color: str) -> None:
        """ Set widget foreground color. """
        self.__foreground_clr = color
        self.configure(fg_color=color, require_redraw=True)

    def set_background_color(self, color: str) -> None:
        """ Set widget background color. """
        self.__background_clr = color
        self.configure(bg_color=color, require_redraw=True)

    def set_corner_background_color(self, color: str) -> None:
        """ Set widget corner background color. """
        self.__corner_background_clr = color
        self.configure(background_corner_colors=color, require_redraw=True)

    def set_border_color(self, color: str) -> None:
        """ Set widget border color. """
        self.__border_clr = color
        self.configure(border_color=color, require_redraw=True)

    def set_border_width(self, width: int) -> None:
        """ Set widget border width. """
        self.__border_width = width
        self.configure(border_width=width, require_redraw=True)

    def set_corner_radius(self, radius: int) -> None:
        """ Set widget corner radius. """
        self.__corner_radius = radius
        self.configure(border_width=radius, require_redraw=True)

    def set_size(self, width: int, height: int) -> None:
        """ Set widget size as tuple. """
        self.configure(width=width, height=height, require_redraw=True)

    def set_width(self, width: int) -> None:
        """ Set widget width. """
        self.configure(width=width, require_redraw=True)

    def set_height(self, height: int) -> None:
        """ Set widget height. """
        self.configure(height=height, require_redraw=True)

    def command_on_event(self, sequence: str, command, child: str = None, **kwargs) -> None:
        """ Bind command on specified event to
        entire widget or specified child widget. """
        if (child is not None) and (self.interface.is_existing_widget(child)):
            try:
                self.interface.get(child).bind(sequence=sequence, func=command, **kwargs)
            except Exception:
                self.interface.get(child).bind(sequence=sequence, command=command, **kwargs)
        elif child is None:
            self.bind(sequence=sequence, command=command, add=kwargs.get('add', None))
