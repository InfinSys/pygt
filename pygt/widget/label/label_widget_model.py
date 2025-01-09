
""" Label Widget Model """


#   EXTERNAL IMPORTS
from tkinter import StringVar


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class LabelModel:
    """ Label widget model. """
    def __init__(self, text: str) -> None:
        self.__text_var: StringVar = StringVar(value=text)
    
    @property
    def text(self) -> StringVar:
        """ Label text variable. """
        return self.__text_var

    def has_text(self) -> bool:
        """ Returns true if label contains text. """
        return self.__text_var.get() != ""

    def text_variable(self) -> StringVar:
        """ Returns label underlying text variable. """
        return self.__text_var
