
""" List Table Widget """


#   EXTERNAL IMPORTS
from pygt.widget.base_widget import PyGTWidget
from tkinter import Widget
from tkinter.ttk import Treeview, Style


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
STYLE_CONFIG_NAME: str = "PyGTListTable.Treeview"
DEFAULT_CORNER_RADIUS: int = 4
DEFAULT_ROW_HEIGHT: int = 30
DEFAULT_HEADING_PADDING: int = 10
DEFAULT_BACKGROUND_COLOR: str = "#ffffff"
DEFAULT_SELECTED_CELL_BACKGROUND: str = "#309ed9"
DEFAULT_SELECTED_CELL_FOREGROUND: str = "#ffffff"
DEFAULT_FONT: tuple = ("Arial", 10, "normal")
DEFAULT_FONT_COLOR: str = "#000000"
DEFAULT_X_PAD: tuple[int, int] = (5, 5)
DEFAULT_Y_PAD: tuple[int, int] = (5, 5)


#   CLASSES
class ListTable(PyGTWidget):
    """ Simple list table. """
    def __init__(self, master: Widget, **kwargs) -> None:
        self.__column_ids: tuple[str] = kwargs.pop('columns', None)
        self.__column_names: dict[str, str] = {
            column_id: name for column_id, name in zip(self.__column_ids, kwargs.pop('labels', []))
        }
        self.__fit_to_size: bool = kwargs.pop('fit_to_size', False)
        self.__row_height: int = kwargs.pop('row_height', DEFAULT_ROW_HEIGHT)
        self.__alternate_cell_bg_clr: str = kwargs.get('alt_bg', DEFAULT_BACKGROUND_COLOR)
        self.__has_alternating_cells: bool = (kwargs.pop('alt_bg', None) is not None)

        table_height: int = kwargs.pop('table_height', None)
        heading_padding: int = kwargs.pop('heading_pad', DEFAULT_HEADING_PADDING)
        x_padding: tuple = kwargs.pop('padx', DEFAULT_X_PAD)
        y_padding: tuple = kwargs.pop('pady', DEFAULT_Y_PAD)
        heading_font: tuple = kwargs.pop('heading_font', DEFAULT_FONT)
        heading_font_fg: str = kwargs.pop('heading_fg', DEFAULT_FONT_COLOR)
        cell_font: tuple = kwargs.pop('cell_font', DEFAULT_FONT)
        cell_font_fg: str = kwargs.pop('cell_fg', DEFAULT_FONT_COLOR)
        select_cell_bg: str = kwargs.pop('select_cell_bg', DEFAULT_SELECTED_CELL_BACKGROUND)
        select_cell_fg: str = kwargs.pop('select_cell_fg', DEFAULT_SELECTED_CELL_FOREGROUND)
        show_columns: tuple[str] = kwargs.pop('show_columns', None)

        self.__treeview_init_args: dict[str, any] = {
            'master': self,
            'columns': self.__column_ids,
            'displaycolumns': show_columns,
            'show': "headings",
            'style': STYLE_CONFIG_NAME,
            'height': table_height
        }

        self.__treeview_pack_args: dict[str, any] = {
            'identifier': "treeview_table",
            'fill': "both",
            'expand': True,
            'padx': x_padding,
            'pady': y_padding
        }

        super().__init__(
            master=master,
            width=kwargs.pop('width', 1),
            height=kwargs.pop('height', 1),
            corner_radius=kwargs.pop('corner_radius', DEFAULT_CORNER_RADIUS),
            fg=kwargs.pop('bg', DEFAULT_BACKGROUND_COLOR),
            propogate=True,
            border=kwargs.pop('border', 0),
            border_fg=kwargs.pop('border_fg', None),
            **kwargs
        )

        self.__style: Style = Style()
        self.__style.configure(
            style=STYLE_CONFIG_NAME,
            rowheight=self.__row_height,
            font=cell_font,
            foreground=cell_font_fg,
            background=self.foreground_color()
        )
        self.__style.configure(
            style=f"{STYLE_CONFIG_NAME}.Heading",
            font=heading_font,
            foreground=heading_font_fg,
            padding=heading_padding
        )

        self.__style.layout(
            style=STYLE_CONFIG_NAME,
            layoutspec=[(f"{STYLE_CONFIG_NAME}.treearea", {'sticky': "nswe"})]
        )

        self.__style.map(
            style=STYLE_CONFIG_NAME,
            background=[("selected", select_cell_bg)],
            foreground=[("selected", select_cell_fg)]
        )

        self.__configure_treeview()

    def column_ids(self) -> list[str]:
        """ Returns list of table column identifiers. """
        return [column_id for column_id in self.__column_ids]

    def row_ids(self) -> list[str]:
        """ Returns list of table row identifiers. """
        return [row_id for row_id in self.get_treeview().get_children()]

    def column_names(self) -> list[str]:
        """ Returns list of table column names. """
        return [column_name for _, column_name in self.__column_names.items()]

    def row_height(self) -> int:
        """ Returns height of a single table row. """
        return self.__row_height

    def has_alternating_row_colors(self) -> bool:
        """ Returns true if table uses alternating row colors. """
        return self.__has_alternating_cells

    def get_treeview(self) -> Treeview:
        """ Returns list underlying treeview widget. """
        return self.interface.get(identifier="treeview_table")

    def length(self) -> int:
        """ Returns total number of rows in table. """
        return len(self.get_treeview().get_children())

    def get_row_data(self, identifier: str) -> tuple[any]:
        """ Returns data in row associated with provided identifier. """
        return self.get_treeview().item(item=identifier)['values']

    def table_data(self) -> list[list]:
        """ Returns table row data. """
        table_rows: list[tuple] = []

        for item_id in self.get_treeview().get_children():
            row_data = self.get_row_data(item_id)
            table_rows.append(row_data)

        return table_rows

    def get_selection(self) -> list[str]:
        """ Returns list of current selected table row identifiers. """
        return [row_id for row_id in self.get_treeview().selection()]

    def get_selection_data(self) -> list[tuple]:
        """ Returns set of current selected table rows. """
        selected_rows: list[str] = self.get_selection()

        if not selected_rows:
            return []

        selection_data: list[tuple] = []

        for row_id in selected_rows:
            selection_data.append(tuple(self.get_row_data(row_id)))

        return selection_data

    def append(self, row_data: list) -> None:
        """ Add row of data to end of table. """
        if self.has_alternating_row_colors():
            row_tag: str = "evenrow" if ((self.length() + 1) % 2) == 0 else "oddrow"
            self.get_treeview().insert(parent="", index="end", values=row_data, tags=(row_tag,))
        else:
            self.get_treeview().insert(parent="", index="end", values=row_data)

        if self.__fit_to_size:
            self.set_table_height(rows=self.length())

    def append_rows(self, rows: list[list]) -> None:
        """ Add rows of data to end of table. """
        for row_data in rows:
            self.append(row_data)

    def delete_row(self, **kwargs) -> None:
        """ Delete specified row from table. """
        row_id: str = kwargs.get('identifier', None)
        row_index: int = kwargs.get('index', None)
        delete_selected: bool = kwargs.get('selected', False)

        if (row_id is None) and (row_index is None) and (not delete_selected):
            return

        target_id: str = None

        if delete_selected:
            selected_rows: tuple[str] = self.get_treeview().selection()

            if (not selected_rows) or (len(selected_rows) > 1):
                return

            target_id = selected_rows[0]
        elif row_id is not None:
            target_id = row_id
        elif row_index is not None:
            target_id = self.row_ids()[row_index]

        self.get_treeview().delete(target_id)

        if self.has_alternating_row_colors():
            self.__redraw_table()

        if self.__fit_to_size:
            self.set_table_height(rows=self.length())

    def set_alternating_cell_color(self, color: str) -> None:
        """ Set color of every other row to specified color. """
        self.__alternate_cell_bg_clr = color
        self.__has_alternating_cells = True
        self.__redraw_table()

    def set_column_width(self, column_id: str, width: int) -> None:
        """ Set width of specified table column. """
        self.get_treeview().column(column=column_id, width=width)

    def set_row_height(self, height: int) -> None:
        """ Set row height for entire table. """
        self.__row_height = height
        self.__style.configure(style=STYLE_CONFIG_NAME, rowheight=height)

    def set_table_height(self, rows: int) -> None:
        """ Set total number of rows table shows at once. """
        self.get_treeview().configure(height=rows)

    def __configure_treeview(self) -> None:
        """ Prepare treeview widget. """
        self.interface.new(
            identifier="treeview_table",
            widget=Treeview(**self.__treeview_init_args)
        )
        self.interface.pack(**self.__treeview_pack_args)

        self.get_treeview().tag_configure(tagname="oddrow", background=self.foreground_color())
        self.get_treeview().tag_configure(tagname="evenrow", background=self.__alternate_cell_bg_clr)

        for column_id in self.__column_ids:
            self.get_treeview().heading(
                column=column_id,
                text=self.__column_names.get(column_id, column_id)
            )

    def __redraw_table(self) -> None:
        """ Update tables appearance on user interface. """
        data: list[list] = self.table_data()
        self.interface.remove(identifier="treeview_table")
        self.__configure_treeview()
        self.append_rows(rows=data)
