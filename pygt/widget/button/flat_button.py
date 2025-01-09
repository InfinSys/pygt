
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
DEFAULT_BUTTON_COLOR: str = "#888888"
DEFAULT_FONT_COLOR: str = "#000000"
DEFAULT_TEXT_X_PAD: tuple[int, int] = (5, 5)
DEFAULT_TEXT_Y_PAD: tuple[int, int] = (5, 5)


#   CLASSES
class FlatButton(PyGTWidget, ButtonModel):
    """ Flat button. """
    def __init__(self, master: Widget, text: str, **kwargs) -> None:
        self.__hover_background_clr: str = kwargs.pop('hover_bg', None)
        self.__hover_foreground_clr: str = kwargs.pop('hover_fg', None)
        self.__text_font: tuple = kwargs.pop('font', DEFAULT_FONT)
        self.__font_clr: str = kwargs.pop('font_fg', DEFAULT_FONT_COLOR)
        self.__text_x_pad: tuple = kwargs.pop('text_x_pad', DEFAULT_TEXT_X_PAD)
        self.__text_y_pad: tuple = kwargs.pop('text_y_pad', DEFAULT_TEXT_Y_PAD)

        primary_command = kwargs.pop('primary_cmd', None)
        secondary_command = kwargs.pop('secondary_cmd', None)

        PyGTWidget.__init__(
            self=self,
            master=master,
            width=kwargs.pop('width', DEFAULT_WIDTH),
            height=kwargs.pop('height', DEFAULT_HEIGHT),
            corner_radius=kwargs.pop('corner_radius', DEFAULT_CORNER_RADIUS),
            fg=kwargs.pop('bg', DEFAULT_BUTTON_COLOR),
            propogate=kwargs.pop('fit_to_size', False),
            **kwargs
        )

        ButtonModel.__init__(
            self=self,
            text=text,
            primary_call=primary_command,
            secondary_call=secondary_command
        )

        self.interface.new(
            identifier="text_label",
            widget=Label(
                master=self,
                textvariable=self.text_variable(),
                font=self.__text_font,
                anchor="center",
                bg=self.foreground_color(),
                fg=self.__font_clr
            )
        )
        self.interface.pack(
            identifier="text_label",
            expand=True,
            padx=self.__text_x_pad,
            pady=self.__text_y_pad
        )

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

    def font_hover_color(self) -> str:
        """ Returns button hover event foreground color. """
        return self.__hover_foreground_clr
    
    def text_font(self) -> tuple:
        """ Returns button text font. """
        return self.__text_font

    def font_color(self) -> str:
        """ Returns button label font color. """
        return self.__font_clr
    
    def get_label(self) -> Label:
        """ Returns button label widget. """
        return self.interface.get(identifier="text_label")

    def set_hover_background(self, color: str) -> None:
        """ Set button hover event background color. """
        self.__hover_background_clr = color

    def set_font_hover_color(self, color: str) -> None:
        """ Set button hover event foreground color. """
        self.__hover_foreground_clr = color
    
    def set_text_font(self, font: tuple) -> None:
        """ Set button text font. """
        self.__text_font = font
        self.get_label().config(font=font)

    def set_font_color(self, color: str) -> None:
        """ Set button font color. """
        self.__font_clr = color
        self.get_label().config(fg=color)

    def __on_hover_event(self, event: Event) -> None:
        """ Handle button hover event. """
        if self.__hover_background_clr is None:
            return

        if event.type.name == "Enter":
            self.configure(fg_color=self.__hover_background_clr, require_redraw=True)
            self.get_label().config(
                bg=self.__hover_background_clr,
                fg=self.__hover_foreground_clr
            )
        elif event.type.name == "Leave":
            self.set_foreground_color(color=self.foreground_color())
            self.get_label().config(
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
