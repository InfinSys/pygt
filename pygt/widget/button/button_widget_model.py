
""" Button Widget Model """


#   EXTERNAL IMPORTS
from tkinter import StringVar


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ButtonModel:
    """ Button widget model. """
    def __init__(self, text: str, primary_call, secondary_call) -> None:
        self.__text_var: StringVar = StringVar(value=text)
        self.__primary_cmd = primary_call if callable(primary_call) else None
        self.__secondary_cmd = secondary_call if callable(secondary_call) else None

    @property
    def text(self) -> StringVar:
        """ Button text variable. """
        return self.__text_var

    def has_command(self) -> bool:
        """ Returns true if button is associated with any command. """
        return (self.__primary_cmd is not None) or (self.__secondary_cmd is not None)

    def has_primary_command(self) -> bool:
        """ Returns true if button has a primary command. """
        return self.__primary_cmd is not None

    def has_secondary_command(self) -> bool:
        """ Returns true if button has a secondary command. """
        return self.__secondary_cmd is not None

    def primary_command(self, **kwargs) -> None:
        """ Invoke primary button command. """
        return self.__primary_cmd(**kwargs)

    def secondary_command(self, **kwargs) -> None:
        """ Invoke secondary button command. """
        return self.__secondary_cmd(**kwargs)

    def set_primary_command(self, command) -> None:
        """ Set primary button command. """
        self.__primary_cmd = command if callable(command) else self.__primary_cmd

    def set_secondary_command(self, command) -> None:
        """ Set secondary button command. """
        self.__secondary_cmd = command if callable(command) else self.__secondary_cmd

    def text_variable(self) -> StringVar:
        """ Returns button underlying text variable. """
        return self.__text_var
