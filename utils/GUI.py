import tkinter as tk
from tkinter import filedialog, ttk, W, CENTER, StringVar

from PIL import ImageFont
import os

class GUI:
    def __init__(self) -> None:
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
    
    def show_password(self):
        if self.show == "*":
            self.show = ""
        elif self.show == "":
            self.show = "*"
        self.__key_entry["show"] = self.show
    
    def Auth_window(self, filename):
        self.win.destroy()
        self.win=tk.Tk()
        self.win.title("Verify Password")
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
        
        # Create a label widget
        key_entry_var = StringVar()
        text = "Key: "
        label=tk.Label(self.win, text=text)
        label.place(relx=self.place_width_porcentage, rely=self.place_starting+self.place_step*3, anchor=W)
        
        self.__key_entry = ttk.Entry(self.win, width=31, textvariable=key_entry_var, show=self.show)
        self.__key_entry.place(relx=0.56, rely=self.place_starting+self.place_step*3, anchor=CENTER)

        #string:
        ok_button = ttk.Button(self.win, text="Ok", width = self.place_width//2 - 5, command=self.calculate)
        ok_button.place(relx=self.place_in_center - 0.2, rely=self.place_starting+self.place_step*5, anchor=CENTER)
        
        cancel_button = ttk.Button(self.win, text="Cancelar", width = self.place_width//2 -5, command=self.show_password)
        cancel_button.place(relx=self.place_in_center + 0.2, rely=self.place_starting+self.place_step*5, anchor=CENTER)
        
        self.win.mainloop()
        
    def open_encrypted_file(self):
        text_file_extensions = ['*.bin']
        ftypes = [
            ('.Bin (Encripted)', text_file_extensions)]
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                           filetypes=ftypes)
        self.Auth_window(filename)

    
    def calculate(self):
        pass
    
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
        load_file_button = ttk.Button(self.win, text="Create File", width = self.place_width, command=self.calculate)
        load_file_button.place(relx=self.place_in_center, rely=self.place_starting+self.place_step, anchor=CENTER)
 
        Load_key_button = ttk.Button(self.win, text="Load File", width = self.place_width, command=self.open_encrypted_file)
        Load_key_button.place(relx=self.place_in_center, rely=self.place_starting+self.place_step*2, anchor=CENTER)

        self.win.mainloop()
        
    def get_font_shape(self, string: str, font: str = None, font_size: int = 12) -> tuple:
        if font is None:
            font = self.font
        font_init = ImageFont.truetype(font, font_size)
        return font_init.getsize(string)

A = GUI()
A.init_window()