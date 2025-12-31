
""" Photo Image Widget """

#   EXTERNAL IMPORTS
from PIL import Image, ImageTk, ImageFile
import tkinter as tk


#   INTERNAL IMPORTS
from pygt.widget.base_widget import PyGTWidget


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class PhotoImage(PyGTWidget):
    """ Photo image. """
    def __init__(self, master: tk.Widget, img_path: str, width: int, height: int, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.pack_propagate(True)

        self.__path: str = img_path
        self.__dimensions: tuple[int, int] = width, height
        self.__photo = None

        if not self.load_image():
            print(f"ERROR: No such image at path: {self.__path}")
            return

        self.interface.new(
            identifier="img_label",
            widget=tk.Label(
                master=self,
                image=self.__photo
            )
        )
        self.interface.pack(
            identifier="img_label",
            expand=True
        )
        self.__image_label: tk.Label = self.interface.get(identifier="img_label")

    def set_path(self, img_path: str) -> None:
        """ Set image path. """
        self.__path = img_path

    def load_image(self) -> bool:
        """ Load image into memory. """
        try:
            original_image: ImageFile = Image.open(self.__path)
            resized_image: Image = original_image.resize(
                size=self.__dimensions,
                resample=Image.Resampling.LANCZOS
            )

            self.__photo = ImageTk.PhotoImage(resized_image)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False
