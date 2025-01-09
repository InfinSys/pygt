
""" Basic Text Label Widget """


#   EXTERNAL IMPORTS
from .label_widget_model import LabelModel
from pygt.widget.base_widget import PyGTWidget
from tkinter import Widget, Label


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
DEFAULT_FONT: tuple[str, int, str] = ("Arial", 9, "normal")
DEFAULT_FONT_COLOR: str = "#000000"
DEFAULT_BACKGROUND_COLOR: str = "#ffffff"


#   CLASSES
class TextLabel(PyGTWidget, LabelModel):
    """ Basic text label. """
    def __init__(self, master: Widget, text: str, **kwargs) -> None:
        self.__text_font: tuple = kwargs.pop('font', DEFAULT_FONT)
        self.__font_clr: str = kwargs.pop('font_fg', DEFAULT_FONT_COLOR)
        self.__text_anchor: str = kwargs.pop('anchor', "center")

        PyGTWidget.__init__(
            self=self,
            master=master,
            width=kwargs.pop('width', 1),
            height=kwargs.pop('height', 1),
            fg=kwargs.pop('bg', DEFAULT_BACKGROUND_COLOR),
            propogate=kwargs.pop('propogate', True),
            border=kwargs.pop('border', 0),
            border_fg=kwargs.pop('border_fg', None),
            **kwargs
        )

        LabelModel.__init__(self=self, text=text)

        self.interface.new(
            identifier="text_label",
            widget=Label(
                master=self,
                textvariable=self.text_variable(),
                font=self.__text_font,
                anchor=self.__text_anchor,
                bg=self.foreground_color(),
                fg=self.__font_clr
            )
        )
        self.interface.pack(
            identifier="text_label",
            expand=True
        )

    def text_font(self) -> tuple:
        """ Returns label text font. """
        return self.__text_font

    def font_color(self) -> str:
        """ Returns font color. """
        return self.__font_clr

    def get_label(self) -> Label:
        """ Returns underlying label widget. """
        return self.interface.get(identifier="text_label")

    def set_text_font(self, font: tuple) -> None:
        """ Set label text font. """
        self.__text_font = font
        self.get_label().config(font=font)

    def set_font_color(self, color: str) -> None:
        """ Set label font color. """
        self.__font_clr = color
        self.get_label().config(fg=color)
