
""" Text Entry Widget Model """


#   EXTERNAL IMPORTS
from tkinter import StringVar


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class EntryModel:
    """ Text entry widget model. """
    def __init__(self, on_enter_call, validate_call, placeholder: str = "") -> None:
        self.__text_var: StringVar = StringVar(value=placeholder)
        self.__placeholder_text: str = placeholder
        self.__on_enter_command = on_enter_call if callable(on_enter_call) else None
        self.__validate_command = validate_call if callable(validate_call) else None

    @property
    def text(self) -> StringVar:
        """ Entry text variable. """
        return self.__text_var

    def has_enter_pressed_command(self) -> bool:
        """ Returns true if entry has command for enter press event. """
        return self.__on_enter_command is not None

    def has_validate_command(self) -> bool:
        """ Returns true if entry has a text validation command set. """
        return self.__validate_command is not None

    def has_placeholder_text(self) -> bool:
        """ Returns true if entry uses a placeholder text value when empty. """
        return self.__placeholder_text.strip() != ""

    def enter_pressed_command(self, **kwargs) -> None:
        """ Invoke entry 'on enter pressed' command. """
        return self.__on_enter_command(**kwargs)

    def validate_text_command(self, **kwargs) -> None:
        """ Invoke entry text validation command. """
        return self.__validate_command(**kwargs)

    def placeholder_text(self) -> str:
        """ Returns entry placeholder text value. """
        return self.__placeholder_text

    def set_enter_pressed_command(self, command) -> None:
        """ Set entry 'on enter pressed' command. """
        self.__on_enter_command = command if callable(command) else self.__on_enter_command

    def set_validate_command(self, command) -> None:
        """ Set entry text validation command. """
        self.__validate_command = command if callable(command) else self.__validate_command

    def text_variable(self) -> StringVar:
        """ Returns entry underlying text variable. """
        return self.__text_var
