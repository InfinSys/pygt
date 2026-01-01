
""" Base PyGT Widget Class """


#   EXTERNAL IMPORTS
from tkinter import Widget
from customtkinter import CTkFrame
import tkinter as tk
from typing import Union, Callable
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
        self.__corner_background_clr: Union[str, tuple] = kwargs.get('corner_bg', None)
        self.__border_clr: str = kwargs.get('border_fg', None)
        self.__border_width: int = kwargs.get('border', 0)
        self.__corner_radius: int = kwargs.get('corner_radius', 0)
        self.__monitor_mouse: bool = kwargs.get('track_mouse', True)
        self.__has_mouse: Union[bool, None] = False if self.__monitor_mouse else None
        self.__mouse_entry_cmd: Union[Callable, None] = kwargs.get('mouse_enter_cmd', None)
        self.__mouse_entry_cmd = self.__mouse_entry_cmd if callable(
            self.__mouse_entry_cmd) and self.__monitor_mouse else None
        self.__mouse_exit_cmd: Union[Callable, None] = kwargs.get('mouse_exit_cmd', None)
        self.__mouse_exit_cmd = self.__mouse_exit_cmd if callable(
            self.__mouse_exit_cmd) and self.__monitor_mouse else None

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

        if self.__monitor_mouse:
            self.__configure_mouse_watch_events()

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

    def corner_background_color(self) -> Union[str, tuple]:
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

    def bounds(self) -> tuple[int, int, int, int]:
        """ Returns top-left and bottom-right most
            coordinates of widget bounds box relative
            client to display. """
        self.update_idletasks()
        x_pos: int = self.winfo_rootx()
        y_pos: int = self.winfo_rooty()
        width_: int = self.winfo_width()
        height_: int = self.winfo_height()
        return x_pos, y_pos, (x_pos + width_), (y_pos + height_)

    def is_overlapping(self, widget: any) -> bool:
        """ Returns true if any part of provided widgets
            bounds intersects this bounds. """
        ax1, ay1, ax2, ay2 = self.bounds()

        if issubclass(type(widget), PyGTWidget):
            widget: PyGTWidget
            bx1, by1, bx2, by2 = widget.bounds()
            return not (
                ax2 <= bx1 or  # 'a' is left of 'b'
                ax1 >= bx2 or  # 'a' is right of 'b'
                ay2 <= by1 or  # 'a' is above 'b'
                ay1 >= by2     # 'a' is below 'b'
            )
        elif issubclass(type(widget), Widget):
            widget: Widget
            widget.update_idletasks()
            bx1: int = widget.winfo_rootx()
            by1: int = widget.winfo_rooty()
            bx2: int = bx1 + widget.winfo_width()
            by2: int = by1 + widget.winfo_height()
            return not (
                ax2 <= bx1 or  # 'a' is left of 'b'
                ax1 >= bx2 or  # 'a' is right of 'b'
                ay2 <= by1 or  # 'a' is above 'b'
                ay1 >= by2     # 'a' is below 'b'
            )
        else:
            print(f"\nWARNING: Cannot validate overlap of 'PyGTWidget' type versus '{type(widget)}' type!")
            return False  # Invalid type for check

    def is_tracking_mouse(self) -> bool:
        """ Returns true if widget is watching
            for mouse entry/exit. """
        return self.__monitor_mouse

    def has_mouse_within_bounds(self) -> bool:
        """ Returns true if mouse is within widget bounds box.
             (DO NOT POLL THIS METHOD!!!)"""
        mouse_x: int = self.winfo_pointerx()
        mouse_y: int = self.winfo_pointery()
        x1, y1, x2, y2 = self.bounds()
        return (x1 <= mouse_x < x2) and (y1 <= mouse_y < y2)

    def has_mouse(self) -> Union[bool, None]:
        """ Returns true if mouse is above this widget;
            returns None if not monitoring mouse. """
        return self.__has_mouse

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

    def track_mouse(self) -> None:
        """ Instruct widget to track mouse entry/exit events. """
        if self.__monitor_mouse:
            return
        self.__configure_mouse_watch_events()

    def command_on_event(self, sequence: str, command, child: str = None, **kwargs) -> None:
        """ Bind command on specified event to
        entire widget or specified child widget. """
        if (child is not None) and (self.interface.is_existing_widget(child)):
            try:
                self.interface.get(child).bind(sequence=sequence, func=command, **kwargs)
            except Exception:
                self.interface.get(child).bind(sequence=sequence, command=command, **kwargs)
        elif child is None:
            raw_sequence: str = sequence.strip('<').strip('>')
            if (raw_sequence == "Enter") or (raw_sequence == "Leave"):
                kwargs['add'] = True
            self.bind(sequence=sequence, command=command, **kwargs)

    def __configure_mouse_watch_events(self) -> None:
        """ Prepare mouse watch events. """
        self.bind(
            sequence="<Enter>",
            command=self.__on_mouse_entry,
            add=True
        )
        self.bind(
            sequence="<Leave>",
            command=self.__on_mouse_exit,
            add=True
        )

    def __on_mouse_entry(self, event: tk.Event) -> None:
        """ Handle mouse hover events. """
        if self.__has_mouse or (not self.has_mouse_within_bounds()):
            return
        self.__has_mouse = True
        if self.__mouse_entry_cmd is not None:
            self.__mouse_entry_cmd(event=event)

    def __on_mouse_exit(self, event: tk.Event) -> None:
        """ Handle mouse leave events. """
        if self.has_mouse_within_bounds():
            return
        self.__has_mouse = False
        if self.__mouse_exit_cmd is not None:
            self.__mouse_exit_cmd(event=event)
