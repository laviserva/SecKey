from functools import total_ordering
import tkinter as tk
from tkinter import ttk, W, CENTER, StringVar

from PIL import ImageFont

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
        #self.place_
    
    def calculate(self):
        pass
    
    def init_window(self):
        win=tk.Tk()
        win.resizable(width=False, height=False)
        # Set the geometry of the window
        win.geometry(self.geometry)

        # Create a frame widget
        frame=tk.Frame(win, width=self.width, height=self.height)
        frame.grid(row=0, column=0, sticky="NW")

        # Create a label widget
        label=tk.Label(win, text="SecKeys", font=self.font)
        label.place(relx=self.place_in_center, rely=self.place_starting, anchor=CENTER)

        load_file_button = ttk.Button(win, text="Load File", width = self.place_width, command=self.calculate)
        load_file_button.place(relx=self.place_in_center, rely=self.place_starting+self.place_step, anchor=CENTER)

        Load_key_button = ttk.Button(win, text="Load File", width = self.place_width, command=self.calculate)
        Load_key_button.place(relx=self.place_in_center, rely=self.place_starting+self.place_step*2, anchor=CENTER)
        
        # Create a label widget
        key_entry_var = StringVar()
        text = "Key: "
        label=tk.Label(win, text=text)
        key_entry = ttk.Entry(win, width=33, textvariable=key_entry_var)
        
        font = self.get_font_shape(text, self.font)[0]
        total_len = self.place_width_porcentage
        
        label.place(relx=total_len, rely=self.place_starting+self.place_step*3, anchor=W)
        key_entry.place(relx=0.55, rely=self.place_starting+self.place_step*3, anchor=CENTER)

        #string:
        Load_key_button = ttk.Button(win, text="Ok", width = self.place_width, command=self.calculate)
        Load_key_button.place(relx=self.place_in_center, rely=self.place_starting+self.place_step*4.5, anchor=CENTER)

        win.mainloop()
        
    def get_font_shape(self, string: str, font: str = None, font_size: int = 12) -> tuple:
        if font is None:
            font = self.font
        font_init = ImageFont.truetype(font, font_size)
        return font_init.getsize(string)

A = GUI()
A.init_window()