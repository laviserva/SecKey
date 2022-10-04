import os
import tkinter as tk
from tkinter import ttk

from enum import Enum, auto
from typing import Callable

from img_utils import resize_image, change_img_colors

class gui_state(Enum):
    CLOSE = auto
    DEFAULT = auto()
    USER_PASS_CENSURED = auto()
    USER_PASS_UNCENSURED = auto()

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
        self.border: int = 1
        
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
                                border=self.border,
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
        
    def load_dict(self, dicto: dict) -> None:
        self.__dicto = dicto
        
    def __load_images(self) -> None:
        self.__menu_image = resize_image(self.__menu_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__add_image = resize_image(self.__add_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__save_image = resize_image(self.__save_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__key_image = resize_image(self.__key_image_path, width = self.buttons_width, height=self.buttons_height)
        self.__config_image = resize_image(self.__config_image_path, width = self.buttons_width, height=self.buttons_height)
    
    def __button_index_helper_first_doubcl(self, i:int, j:int) -> None:
        print(self.Buttons_win[i])
        state = self.Buttons_win[i][1][1]
        button_text_bool = "Password" in self.Buttons_win[i][0][j]["text"]
        label_text_bool = "User" not in self.Buttons_win[i][0][j]["text"] and not button_text_bool
        if state == gui_state.DEFAULT and label_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event: self.__expand_gui_num_users(i, j))
        elif state == gui_state.CLOSE and label_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event: self.__default_gui_data_to_screen())
        elif state == gui_state.USER_PASS_CENSURED and button_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event: self.__expand_gui_users_pass())
        elif state == gui_state.USER_PASS_UNCENSURED and button_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event: self.__show_password(i, j))
            
    def __show_password(self, i, j):
        print(i)
        print(j)
        key = self.Buttons_win[i][1][0]
        password = "Password: " + self.__dicto[key][(j-1)//2+1]["password"]
        self.Buttons_win[i][0][j].config(text = password)
                
    def __expand_gui_num_users(self, i:int, j: int) -> None:
        key = self.Buttons_win[i][1][0]
        self.Buttons_win[i][0][1].destroy()
        self.Buttons_win[i][1][1] = gui_state.USER_PASS_UNCENSURED
        del(self.Buttons_win[i][0][1])
        grid_row_cont = self.Buttons_win[i][2][0] + 1
        
        for num_users in range(1, len(self.__dicto[key]) + 1):
            user = self.__dicto[key][num_users]["user"]
            user = f"User: {user}"
            password = self.__dicto[key][num_users]["password"]
            password = len(password)*"*"
            password = f"Password: {password}"
            #text += f"User: {user}\nPassword: {password}\n"
            user_button = tk.Button(self.win,text=user, border=self.border, relief=tk.SUNKEN, anchor="nw", justify="left")
            user_button.grid(row = grid_row_cont, sticky=tk.E+tk.W)
            self.Buttons_win[i][0].append(user_button)
            password_button = tk.Button(self.win,text=password, border=self.border, relief=tk.SUNKEN, anchor="nw", justify="left")
            password_button.grid(row = grid_row_cont + 1, sticky=tk.E+tk.W)
            self.Buttons_win[i][0].append(password_button)
            grid_row_cont += 2
        
        for i in range(len(self.Buttons_win)):
            for j in range(1, len(self.Buttons_win[i][0])):
                self.Buttons_win[i][0][j].config(command = lambda i=i, j=j: self.__button_index_helper_first_doubcl(i, j))
    def __expand_gui_users_pass(self) -> None:
        self.printo()
        
        
    def __default_gui_data_to_screen(self) -> None:
        self.Buttons_win = []
        grid_cont = 0
        for key in self.__dicto:
            site = f"\n{key}"
            num_users = f"# Users: {len(self.__dicto[key])}"
            
            next_grid_cont = grid_cont + len(self.__dicto[key])*2
            
            Label_site = tk.Button(self.win,text=site, border=self.border, relief=tk.SUNKEN, anchor=tk.CENTER, justify=tk.CENTER, font=30, width=25)
            Label_site.grid(row = grid_cont, column = 0, sticky=tk.E+tk.W)
            button_site = tk.Button(self.win,text=num_users, border=self.border, relief=tk.SUNKEN, anchor=tk.W, justify="left")
            button_site.grid(row = next_grid_cont, column = 0, sticky=tk.E+tk.W)

            self.Buttons_win.append([
                [Label_site, button_site],
                [key, gui_state.DEFAULT],
                [grid_cont, next_grid_cont] # grid of Site, Grid of last password before site's grid
                ]
            )
            grid_cont = 1 + next_grid_cont
            
        for i in range(len(self.Buttons_win)):
            for j in range(len(self.Buttons_win[i][0])):
                self.Buttons_win[i][0][j].config(command = lambda i=i, j=j: self.__button_index_helper_first_doubcl(i, j))
        
    def __update_scrollbar(self, event) -> None:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
    def __set_scrollbar(self, window: tk.Frame) -> None:
        self.main = tk.Frame(window)
        self.main.pack(side = tk.RIGHT, fill=tk.BOTH)
        self.canvas = tk.Canvas(self.main)
        my_scrollbar = ttk.Scrollbar(self.main, orient = tk.VERTICAL, command = self.canvas.yview)
        my_scrollbar.pack(side = tk.RIGHT, fill = tk.Y, anchor="e")
        
        self.canvas.pack(side = tk.LEFT, fill=tk.BOTH)
        self.canvas.configure(yscrollcommand=my_scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.win = tk.Frame(self.canvas)
        #self.canvas.create_window((0,0), window=self.win, anchor = "center")
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
        
        self.load_dict(example_dict)

        self.__load_images()
        self.__create_menu(self.menu)
        self.__set_scrollbar(self.root)
        self.__default_gui_data_to_screen()
        self.win.bind("<Configure>", self.__update_scrollbar)
        self.root.mainloop()

A = data_window()
example_dict = { # Global variable fix function's local variables __default_gui_data_to_screen when finish
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