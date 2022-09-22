import os
import tkinter as tk

from PIL import Image
from enum import Enum, auto

class data_window_state(Enum):
    pass

class data_window:
    def __init__(self) -> None:
        self.width  = 300
        self.height = 400
        self.menu_width = 50
        self.menu_weight = 400
        self.menu_buttons_step = self.height // 6
        self.buttons_width = 7
        self.buttons_height = 4
    
    def printo(self):
        print("button")
        
    def __create_buttons(self, window: tk.Frame, text: str, command, relx: float, rely: float) -> tk.Button:
        button = tk.Button(window,
                                text = text,
                                width=self.buttons_width,
                                height=self.buttons_height,
                                #image=tk.PhotoImage(file=r"resources\menu.png"),
                                command = command
                                )
        button.place(relx=relx, rely=rely)
        return button
    
    def __create_menu(self) -> None:
        self.menu = tk.Frame(self.win, width=self.menu_width, height=self.menu_weight ,background="#3a7ff6")
        self.menu.pack(side = "left",  fill = tk.BOTH)
        
        menu_button = self.__create_buttons(self.menu, "menu", self.printo, 0, 0.1).pack()
        add_button = self.__create_buttons(self.menu, "add", self.printo, 0, 0.2).pack()
        save_button = self.__create_buttons(self.menu, "save", self.printo, 0, 0.3).pack()
        key_button = self.__create_buttons(self.menu, "key", self.printo, 0, 0.4).pack()
        config_button = self.__create_buttons(self.menu, "config", self.printo, 0, 0.5).pack()
        
    
    def window(self):
        self.win=tk.Tk()
        screen_width  = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x_coordinates = screen_width//2 - self.width//2
        y_coordinates = screen_height//2 - self.height//2
        self.win.title("SecKey")
        self.geometry = f"{str(self.width)}x{str(self.height)}+{x_coordinates}+{y_coordinates}"
        self.win.iconphoto(False, tk.PhotoImage(file=r"resources\sk.png"))
        #self.win.wm_attributes('-toolwindow', 'True') # Hide icon
        self.win.resizable(width=False, height=False)
        # Set the geometry of the window
        self.win.geometry(self.geometry)
        self.__create_menu()
        
        self.win.mainloop()

import os
print(os.path.exists(r"resources"))
A = data_window()
A.window()