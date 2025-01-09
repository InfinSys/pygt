
""" Flat Button Widget """


#   EXTERNAL IMPORTS
from .button_widget_model import ButtonModel
from pygt.widget.base_widget import PyGTWidget
from tkinter import Widget, Label, Event


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
DEFAULT_WIDTH: int = 70
DEFAULT_HEIGHT: int = 30
DEFAULT_CORNER_RADIUS: int = 4
DEFAULT_FONT: tuple[str, int, str] = ("Arial", 9, "normal")
DEFAULT_FONT_COLOR: str = "#000000"


#   CLASSES
class FlatButton(PyGTWidget, ButtonModel):
    """ Flat button. """
    def __init__(self, master: Widget, text: str, **kwargs) -> None:
        PyGTWidget.__init__(
            self=self,
            master=master,
            width=kwargs.get('width', DEFAULT_WIDTH),
            height=kwargs.get('height', DEFAULT_HEIGHT),
            corner_radius=kwargs.get('corner_radius', DEFAULT_CORNER_RADIUS),
            fg=kwargs.get('bg', None)
        )

        ButtonModel.__init__(
            self=self,
            text=text,
            primary_call=kwargs.get('primary_cmd', None),
            secondary_call=kwargs.get('secondary_cmd', None)
        )

        self.__hover_background_clr: str = kwargs.get('hover_bg', None)
        self.__hover_foreground_clr: str = kwargs.get('hover_fg', None)
        self.__font_clr: str = kwargs.get('font_fg', DEFAULT_FONT_COLOR)

        self.interface.new(
            identifier="text_label",
            widget=Label(
                master=self,
                textvariable=self.text_variable(),
                font=kwargs.get('font', DEFAULT_FONT),
                anchor="center",
                bg=self.foreground_color(),
                fg=self.__font_clr
            )
        )
        self.interface.pack(identifier="text_label", expand=True)

        self.command_on_event(sequence="<Button-1>", child="text_label", command=self.__on_press_event, add="+")
        self.command_on_event(sequence="<Button-3>", child="text_label", command=self.__on_press_event, add="+")
        self.command_on_event(sequence="<Enter>", child="text_label", command=self.__on_hover_event, add="+")
        self.command_on_event(sequence="<Button-1>", command=self.__on_press_event, add="+")
        self.command_on_event(sequence="<Button-3>", command=self.__on_press_event, add="+")
        self.command_on_event(sequence="<Enter>", command=self.__on_hover_event, add="+")
        self.command_on_event(sequence="<Leave>", command=self.__on_hover_event, add="+")

    def hover_background_color(self) -> str:
        """ Returns button hover event background color. """
        return self.__hover_background_clr

    def hover_foreground_color(self) -> str:
        """ Returns button hover event foreground color. """
        return self.__hover_foreground_clr

    def font_color(self) -> str:
        """ Returns button label font color. """
        return self.__font_clr

    def set_hover_background(self, color: str) -> None:
        """ Set button hover event background color. """
        self.__hover_background_clr = color

    def set_hover_foreground(self, color: str) -> None:
        """ Set button hover event foreground color. """
        self.__hover_foreground_clr = color

    def __on_hover_event(self, event: Event) -> None:
        """ Handle button hover event. """
        if self.__hover_background_clr is None:
            return

        if event.type.name == "Enter":
            self.configure(fg_color=self.__hover_background_clr, require_redraw=True)
            self.interface.get(identifier="text_label").config(
                bg=self.__hover_background_clr,
                fg=self.__hover_foreground_clr
            )
        elif event.type.name == "Leave":
            self.set_foreground_color(color=self.foreground_color())
            self.interface.get(identifier="text_label").config(
                bg=self.foreground_color(),
                fg=self.__font_clr
            )

    def __on_press_event(self, event: Event) -> None:
        """ Handle button press event. """
        if event.num == 1:
            if self.has_primary_command():
                self.primary_command()
        elif event.num == 3:
            if self.has_secondary_command():
                self.secondary_command()
