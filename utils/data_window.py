import os
import tkinter as tk

from enum import Enum, auto

from img_utils import resize_image, change_img_colors

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
        self.buttons_height = self.buttons_width
        
        self.__default_bg_color = "#3a7ff6"         # Default color bg (permanent)
        self.__default_fg_color = "#000000"         # Default color fg (permanent)
        self.__highlighted_fg_color = "#ff0000"    # highlighted bg color when mouse on button (temporal)
        self.__highlighted_bg_color = "#0000ff"    # highlighted bg color when mouse on button (temporal)
        
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
                                highlightthickness=3,
                                activebackground=self.__highlighted_bg_color,
                                activeforeground=self.__highlighted_fg_color,
                                bg = self.__default_bg_color,
                                image=image,
                                command = command
                                )
        button.place(relx=relx, rely=rely)
        return button
    
    def __on_button(self, button: tk.Button, state: buttons_state, primary_color: str, secundary_color: str = None) -> None:
        button.bind("<Enter>", lambda event: self.__on_enter_mouse(button, state, primary_color, secundary_color))
        button.bind("<Leave>", lambda event: self.__on_leave_mouse(button, state, self.__default_fg_color))
    
    def __on_enter_mouse(self, button: tk.Button, state: buttons_state, primary_color: str, secundary_color: str = None) -> None:
        if secundary_color is None:
            secundary_color = self.__default_bg_color
        if state == buttons_state.MENU:
            self.__menu_image = change_img_colors(self.__menu_image_path, primary_color, secundary_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__menu_image)
        elif state == buttons_state.ADD:
            self.__add_image = change_img_colors(self.__add_image_path, primary_color, secundary_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__add_image)
        elif state == buttons_state.SAVE:
            self.__save_image = change_img_colors(self.__save_image_path, primary_color, secundary_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__save_image)
        elif state == buttons_state.KEY:
            self.__key_image = change_img_colors(self.__key_image_path, primary_color, secundary_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__key_image)
        elif state == buttons_state.CONFIG:
            self.__config_image = change_img_colors(self.__config_image_path, primary_color, secundary_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__config_image)
    
    def __on_leave_mouse(self, button: tk.Button, state: buttons_state, primary_color: str) -> None:
        if state == buttons_state.MENU:
            self.__menu_image = change_img_colors(self.__menu_image_path, primary_color, self.__default_bg_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__menu_image)
        elif state == buttons_state.ADD:
            self.__add_image = change_img_colors(self.__add_image_path, primary_color, self.__default_bg_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__add_image)
        elif state == buttons_state.SAVE:
            self.__save_image = change_img_colors(self.__save_image_path, primary_color, self.__default_bg_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__save_image)
        elif state == buttons_state.KEY:
            self.__key_image = change_img_colors(self.__key_image_path, primary_color, self.__default_bg_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__key_image)
        elif state == buttons_state.CONFIG:
            self.__config_image = change_img_colors(self.__config_image_path, primary_color, self.__default_bg_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__config_image)
    
    def __create_menu(self) -> None:
        self.menu = tk.Frame(self.win, width=self.menu_width, height=self.menu_weight ,background=self.__default_bg_color)
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
        
        self.__on_button(button=menu_button, primary_color= self.__highlighted_fg_color, secundary_color=self.__highlighted_bg_color, state= buttons_state.MENU)
        self.__on_button(button=add_button, primary_color= self.__highlighted_fg_color, secundary_color=self.__highlighted_bg_color, state= buttons_state.ADD)
        self.__on_button(button=save_button, primary_color= self.__highlighted_fg_color, secundary_color=self.__highlighted_bg_color, state= buttons_state.SAVE)
        self.__on_button(button=key_button, primary_color= self.__highlighted_fg_color, secundary_color=self.__highlighted_bg_color, state= buttons_state.KEY)
        self.__on_button(button=config_button, primary_color= self.__highlighted_fg_color, secundary_color=self.__highlighted_bg_color, state= buttons_state.CONFIG)
        
    def __load_images(self):
        self.__menu_image = resize_image(self.__menu_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__add_image = resize_image(self.__add_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__save_image = resize_image(self.__save_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__key_image = resize_image(self.__key_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__config_image = resize_image(self.__config_image_path, width = self.buttons_width, height=self.buttons_height)
    
    
    ################################################# Develoap
    def __double_click(self, button: tk.Button, dicto):
        text =f"""
        Site 01
        Users: {len(dicto["site 01"])}
        
        1:
        User: {dicto["site 01"][1]["user"]}
        Password: {dicto["site 01"][1]["password"]}
        """
        button.config(text=text)
        
    def frame_example(self, dicto: dict):
        label_data = dicto["site 01"]
        button_ejemplo = tk.Button(self.win,text=label_data, border=1, relief=tk.SUNKEN, anchor="w", justify="left")
        button_ejemplo.pack(fill = "both")
        button_ejemplo.bind('<Double-Button-1>', lambda event: self.__double_click(button_ejemplo, dicto))
        
    ################################################################
    
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
        self.frame_example(example_dict)
        self.win.mainloop()

A = data_window()
example_dict = { # Global variable fix function's local variables frame_example when finish
                'site 01':{
                    1:{'user': 'user1', 'password': 'pass1', 'token': 'token1'},
                    2: {'user': 'user3', 'password': 'pass3', 'token': 'token3'}},
                'site 02':{
                    1: {'user': 'user2', 'password': 'pass2'}},
                'site 04':{
                    1: {'user': 'user4', 'password': 'pass4'}}, 
                'site 10': {
                    1: {'user': 'user5', 'password': 'pass5'}}}

A.window()