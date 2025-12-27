
""" Scrollable Frame Widget """


#   EXTERNAL IMPORTS
import tkinter as tk
from tkinter import ttk


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ScrollFrame(ttk.Frame):
    """ Scrollable wrapper frame. """
    def __init__(self, master: tk.Widget, view_type: type = None, **init_args) -> None:
        super().__init__(master=master)

        self.__canvas: tk.Canvas = tk.Canvas(master=self)
        self.__scrollbar: ttk.Scrollbar = ttk.Scrollbar(
            master=self,
            orient=tk.VERTICAL,
            command=self.__canvas.yview
        )
        self.__canvas.configure(yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.__frame_type: type = view_type
        self.__frame_id: int = None
        self.__frame: tk.Frame = None

        if self.__frame_type is not None:
            self.set_view(view_type=view_type, **init_args)

        if self.__frame is not None:
            self.__setup_event_bindings()
            self.__populate_frame_in_canvas()

    def get_view(self) -> tk.Frame:
        """ Returns inner-frame. """
        return self.__frame

    def set_view(self, view_type: type, **init_args) -> None:
        """ Set scrollable view frame. """
        if self.__frame is None:
            self.__frame = view_type(
                master=self.__canvas,
                **init_args
            )
            self.__setup_event_bindings()
            self.__populate_frame_in_canvas()

    def scroll_to_percentage(self, h_percent: float) -> None:
        """ Scroll to region of view using height percentage. """
        self.__canvas.yview_moveto(h_percent)

    def scroll_to_top(self):
        """ Scroll to very top of view. """
        self.__canvas.yview_moveto(0)

    def scroll_to_bottom(self):
        """ Scroll to very bottom of view. """
        self.__canvas.yview_moveto(1)

    def __setup_event_bindings(self) -> None:
        """ Setup event bindings. """
        self.__canvas.bind(
            "<Enter>",
            lambda e: self.__canvas.bind_all("<MouseWheel>", self.__on_mouse_wheel)
        )
        self.__canvas.bind("<Leave>", lambda e: self.__canvas.unbind_all("<MouseWheel>"))
        self.__canvas.bind("<Configure>", self.__on_canvas_configure)
        self.__frame.bind("<Configure>", self.__on_frame_configure)

    def __populate_frame_in_canvas(self) -> None:
        """ Create viewable frame in canvas. """
        self.__frame_id = self.__canvas.create_window(
            (0, 0),
            window=self.__frame,
            anchor=tk.NW
        )

    def __on_frame_configure(self, event: tk.Event) -> None:
        """ Handle dynamic inner-frame resize events. """
        # Keep scroll region in sync
        self.__canvas.configure(scrollregion=self.__canvas.bbox(tk.ALL))

    def __on_canvas_configure(self, event: tk.Event) -> None:
        """ Handle dynamic canvas resize events. """
        # Keep content width in sync
        self.__canvas.itemconfig(self.__frame_id, width=event.width)

    def __on_mouse_wheel(self, event: tk.Event) -> None:
        """ Handle user scroll wheel event. """
        first, last = self.__canvas.yview()

        if first <= 0.0 and last >= 1.0:
            return  # No scrolling - content fits entirely

        self.__canvas.yview_scroll(-1 * (event.delta // 120), tk.UNITS)
