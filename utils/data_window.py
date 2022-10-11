import os
import tkinter as tk
from tkinter import ttk

from enum import Enum, auto
from typing import Callable

from img_utils import resize_image, change_img_colors

class gui_state(Enum):
    CLOSE = auto
    DEFAULT = auto()
    USER_PASS = auto()

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
        self.border: int = 0
        
        self.__default_menu_bg_color: str = "#3a7ff6"           # Default color bg (permanent)
        self.__default_fg_color: str = "#000000"                # Default color fg (permanent)
        self.__highlighted_fg_menu_color: str = "#000000"       # highlighted bg color when mouse on button (temporal)
        self.__highlighted_bg_menu_color: str = "#87d2fa"       # highlighted bg color when mouse on button (temporal)
        self.font = "Times"
        self.font_size_n = 12
        self.font_size_h1 = 15
        self.button_create_fg_color = "#ff7777"
        self.button_load_fg_color = "#87d2fa"
        self.bg_color = "#1e1e1e"
        
        self.__resources_dir = r"resources"
        self.__all_buttons_states = [
            buttons_state.MENU,
            buttons_state.ADD,
            buttons_state.SAVE,
            buttons_state.KEY,
            buttons_state.CONFIG
        ]
        self.__all_imgs_path = [
            os.path.join(self.__resources_dir, "menu.png"),
            os.path.join(self.__resources_dir, "add.png"),
            os.path.join(self.__resources_dir, "save.png"),
            os.path.join(self.__resources_dir, "key.png"),
            os.path.join(self.__resources_dir, "config.png")
        ]
        self.__all_imgs = []
        self.Buttons_win = []
        self.Buttons_menu = []
    
    def printo(self):
        print("button")
        
    def __create_menu_buttons(self, window: tk.Frame, text: str, image, command: Callable, relx: float, rely: float) -> tk.Button:
        button = tk.Button(window,
                                text = text,
                                width=self.buttons_width,
                                height=self.buttons_height,
                                border=self.border,
                                highlightthickness=3,
                                activebackground=self.__highlighted_bg_menu_color,
                                activeforeground=self.__highlighted_fg_menu_color,
                                bg = self.__default_menu_bg_color,
                                image=image,
                                command = command
                                )
                                   
        button.place(relx=relx, rely=rely)
        return button
    
    def __create_main_buttons(self, window: tk.Frame, text: str, grid_row_cont: int) -> tk.Button:
        button = tk.Button(window,
                            text=text,
                            border=self.border,
                            relief=tk.SUNKEN,
                            anchor="nw",
                            justify="left",
                            font=(self.font, self.font_size_n),
                            fg = self.button_create_fg_color,
                            bg = self.bg_color,
                            activebackground = self.button_create_fg_color,
                            activeforeground = self.bg_color
                            )
        button.grid(row = grid_row_cont, sticky=tk.E+tk.W)
        return button
    
    def __create_menu(self, window: tk.Frame) -> None:
        if self.Buttons_menu == []:
            menu      = ["menu", "add", "save", "key", "config"]
            functions = [self.printo]*5
            for mnu, funct, img in zip(menu, functions, self.__all_imgs):
                button = self.__create_menu_buttons(window, mnu, img, funct, 0, 0.1)
                button.pack()
                self.Buttons_menu.append([button])
            for btn, stt in zip(self.Buttons_menu, self.__all_buttons_states):
                self.__on_menu_buttons(button=btn[0], primary_color= self.__highlighted_fg_menu_color, secundary_color=self.__highlighted_bg_menu_color, state=stt)
    
    def __on_menu_buttons(self, button: tk.Button, state: buttons_state, primary_color: str, secundary_color: str = None) -> None:
        button.bind("<Enter>", lambda event: self.__on_menu_mouse(button, state, primary_color, secundary_color))
        button.bind("<Leave>", lambda event: self.__on_menu_mouse(button, state, self.__default_fg_color, self.__default_menu_bg_color))
    
    def __on_main_buttons(self, i , j, button: tk.Button, primary_color: str, secundary_color: str = None) -> None:
        button.bind("<Enter>", lambda event: self.__on_main_mouse(button, primary_color, secundary_color))
        button.bind("<Leave>", lambda event: self.__on_main_mouse(button, secundary_color, primary_color))
    
    def __on_menu_mouse(self, button: tk.Button, state: buttons_state, primary_color: str, secundary_color) -> None:
        if secundary_color is None:
            secundary_color = self.__default_menu_bg_color
        for i, button_state in enumerate(self.__all_buttons_states):
            if state != button_state:
                continue
            self.__all_imgs[i] = change_img_colors(self.__all_imgs_path[i], primary_color, secundary_color, self.buttons_width, self.buttons_height)
            button.config(image = self.__all_imgs[i])
            
    def __on_main_mouse(self, button: tk.Button, fg: str, bg: str) -> None:
        button.config(bg = bg, fg = fg)
            
    def load_dict(self, dicto: dict) -> None:
        self.__dicto = dicto
        
    def __load_images(self) -> None:
        if self.__all_imgs != []: return
        for img in self.__all_imgs_path:
            self.__all_imgs.append([resize_image(img, width = self.buttons_width, height=self.buttons_height)])
    
    def __button_index_helper_first_doubcl(self, i:int, j:int) -> None:
        state = self.Buttons_win[i][1][1]
        button_text_bool = "Password" in self.Buttons_win[i][0][j]["text"]
        label_text_bool = "User" not in self.Buttons_win[i][0][j]["text"] and not button_text_bool
        
        if state == gui_state.DEFAULT and label_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event, i=i, j=j: self.__expand_gui_num_users(i, j))
        elif state == gui_state.CLOSE and label_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event: self.__default_gui_data_to_screen())
        elif state == gui_state.USER_PASS and button_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event: self.__hide_show_password(i, j))
        self.__update_main_buttons()
            
    def __hide_show_password(self, i, j):
        key = self.Buttons_win[i][1][0]
        text = self.Buttons_win[i][0][j]["text"].split()[-1]
        text_len = len(text)
        password = "Password: "
        if "*"*text_len == text:
            password +=  self.__dicto[key][(j-1)//2+1]["password"]
        else:
            password += "*"*text_len
        self.Buttons_win[i][0][j].config(text = password)
        
    def __expand_gui_num_users(self, i:int, j: int) -> None:
        key = self.Buttons_win[i][1][0]
        self.Buttons_win[i][0][1].destroy()
        self.Buttons_win[i][1][1] = gui_state.USER_PASS
        del(self.Buttons_win[i][0][1])
        grid_row_cont = self.Buttons_win[i][2][0] + 1
        
        for num_users in range(1, len(self.__dicto[key]) + 1):
            user = self.__dicto[key][num_users]["user"]
            user = f"User: {user}"
            password = self.__dicto[key][num_users]["password"]
            password = len(password)*"*"
            password = f"Password: {password}"
            user_button = self.__create_main_buttons(self.win, user, grid_row_cont)
            self.Buttons_win[i][0].append(user_button)
            password_button = self.__create_main_buttons(self.win, password, grid_row_cont + 1)
            self.Buttons_win[i][0].append(password_button)
            grid_row_cont += 2
        
        for i in range(len(self.Buttons_win)):
            for j in range(1, len(self.Buttons_win[i][0])):
                self.Buttons_win[i][0][j].config(command = lambda i=i, j=j: self.__button_index_helper_first_doubcl(i, j))
        self.__update_main_buttons()
        
    def __default_gui_data_to_screen(self) -> None:
        ################# reduce
        grid_cont = 0
        for key in self.__dicto:
            site = f"\n{key}"
            num_users = f"# Users: {len(self.__dicto[key])}"
            next_grid_cont = grid_cont + len(self.__dicto[key])*2
            Label_site = tk.Button(self.win,
                                   text=site,
                                   border=self.border,
                                   relief=tk.SUNKEN,
                                   anchor=tk.CENTER,
                                   justify=tk.CENTER,
                                   width=25,
                                   font=(self.font, self.font_size_h1),
                                   fg = self.button_create_fg_color,
                                   bg = self.bg_color,
                                   activebackground = self.button_create_fg_color,
                                   activeforeground = self.bg_color
                                   )
            Label_site.grid(row = grid_cont, column = 0, sticky=tk.E+tk.W)
            button_site = tk.Button(self.win,
                                    text=num_users,
                                    border=self.border,
                                    relief=tk.SUNKEN,
                                    anchor=tk.W,
                                    justify="left",
                                    font=(self.font, self.font_size_n),
                                    fg = self.button_create_fg_color,
                                    bg = self.bg_color,
                                    activebackground = self.button_create_fg_color,
                                    activeforeground = self.bg_color
                                    )
            button_site.grid(row = next_grid_cont, column = 0, sticky=tk.E+tk.W)

            self.Buttons_win.append([
                [Label_site, button_site],
                [key, gui_state.DEFAULT],
                [grid_cont, next_grid_cont]
                ]
            )
            grid_cont = 1 + next_grid_cont
            
        for i in range(len(self.Buttons_win)):
            for j in range(len(self.Buttons_win[i][0])):
                self.Buttons_win[i][0][j].config(command = lambda i=i, j=j: self.__button_index_helper_first_doubcl(i, j))
        self.__update_main_buttons()
        
    def __update_scrollbar(self, event) -> None:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def __update_main_buttons(self) -> None:
        for i in range(len(self.Buttons_win)):
            for j in range(len(self.Buttons_win[i][0])):
                self.__on_main_buttons(i, j, self.Buttons_win[i][0][j], self.bg_color, self.button_create_fg_color)
            
    def __set_scrollbar(self, window: tk.Frame) -> None:
        self.main = tk.Frame(window, bg = self.bg_color, background=self.bg_color)
        self.main.pack(side = tk.RIGHT, fill=tk.BOTH)
        self.canvas = tk.Canvas(self.main, bg = self.bg_color, background=self.bg_color, highlightthickness = 0)
        my_scrollbar = ttk.Scrollbar(self.main,
                                     orient = tk.VERTICAL,
                                     command = self.canvas.yview)
        my_scrollbar.pack(side = tk.RIGHT, fill = tk.Y, anchor="e")
        
        self.canvas.pack(side = tk.LEFT, fill=tk.BOTH)
        self.canvas.configure(yscrollcommand=my_scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.win = tk.Frame(self.canvas, bg = self.bg_color, background=self.bg_color)
        #self.canvas.create_window((0,0), window=self.win, anchor = "center")
        self.canvas.create_window((self.buttons_width,0), window=self.win, anchor = "nw")
    
    def window(self) -> None:
        self.root=tk.Tk()
        self.root.configure(bg = self.bg_color, background=self.bg_color)
        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinates = screen_width//2 - self.width//2
        y_coordinates = screen_height//2 - self.height//2
        self.root.title("SecKey")
        self.geometry = f"{str(self.width)}x{str(self.height)}+{x_coordinates}+{y_coordinates}"
        self.root.iconphoto(False, tk.PhotoImage(file=os.path.join(self.__resources_dir,"sk.png")))
        #self.root.wm_attributes('-toolwindow', 'True') # Hide icon
        self.root.resizable(width=False, height=False)
        # Set the geometry of the window
        self.root.geometry(self.geometry)
        
        self.menu = tk.Frame(self.root,
                             width=self.menu_width,
                             height=self.menu_weight,
                             background=self.__default_menu_bg_color,
                             bg = self.__default_menu_bg_color)
        self.menu.pack(side=tk.LEFT ,fill=tk.BOTH)
        
        self.load_dict(example_dict)

        self.__load_images()
        self.__create_menu(self.menu)
        self.__set_scrollbar(self.root)
        self.__default_gui_data_to_screen()
        self.win.bind("<Configure>", self.__update_scrollbar)
        self.root.mainloop()

A = data_window()
example_dict = {
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