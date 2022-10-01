import os
import tkinter as tk
from tkinter import ttk

from enum import Enum, auto
from typing import Callable

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
        self.width: int  = 300
        self.height: int = 400
        self.menu_width: int = 50
        self.menu_weight: int = 400
        self.menu_buttons_step: int = self.height // 6
        self.buttons_width: int = 40
        self.buttons_height: int = self.buttons_width
        
        self.__default_bg_color: str = "#3a7ff6"         # Default color bg (permanent)
        self.__default_fg_color: str = "#000000"         # Default color fg (permanent)
        self.__highlighted_fg_color: str = "#ff0000"    # highlighted bg color when mouse on button (temporal)
        self.__highlighted_bg_color: str = "#0000ff"    # highlighted bg color when mouse on button (temporal)
        
        self.__resources_dir = r"resources"
        self.__menu_image_path = os.path.join(self.__resources_dir, "menu.png")
        self.__add_image_path = os.path.join(self.__resources_dir, "add.png")
        self.__save_image_path = os.path.join(self.__resources_dir, "save.png")
        self.__key_image_path = os.path.join(self.__resources_dir, "key.png")
        self.__config_image_path = os.path.join(self.__resources_dir, "config.png")
    
    def printo(self):
        print("button")
        
    def __create_buttons(self, window: tk.Frame, text: str, image, command: Callable, relx: float, rely: float) -> tk.Button:
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
    
    def __create_menu(self, window: tk.Frame) -> None:
        menu_button = self.__create_buttons(window, "menu", self.__menu_image, self.printo, 0, 0.1)
        menu_button.pack()
        menu_button.config(image=self.__menu_image)
        add_button = self.__create_buttons(window, "add", self.__add_image, self.printo, 0, 0.2)
        add_button.pack()
        save_button = self.__create_buttons(window, "save", self.__save_image, self.printo, 0, 0.3)
        save_button.pack()
        key_button = self.__create_buttons(window, "key", self.__key_image, self.printo, 0, 0.4)
        key_button.pack()
        config_button = self.__create_buttons(window, "config", self.__config_image, self.printo, 0, 0.5)
        config_button.pack()
        
        self.__on_button(button=menu_button, primary_color= self.__highlighted_fg_color, secundary_color=self.__highlighted_bg_color, state= buttons_state.MENU)
        self.__on_button(button=add_button, primary_color= self.__highlighted_fg_color, secundary_color=self.__highlighted_bg_color, state= buttons_state.ADD)
        self.__on_button(button=save_button, primary_color= self.__highlighted_fg_color, secundary_color=self.__highlighted_bg_color, state= buttons_state.SAVE)
        self.__on_button(button=key_button, primary_color= self.__highlighted_fg_color, secundary_color=self.__highlighted_bg_color, state= buttons_state.KEY)
        self.__on_button(button=config_button, primary_color= self.__highlighted_fg_color, secundary_color=self.__highlighted_bg_color, state= buttons_state.CONFIG)
        
    def __load_images(self) -> None:
        self.__menu_image = resize_image(self.__menu_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__add_image = resize_image(self.__add_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__save_image = resize_image(self.__save_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__key_image = resize_image(self.__key_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__config_image = resize_image(self.__config_image_path, width = self.buttons_width, height=self.buttons_height)
    
    def __button_index_helper(self, i:int) -> None:
        self.Buttons_win[i][0].bind('<Double-Button-1>', lambda event: self.__double_click(i))
        
    def __double_click(self, i:int) -> None:
        key = self.Buttons_win[i][1]
        
        ####################### text is for update buttons when double click
        if self.Buttons_win[i][2][0] == False and self.Buttons_win[i][2][2] != "":
            text = self.Buttons_win[i][2][2]
            self.Buttons_win[i][2][0] = True
        elif self.Buttons_win[i][2][0] == True and self.Buttons_win[i][2][2] != "":
            text = self.Buttons_win[i][2][1]
            self.Buttons_win[i][2][0] = False
        elif self.Buttons_win[i][2][0] == False and self.Buttons_win[i][2][2] == "":
            ################### 
            new_text = f""""""
            for j in range(len(self.__dicto[key])):
                num_users = j + 1
                user = self.__dicto[key][num_users]["user"]
                password = self.__dicto[key][num_users]["password"]
                new_text += f"""
                User: {user}
                Password: {password}
                """
            text = f"""
                Site: {key}
                {new_text}
                """
            self.Buttons_win[i][2][2] = text
            self.Buttons_win[i][2][0] = True
        self.Buttons_win[i][0].config(text=text)
        
    def __update_data_to_screen(self, dict: dict) -> None:
        self.__dicto = dict
        self.Buttons_win = []
        for key in self.__dicto:
            site = key
            
            text = f"""
            Site: {site}
            # Users: {len(self.__dicto[key])}
            """
            
            button_site = tk.Button(self.win,text=text, border=0, relief=tk.SUNKEN, anchor="w", justify="left") ########### Fix this
            button_site.pack(fill = "both")
            
            self.Buttons_win.append([
                button_site,
                key,
                [False, text, ""] # what text is shown, default text, new text.
                ]
            )
        for i in range(len(self.Buttons_win)):
            self.Buttons_win[i][0].config(command = lambda i=i: self.__button_index_helper(i))
        
    def __update_scrollbar(self, event) -> None:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
    def __set_scrollbar(self, window: tk.Frame) -> None:
        self.main = tk.Frame(window)
        self.main.pack(side = tk.RIGHT, fill=tk.BOTH)
        
        self.canvas = tk.Canvas(self.main)
        my_scrollbar = ttk.Scrollbar(self.main, orient = tk.VERTICAL, command = self.canvas.yview)
        my_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.canvas.pack(side = tk.LEFT, fill=tk.BOTH)

        self.canvas.configure(yscrollcommand=my_scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.win = tk.Frame(self.canvas)
        #self.win.pack(side = tk.LEFT)
        self.canvas.create_window((self.buttons_width,0), window=self.win, anchor = "nw")
    
    def window(self) -> None:
        self.root=tk.Tk()
        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinates = screen_width//2 - self.width//2
        y_coordinates = screen_height//2 - self.height//2
        self.root.title("SecKey")
        self.geometry = f"{str(self.width)}x{str(self.height)}+{x_coordinates}+{y_coordinates}"
        self.root.iconphoto(False, tk.PhotoImage(file=os.path.join(self.__resources_dir,"sk.png")))
        #self.root.wm_attributes('-toolwindow', 'True') # Hide icon
        #self.root.resizable(width=False, height=False)
        # Set the geometry of the window
        self.root.geometry(self.geometry)
        
        self.menu = tk.Frame(self.root, width=self.menu_width, height=self.menu_weight ,background=self.__default_bg_color)
        #self.menu.pack(side=tk.LEFT ,fill=tk.BOTH, expand=1)
        self.menu.pack(side=tk.LEFT ,fill=tk.BOTH)

        self.__load_images()
        self.__create_menu(self.menu)
        self.__set_scrollbar(self.root)
        self.__update_data_to_screen(example_dict)
        self.win.bind("<Configure>", self.__update_scrollbar)
        self.root.mainloop()

A = data_window()
example_dict = { # Global variable fix function's local variables __update_data_to_screen when finish
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