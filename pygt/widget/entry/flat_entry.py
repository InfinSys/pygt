
""" Flat Text Entry Widget """


#   EXTERNAL IMPORTS
from .entry_widget_model import EntryModel
from pygt.widget.base_widget import PyGTWidget
from tkinter import Widget, Entry, Event


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
DEFAULT_WIDTH: int = 70
DEFAULT_HEIGHT: int = 30
DEFAULT_CORNER_RADIUS: int = 0
DEFAULT_INSERT_WIDTH: int = 1
DEFAULT_FONT: tuple[str, int, str] = ("Arial", 9, "normal")
DEFAULT_BACKGROUND_COLOR: str = "#ffffff"
DEFAULT_FONT_COLOR: str = "#000000"
DEFAULT_TEXT_SELECT_BACKGROUND: str = "#000000"
DEFAULT_TEXT_SELECT_FOREGROUND: str = "#ffffff"
DEFAULT_PLACEHOLDER_FONT_COLOR: str = "#c9c9c9"
DEFAULT_HOVER_CURSOR: str = "xterm"
DEFAULT_TEXT_JUSTIFICATION: str = "left"
DEFAULT_TEXT_X_PAD: tuple[int, int] = (5, 5)
DEFAULT_TEXT_Y_PAD: tuple[int, int] = (5, 5)
DEFAULT_INSERT_FLASH_TIME: int = 500


#   CLASSES
class FlatEntry(PyGTWidget, EntryModel):
    """ Flat text entry. """
    def __init__(self, master: Widget, **kwargs) -> None:
        self.__text_font: tuple = kwargs.pop('font', DEFAULT_FONT)
        self.__font_clr: str = kwargs.pop('font_fg', DEFAULT_FONT_COLOR)
        self.__placeholder_font_clr: str = kwargs.pop('placeholder_fg', DEFAULT_PLACEHOLDER_FONT_COLOR)
        self.__text_x_pad: tuple = kwargs.pop('text_x_pad', DEFAULT_TEXT_X_PAD)
        self.__text_y_pad: tuple = kwargs.pop('text_y_pad', DEFAULT_TEXT_Y_PAD)
        self.__mask_character: str = kwargs.pop('show', None)
        self.__entry_size: int = kwargs.pop('width', None)

        on_enter_command = kwargs.pop('on_enter_call', None)
        validate_command = kwargs.pop('validate_call', None)
        hover_cursor: str = kwargs.pop('cursor', DEFAULT_HOVER_CURSOR)
        text_justification: str = kwargs.pop('justify', DEFAULT_TEXT_JUSTIFICATION)
        text_select_background: str = kwargs.pop('select_bg', DEFAULT_TEXT_SELECT_BACKGROUND)
        text_select_foreground: str = kwargs.pop('select_fg', DEFAULT_TEXT_SELECT_FOREGROUND)
        placeholder_text: str = kwargs.pop('placeholder', "")
        insert_width: int = kwargs.get('insertwidth', DEFAULT_INSERT_WIDTH)
        insert_on_time: int = kwargs.pop('insertontime', DEFAULT_INSERT_FLASH_TIME)
        insert_off_time: int = kwargs.pop('insertofftime', DEFAULT_INSERT_FLASH_TIME)

        PyGTWidget.__init__(
            self=self,
            master=master,
            width=kwargs.pop('width', 1),
            height=kwargs.pop('height', 1),
            corner_radius=kwargs.pop('corner_radius', DEFAULT_CORNER_RADIUS),
            fg=kwargs.pop('bg', DEFAULT_BACKGROUND_COLOR),
            propogate=kwargs.pop('propogate', True),
            border=kwargs.pop('border', 0),
            border_fg=kwargs.pop('border_fg', None),
            **kwargs
        )

        EntryModel.__init__(
            self=self,
            on_enter_call=on_enter_command,
            validate_call=validate_command,
            placeholder=placeholder_text
        )

        self.interface.new(
            identifier="text_entry",
            widget=Entry(
                master=self,
                width=self.__entry_size,
                textvariable=self.text_variable(),
                font=self.__text_font,
                justify=text_justification,
                relief="flat",
                bg=self.foreground_color(),
                fg=self.__font_clr,
                selectbackground=text_select_background,
                selectforeground=text_select_foreground,
                insertontime=insert_on_time,
                insertofftime=insert_off_time,
                insertwidth=insert_width,
                cursor=hover_cursor
            )
        )
        self.interface.pack(
            identifier="text_entry",
            fill="both",
            expand=True,
            padx=self.__text_x_pad,
            pady=self.__text_y_pad
        )

        self.command_on_event(sequence="<FocusIn>", command=self.__on_focus_in_event, child="text_entry", add="+")
        self.command_on_event(sequence="<FocusOut>", command=self.__on_focus_out_event, child="text_entry", add="+")
        self.command_on_event(sequence="<Return>", command=self.__on_enter_pressed_event, child="text_entry", add="+")

        if self.has_placeholder_text():
            self.__set_placeholder_mode(active=True)

    def is_negligable_text_value(self) -> bool:
        """ Returns true if entry contains no significant text. """
        return self.text.get().strip() == ""

    def text_font(self) -> tuple:
        """ Returns entry text font. """
        return self.__text_font

    def font_color(self) -> str:
        """ Returns entry font color. """
        return self.__font_clr

    def placeholder_font_color(self) -> str:
        """ Returns entry placeholder text font color. """
        return self.__placeholder_font_clr

    def mask_character(self) -> str:
        """ Returns entry mask character if any. """
        return self.__mask_character

    def entry_size(self) -> int:
        """ Returns width of entry. """
        return self.__entry_size

    def get_entry(self) -> Entry:
        """ Returns entry underlying entry widget. """
        return self.interface.get(identifier="text_entry")

    def set_text_font(self, font: tuple) -> None:
        """ Set entry text font. """
        self.__text_font = font
        self.get_entry().config(font=font)

    def set_font_color(self, color: str) -> None:
        """ Set entry font color. """
        self.__font_clr = color
        self.get_entry().config(fg=color)

    def set_placeholder_font_color(self, color: str) -> None:
        """ Set entry placeholder text font color. """
        self.__placeholder_font_clr = color

    def set_mask_character(self, show: str) -> None:
        """ Set entry mask character. """
        self.__mask_character = show
        self.get_entry().config(show=show)

    def set_entry_size(self, width: int) -> None:
        """ Set width of entry. """
        self.__entry_size = width
        self.get_entry().config(width=width)

    def take_focus(self) -> None:
        """ Give entry focus. """
        self.get_entry().focus_set()

    def __set_placeholder_mode(self, active: bool) -> None:
        """ Activate or deactivate entry placeholder text mode. """
        if active:
            self.get_entry().config(fg=self.__placeholder_font_clr)
        else:
            self.get_entry().config(fg=self.__font_clr)

    def __on_focus_in_event(self, event: Event) -> None:
        """ Handle entry focus-in event. """
        if self.has_placeholder_text() and (self.text.get() == self.placeholder_text()):
            self.__set_placeholder_mode(active=False)
            self.text.set(value="")

        if self.__mask_character is not None:
            self.set_mask_character(show=self.__mask_character)

    def __on_focus_out_event(self, event: Event) -> None:
        """ Handle entry focus-out event """
        if self.has_placeholder_text() and self.is_negligable_text_value():
            self.__set_placeholder_mode(active=True)
            if self.__mask_character is not None:
                self.set_mask_character(show=None)
            self.text.set(value=self.placeholder_text())

    def __on_enter_pressed_event(self, event: Event) -> None:
        """ Handle return key press event """
        self.enter_pressed_command()
