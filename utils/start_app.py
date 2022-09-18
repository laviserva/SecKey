import tkinter as tk
from tkinter import filedialog, ttk, W, CENTER, StringVar

from PIL import ImageFont
import os

from dec import EaD # Encript and Decript
from enum import Enum, auto

class start_app_state(Enum):
    ALIVE = auto()
    CLOSED = auto()
    DESTROYED = auto()
    LOADING_FILE = auto()

class start_app(EaD):
    def __init__(self) -> None:
        self.state = start_app_state.ALIVE
        self.width  = 300
        self.height = 400
        self.geometry = f"{str(self.width)}x{str(self.height)}"
        
        self.place_starting = 0.2
        self.place_step = 0.1
        self.place_in_center = 0.5
        self.place_width_porcentage = 0.125 #38
        self.place_width = int(self.place_width_porcentage * self.width)
        self.font = "arial.ttf"
        
        self.show = "*"
        self.__file = None
        
    def __on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.win.destroy()
        self.state = start_app_state.CLOSED
    
    def open_encrypted_file(self):
        text_file_extensions = ['*.bin']
        ftypes = [
            ('.Bin (Encripted)', text_file_extensions)]
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                           filetypes=ftypes)
        self.__file =  filename
        self.win.destroy()
        self.state = start_app_state.LOADING_FILE
    
    def init_window(self):
        self.win=tk.Tk()
        self.win.title("SecKey")
        self.win.wm_attributes('-toolwindow', 'True')
        self.win.resizable(width=False, height=False)
        
        # Set the geometry of the window
        self.win.geometry(self.geometry)

        # Create a frame widget
        frame=tk.Frame(self.win, width=self.width, height=self.height)
        frame.grid(row=0, column=0, sticky="NW")

        # Create a label widget
        label=tk.Label(self.win, text="SecKeys", font=self.font)
        label.place(relx=self.place_in_center, rely=self.place_starting, anchor=CENTER)

        # Buttons
        create_file_button = ttk.Button(self.win, text="Create File", width = self.place_width)
        create_file_button.place(relx=self.place_in_center, rely=self.place_starting+self.place_step, anchor=CENTER)
 
        Load_key_button = ttk.Button(self.win, text="Load File", width = self.place_width, command=self.open_encrypted_file)
        Load_key_button.place(relx=self.place_in_center, rely=self.place_starting+self.place_step*2, anchor=CENTER)

        self.win.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.win.mainloop()
        return self.__file
        
    def get_font_shape(self, string: str, font: str = None, font_size: int = 12) -> tuple:
        if font is None:
            font = self.font
        font_init = ImageFont.truetype(font, font_size)
        return font_init.getsize(string)