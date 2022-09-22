import os
import tkinter as tk

from PIL import Image
from enum import Enum, auto

from img_utils import resize_image

class data_window_state(Enum):
    pass

class data_window:
    def __init__(self) -> None:
        self.width  = 300
        self.height = 400
        self.menu_width = 50
        self.menu_weight = 400
        self.menu_buttons_step = self.height // 6
        self.buttons_width = 40
        self.buttons_height = 40
        
        self.__menu_bg = "#3a7ff6"
        self.__resources_dir = r"resources"
        self.__menu_image = os.path.join(self.__resources_dir, "menu.png")
        self.__add_image = os.path.join(self.__resources_dir, "add.png")
        self.__save_image = os.path.join(self.__resources_dir, "save.png")
        self.__key_image = os.path.join(self.__resources_dir, "key.png")
        self.__config_image = os.path.join(self.__resources_dir, "config.png")
    
    def printo(self):
        print("button")
        
    def __create_buttons(self, window: tk.Frame, text: str, image, command, relx: float, rely: float) -> tk.Button:
        button = tk.Button(window,
                                text = text,
                                width=self.buttons_width,
                                height=self.buttons_height,
                                border=0,
                                highlightbackground="#000000",
                                highlightcolor="#000000",
                                highlightthickness=3,
                                activebackground="#aaaaaa",
                                activeforeground="#000000",
                                bg = self.__menu_bg,
                                image=image,
                                command = command
                                )
        button.place(relx=relx, rely=rely)
        return button
    
    def __on_button(self, button: tk.Button, bg: str, fg: str) -> None:
        button.bind("<Enter>", lambda event: self.__on_enter_mouse(button, bg, fg))
        button.bind("<Leave>", lambda event: self.__on_leave_mouse(button, bg, fg))
    
    def __on_enter_mouse(self, button: tk.Button, bg: str, fg: str) -> None:
        button["background"] = bg
        button["foreground"] = fg
    
    def __on_leave_mouse(self, button: tk.Button, bg: str, fg: str) -> None:
        button["background"] = fg
        button["foreground"] = bg
    
    def __create_menu(self) -> None:
        self.menu = tk.Frame(self.win, width=self.menu_width, height=self.menu_weight ,background=self.__menu_bg)
        self.menu.pack(side = "left",  fill = tk.BOTH)
        
        menu_button = self.__create_buttons(self.menu, "menu", self.__menu_image, self.printo, 0, 0.1)
        menu_button.pack()
        add_button = self.__create_buttons(self.menu, "add", self.__add_image, self.printo, 0, 0.2)
        add_button.pack()
        save_button = self.__create_buttons(self.menu, "save", self.__save_image, self.printo, 0, 0.3)
        save_button.pack()
        key_button = self.__create_buttons(self.menu, "key", self.__key_image, self.printo, 0, 0.4)
        key_button.pack()
        config_button = self.__create_buttons(self.menu, "config", self.__config_image, self.printo, 0, 0.5)
        config_button.pack()
        
        self.__on_button(menu_button, "#aaaaaa", "#bb934a")
        self.__on_button(add_button, "#aaaaaa", "#bb934a")
        self.__on_button(save_button, "#aaaaaa", "#bb934a")
        self.__on_button(key_button, "#aaaaaa", "#bb934a")
        self.__on_button(config_button, "#aaaaaa", "#bb934a")
        
    def __load_images(self):
        self.__menu_image = resize_image(self.__menu_image, self.buttons_width, self.buttons_height)
        self.__add_image = resize_image(self.__add_image, self.buttons_width, self.buttons_height)
        self.__save_image = resize_image(self.__save_image, self.buttons_width, self.buttons_height)
        self.__key_image = resize_image(self.__key_image, self.buttons_width, self.buttons_height)
        self.__config_image = resize_image(self.__config_image, self.buttons_width, self.buttons_height)
    
    def window(self):
        self.win=tk.Tk()
        screen_width  = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x_coordinates = screen_width//2 - self.width//2
        y_coordinates = screen_height//2 - self.height//2
        self.win.title("SecKey")
        self.geometry = f"{str(self.width)}x{str(self.height)}+{x_coordinates}+{y_coordinates}"
        self.win.iconphoto(False, tk.PhotoImage(file=os.path.join(self.__resources_dir,"sk.png")))
        #self.win.wm_attributes('-toolwindow', 'True') # Hide icon
        self.win.resizable(width=False, height=False)
        # Set the geometry of the window
        self.win.geometry(self.geometry)
        self.__load_images()
        self.__create_menu()
        
        self.win.mainloop()

import os
print(os.path.exists(r"resources"))
A = data_window()
A.window()