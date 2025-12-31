
""" Application View Widget Manager """


#   EXTERNAL IMPORTS
from tkinter import Widget, Frame


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class WidgetManager:
    """ Application view widget manager. """
    def __init__(self) -> None:
        self.__widgets: dict[str, Widget] = {}
        self.__pack_args: dict[str, dict[str, any]] = {}

    def widgets(self) -> list[str]:
        """ Returns list of managed widget identifiers. """
        return [widget_id for widget_id in self.__widgets.keys()]

    def is_existing_widget(self, identifier: str) -> bool:
        """ Returns true is a widget exists with the provided identifier. """
        return identifier in self.__widgets.keys()

    def has_stored_pack_arguments(self, identifier: str) -> bool:
        """ Returns true if widget has pack arguments stored. """
        return (identifier in self.__pack_args.keys()) and (len(self.__pack_args[identifier].keys()) > 0)

    def get(self, identifier: str) -> Widget:
        """ Returns requested widget. """
        if not self.is_existing_widget(identifier):
            return None

        return self.__widgets[identifier]

    def get_widgets(self, *widget_ids) -> list[Widget]:
        """ Returns requested widgets or all if no identifiers specified. """
        requested: list[Widget] = []

        for identifier, widget in self.__widgets.items():
            if (widget_ids and (identifier in widget_ids)) or (not widget_ids):
                requested.append(widget)

        return requested

    def new(self, identifier: str, widget: Widget) -> Widget:
        """ Add new widget to view and return instance. """
        if self.is_existing_widget(identifier):
            return None

        self.__widgets[identifier] = widget

        return widget
    
    def update(self, identifier: str, widget: Widget) -> bool:
        """ Update instance of existing widget. """
        if not self.is_existing_widget(identifier):
            return False

        if self.__widgets[identifier] is not None:
            return False

        self.__widgets[identifier] = widget
        return True

    def pack(self, identifier: str, save_args: bool = False, **pack_args) -> None:
        """ Pack specified widget on view. """
        if not self.is_existing_widget(identifier):
            return

        if save_args:
            self.__pack_args[identifier] = pack_args

        self.__widgets[identifier].pack(**pack_args)

    def forget(self, identifier: str) -> bool:
        """ Remove specified widget from layout manager (screen). """
        if not self.is_existing_widget(identifier):
            return False

        self.__widgets[identifier].pack_forget()
        return True

    def restore(self, identifier: str, delete_args: bool = True, **opt_new_pack) -> bool:
        """ Restore specified widget in layout manager (screen). """
        if not self.is_existing_widget(identifier):
            return False

        if (len(opt_new_pack.keys()) == 0) and (not self.has_stored_pack_arguments(identifier)):
            return False

        if len(opt_new_pack.keys()) == 0:
            self.__widgets[identifier].pack(
                **self.__pack_args[identifier]
            )
        else:
            opt_new_pack.update(self.__pack_args.get(identifier, {}))
            self.__widgets[identifier].pack(
                **opt_new_pack
            )

        if delete_args and self.has_stored_pack_arguments(identifier):
            del self.__pack_args[identifier]

        return True

    def remove(self, identifier: str) -> bool:
        """ Remove specified widget from view management. """
        if not self.is_existing_widget(identifier):
            return False

        self.__widgets[identifier].pack_forget()
        self.__widgets[identifier].destroy()
        del self.__widgets[identifier]
        return True

    def set_background_of(self, identifier: str, color: str) -> None:
        """ Set background color of specified widget. """
        if not self.is_existing_widget(identifier):
            return

        self.__widgets[identifier].config(bg=color)

    def set_foreground_of(self, identifier: str, color: str) -> None:
        """ Set foreground color of specified widget. """
        if not self.is_existing_widget(identifier):
            return

        self.__widgets[identifier].config(fg=color)

    def new_container(self, identifier: str, parent: Widget, **container_args) -> Frame:
        """ Create new managed widget container and return instance. """
        if self.is_existing_widget(identifier):
            return None

        propogate: bool = container_args.pop('propogate', True)

        self.new(
            identifier=identifier,
            widget=Frame(
                master=parent,
                **container_args
            )
        )

        self.get(identifier).pack_propagate(propogate)
        self.get(identifier).grid_propagate(propogate)

        return self.__widgets[identifier]
