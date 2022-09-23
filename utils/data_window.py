from ast import Add
import os
import tkinter as tk

from enum import Enum, auto

from img_utils import resize_image, from_array_to_img, from_img_to_array

class data_window_state(Enum):
    pass

class buttons_state(Enum):
    MENU = auto()
    ADD = auto()
    SAVE = auto()
    KEY = auto()
    CONFIG = auto()

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
        self.__menu_fg = "#aaaaaa"
        self.__resources_dir = r"resources"
        self.__menu_image_path = os.path.join(self.__resources_dir, "menu.png")
        self.__add_image_path = os.path.join(self.__resources_dir, "add.png")
        self.__save_image_path = os.path.join(self.__resources_dir, "save.png")
        self.__key_image_path = os.path.join(self.__resources_dir, "key.png")
        self.__config_image_path = os.path.join(self.__resources_dir, "config.png")
    
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
    
    def __from_hexa_to_rgb(self, hexa: str) -> tuple:
        hexa = hexa[1:]
        rgb = list(int(hexa[i:i+2], 16) for i in (0, 2, 4))
        rgb = (*rgb, 255)
        return rgb
    
    def __on_button(self, button: tk.Button, img, bg: str, fg: str, state: buttons_state) -> None:
        button.bind("<Enter>", lambda event: self.__on_enter_mouse(button, img, bg, fg, state))
        button.bind("<Leave>", lambda event: self.__on_leave_mouse(button, img, bg, fg, state))
    
    def __on_enter_mouse(self, button: tk.Button, img, bg: str, fg: str, state: buttons_state) -> None:
        img_array = from_img_to_array(img)
        img_array[:,:,3 != 0] = (0, 0, 0, 255)
        self.__on_update_image(img_array, state)
        button["background"] = fg
        button["foreground"] = bg
    
    def __on_leave_mouse(self, button: tk.Button, img, bg: str, fg: str, state: buttons_state) -> None:
        img_array = from_img_to_array(img)
        img_array[:,:,3 != 0] = (255, 255, 255, 255)
        self.__on_update_image(img_array, state)
        button["background"] = bg
        button["foreground"] = fg
        button.config(image = self.__menu_image)
    
    def __on_update_image(self, img, state: buttons_state):
        if state == buttons_state.MENU:
            self.__menu_image = from_array_to_img(img)
            print(self.__menu_image)
        elif state == buttons_state.ADD:
            self.__add_image = from_array_to_img(img)
        elif state == buttons_state.SAVE:
            self.__save_image = from_array_to_img(img)
        elif state == buttons_state.KEY:
            self.__key_image = from_array_to_img(img)
        elif state == buttons_state.CONFIG:
            self.__config_image = from_array_to_img(img)
    
    def __create_menu(self) -> None:
        self.menu = tk.Frame(self.win, width=self.menu_width, height=self.menu_weight ,background=self.__menu_bg)
        self.menu.pack(side = "left",  fill = tk.BOTH)
        
        menu_button = self.__create_buttons(self.menu, "menu", self.__menu_image, self.printo, 0, 0.1)
        menu_button.pack()
        menu_button.config(image=self.__menu_image)
        add_button = self.__create_buttons(self.menu, "add", self.__add_image, self.printo, 0, 0.2)
        add_button.pack()
        save_button = self.__create_buttons(self.menu, "save", self.__save_image, self.printo, 0, 0.3)
        save_button.pack()
        key_button = self.__create_buttons(self.menu, "key", self.__key_image, self.printo, 0, 0.4)
        key_button.pack()
        config_button = self.__create_buttons(self.menu, "config", self.__config_image, self.printo, 0, 0.5)
        config_button.pack()
        
        self.__on_button(button=menu_button, img=self.__menu_image_path, bg = self.__menu_bg, fg= self.__menu_fg, state= buttons_state.MENU)
        self.__on_button(button=add_button, img=self.__add_image_path, bg = self.__menu_bg, fg= self.__menu_fg, state= buttons_state.ADD)
        self.__on_button(button=save_button, img=self.__save_image_path, bg = self.__menu_bg, fg= self.__menu_fg, state= buttons_state.SAVE)
        self.__on_button(button=key_button, img=self.__key_image_path, bg = self.__menu_bg, fg= self.__menu_fg, state= buttons_state.KEY)
        self.__on_button(button=config_button, img=self.__config_image_path, bg = self.__menu_bg, fg= self.__menu_fg, state= buttons_state.CONFIG)
        
    def __load_images(self):
        self.__menu_image = resize_image(self.__menu_image_path, self.buttons_width, self.buttons_height)
        self.__add_image = resize_image(self.__add_image_path, self.buttons_width, self.buttons_height)
        self.__save_image = resize_image(self.__save_image_path, self.buttons_width, self.buttons_height)
        self.__key_image = resize_image(self.__key_image_path, self.buttons_width, self.buttons_height)
        self.__config_image = resize_image(self.__config_image_path, self.buttons_width, self.buttons_height)
    
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