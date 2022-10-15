import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from enum import Enum, auto
from typing import Callable
from abc import abstractmethod

from img_utils import resize_image, change_img_colors
from dec import EaD # Encript and Decript

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

class create_windows_abs():
    buttons_width: int = 40
    buttons_height: int = buttons_width
    border: int = 0
    bg_color = "#1e1e1e"
    def __init__(self) -> None:
        self.resources_dir = r"resources"
        self.dicto = None
        
    @abstractmethod
    def create_buttons(self, *args):
        pass
    @abstractmethod
    def create_main_window(self, *args):
        pass
    @abstractmethod
    def create_scrollbar(self, *args):
        pass
    @abstractmethod
    def default_gui(self, *args):
        pass
    def load_dict(self, dicto: dict):
        self.dicto = dicto
    def test(self):
        print("print")

class create_root(create_windows_abs):
    width: int  = 300
    height: int = 400
    font_size_n = 12
    font_size_h1 = 15
    font = "Times"
    bg_color = "#1e1e1e"
    button_create_fg_color = "#ff7777"
    
    def __init__(self) -> None:
        super().__init__()
        self.title = "SecKey"
        self.resources_dir = r"resources"
        self.Buttons_win = []
        
    def create_buttons(self, window: tk.Frame, text: str, grid_row_cont: int, anchor: tk = tk.NW ,justify: tk = tk.LEFT, font_size = None, width:int = -1) -> tk.Button:
        if not font_size: font_size = self.font_size_n
        button = tk.Button(window,
                            text=text,
                            border=self.border,
                            relief=tk.SUNKEN,
                            anchor=anchor,
                            justify=justify,
                            font=(self.font, font_size),
                            fg = self.button_create_fg_color,
                            bg = self.bg_color,
                            activebackground = self.button_create_fg_color,
                            activeforeground = self.bg_color
                            )
        if width > 0:
            button.config(width=width)
        button.grid(row = grid_row_cont, sticky=tk.E+tk.W)
        return button
    
    def create_main_window(self) -> tk.Tk:
        self.root=tk.Tk()
        self.root.configure(bg = self.bg_color, background=self.bg_color)
        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinates = screen_width//2 - self.width//2
        y_coordinates = screen_height//2 - self.height//2
        self.root.title(self.title)
        self.geometry = f"{str(self.width)}x{str(self.height)}+{x_coordinates}+{y_coordinates}"
        self.root.iconphoto(False, tk.PhotoImage(file=os.path.join(self.resources_dir,"sk.png")))
        #self.root.wm_attributes('-toolwindow', 'True') # Hide icon
        self.root.resizable(width=False, height=False)
        # Set the geometry of the window
        self.root.geometry(self.geometry)
        return self.root

    def loop(self):
        self.root.mainloop()
    
    def __on_buttons(self, i , j, button: tk.Button, primary_color: str, secundary_color: str = None) -> None:
        button.bind("<Enter>", lambda event: self.__on_mouse(button, primary_color, secundary_color))
        button.bind("<Leave>", lambda event: self.__on_mouse(button, secundary_color, primary_color))
    
    def __on_mouse(self, button: tk.Button, fg: str, bg: str) -> None:
        button.config(bg = bg, fg = fg)

    def __button_index_helper_first_doubcl(self, i:int, j:int) -> None:
        state = self.Buttons_win[i][1][1]
        button_text_bool = "Password" in self.Buttons_win[i][0][j]["text"]
        label_text_bool = "User" not in self.Buttons_win[i][0][j]["text"] and not button_text_bool
        button_expanded = len(self.Buttons_win[i][0]) > 2
        if state == gui_state.DEFAULT and label_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event, i=i, j=j: self.__expand_gui_num_users(i, j))
        elif state == gui_state.CLOSE and label_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event: self.__default_gui())
        elif state == gui_state.USER_PASS and button_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event: self.__hide_show_password(i, j))
        elif state == gui_state.USER_PASS and label_text_bool and button_expanded:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event, i=i: self.__contract_gui_num_users(i))
        self.__update_main_buttons()
            
    def __hide_show_password(self, i, j):
        key = self.Buttons_win[i][1][0]
        text = self.Buttons_win[i][0][j]["text"].split()[-1]
        text_len = len(text)
        password = "Password: "
        if "*"*text_len == text:
            password +=  self.dicto[key][(j-1)//2+1]["password"]
        else:
            password += "*"*text_len
        self.Buttons_win[i][0][j].config(text = password)
    
    def __contract_gui_num_users(self, i: int):
        grid_cont = self.Buttons_win[i][2][0]
        last_grid = self.Buttons_win[i][2][1]
        key = self.Buttons_win[i][1][0]
        site = f"\n{key}"
        num_users = f"# Users: {len(self.dicto[key])}"
        next_grid_cont = grid_cont + len(self.dicto[key])*2
        [self.Buttons_win[i][0][j].destroy() for j in range(1, len(self.Buttons_win[i][0]))]
        del((self.Buttons_win[i][0][1:]))
        print(self.Buttons_win[i][0])
        Label_site = self.create_buttons(self.win, site, grid_cont, anchor=tk.CENTER ,justify=tk.CENTER, font_size = self.font_size_h1, width=25)
        button_site = self.create_buttons(self.win, num_users, next_grid_cont, anchor=tk.W , font_size = self.font_size_n)
        
        self.Buttons_win[i][0] = [Label_site, button_site]
        self.Buttons_win[i][1][1] = gui_state.DEFAULT
        self.Buttons_win[i][2] = [grid_cont, last_grid]

        for i in range(len(self.Buttons_win)):
            for j in range(len(self.Buttons_win[i][0])):
                self.Buttons_win[i][0][j].config(command = lambda i=i, j=j: self.__button_index_helper_first_doubcl(i, j))
        self.__update_main_buttons()
        
    def __expand_gui_num_users(self, i:int, j: int) -> None:
        key = self.Buttons_win[i][1][0]
        self.Buttons_win[i][0][1].destroy()
        self.Buttons_win[i][1][1] = gui_state.USER_PASS
        del(self.Buttons_win[i][0][1])
        grid_row_cont = self.Buttons_win[i][2][0] + 1
        
        for num_users in range(1, len(self.dicto[key]) + 1):
            user = self.dicto[key][num_users]["user"]
            user = f"User: {user}"
            password = self.dicto[key][num_users]["password"]
            password = len(password)*"*"
            password = f"Password: {password}"
            user_button = self.create_buttons(self.win, user, grid_row_cont)
            self.Buttons_win[i][0].append(user_button)
            password_button = self.create_buttons(self.win, password, grid_row_cont + 1)
            self.Buttons_win[i][0].append(password_button)
            grid_row_cont += 2
        
        for i in range(len(self.Buttons_win)):
            for j in range(1, len(self.Buttons_win[i][0])):
                self.Buttons_win[i][0][j].config(command = lambda i=i, j=j: self.__button_index_helper_first_doubcl(i, j))
        self.__update_main_buttons()
    
    def default_gui(self, win) -> None:
        self.win = win
        grid_cont = 0
        for key in self.dicto:
            site = f"\n{key}"
            num_users = f"# Users: {len(self.dicto[key])}"
            next_grid_cont = grid_cont + len(self.dicto[key])*2
            Label_site = self.create_buttons(self.win, site, grid_cont, anchor=tk.CENTER ,justify=tk.CENTER, font_size = self.font_size_h1, width=25)
            button_site = self.create_buttons(self.win, num_users, next_grid_cont, anchor=tk.W , font_size = self.font_size_n)

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
    
    def __update_main_buttons(self) -> None:
        for i in range(len(self.Buttons_win)):
            for j in range(len(self.Buttons_win[i][0])):
                self.__on_buttons(i, j, self.Buttons_win[i][0][j], self.bg_color, self.button_create_fg_color)
    
class create_menu(create_windows_abs):
    width: int = 50
    height: int = 400
    default_bg_color: str = "#3a7ff6"
    highlighted_fg_color: str = "#000000"
    highlighted_bg_color: str = "#87d2fa"
    default_fg_color: str = "#000000"
    def __init__(self) -> None:
        super().__init__()
        self.all_buttons_states = [
            buttons_state.MENU,
            buttons_state.ADD,
            buttons_state.SAVE,
            buttons_state.KEY,
            buttons_state.CONFIG
        ]
        self.Buttons_menu = []
        self.all_imgs_path = [
            os.path.join(self.resources_dir, "menu.png"),
            os.path.join(self.resources_dir, "add.png"),
            os.path.join(self.resources_dir, "save.png"),
            os.path.join(self.resources_dir, "key.png"),
            os.path.join(self.resources_dir, "config.png")
        ]
        self.all_imgs = self.__load_images()
    
    def create_buttons(self, window: tk.Frame, text: str, image, command: Callable, relx: float, rely: float) -> tk.Button:
        button = tk.Button(window,
                                text = text,
                                width=self.buttons_width,
                                height=self.buttons_height,
                                border=self.border,
                                highlightthickness=3,
                                activebackground=self.highlighted_bg_color,
                                activeforeground=self.highlighted_fg_color,
                                bg = self.default_bg_color,
                                image=image,
                                command = command
                                )
        button.place(relx=relx, rely=rely)
        return button
        
    def create_main_window(self, root: tk.Frame) -> tk.Frame:
        self.menu = tk.Frame(root,
                             width=self.width,
                             height=self.height,
                             background=self.default_bg_color,
                             bg = self.default_bg_color)
        self.menu.pack(side=tk.LEFT ,fill=tk.BOTH)
        return self.menu
    
    def default_gui(self) -> None:
        if self.Buttons_menu == []:
            menu      = ["menu", "add", "save", "key", "config"]
            functions = [self.test]*5
            for mnu, funct, img in zip(menu, functions, self.all_imgs):
                button = self.create_buttons(self.menu, mnu, img, funct, 0, 0.1)
                button.pack()
                self.Buttons_menu.append([button])
            for btn, stt in zip(self.Buttons_menu, self.all_buttons_states):
                self.__on_buttons(button=btn[0], primary_color= self.highlighted_fg_color, secundary_color=self.highlighted_bg_color, state=stt)

    def __load_images(self) -> None:
        imgs = []
        if imgs != []: return
        for img in self.all_imgs_path:
            imgs.append([resize_image(img, width = self.buttons_width, height=self.buttons_height)])
        return imgs
    
    def __on_buttons(self, button: tk.Button, state: buttons_state, primary_color: str, secundary_color: str = None) -> None:
        button.bind("<Enter>", lambda event: self.__on_mouse(button, state, primary_color, secundary_color))
        button.bind("<Leave>", lambda event: self.__on_mouse(button, state, self.default_fg_color, self.default_bg_color))
        
    def __on_mouse(self, button: tk.Button, state: buttons_state, primary_color: str, secundary_color) -> None:
        if secundary_color is None:
            secundary_color = self.default_bg_color
        for i, button_state in enumerate(self.all_buttons_states):
            if state != button_state:
                continue
            self.all_imgs[i] = change_img_colors(self.all_imgs_path[i], primary_color, secundary_color, self.buttons_width, self.buttons_height)
            button.config(image = self.all_imgs[i])

class create_scrollbar(create_windows_abs):
    def __init__(self) -> None:
         super().__init__()
         
    def create_scrollbar(self, window: tk.Frame) -> None:
        self.main = tk.Frame(window, bg = self.bg_color, background=self.bg_color)
        self.main.pack(side = tk.RIGHT, fill=tk.BOTH)
        self.canvas = tk.Canvas(self.main, bg = self.bg_color, background=self.bg_color, highlightthickness = 0)
        self.scrollbar = ttk.Scrollbar(self.main,
                                     orient = tk.VERTICAL,
                                     command = self.canvas.yview)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y, anchor=tk.E)
        
        self.canvas.pack(side = tk.LEFT, fill=tk.BOTH)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.win = tk.Frame(self.canvas, bg = self.bg_color, background=self.bg_color)
        self.canvas.create_window((create_menu.width*10,0), window=self.win, anchor = tk.NE)
        self.update_scrollbar()
        return self.win, self.canvas, self.scrollbar
    
    def __set_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
    
    def __update_scrollbar(self, event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def update_scrollbar(self):
        self.win.bind("<Configure>", self.__update_scrollbar)
        self.canvas.bind_all("<MouseWheel>", self.__set_mousewheel)
    
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
file_path = r"file_encripted.bin"
A = create_root()#data_window(example_dict, file_path)
A.load_dict(example_dict)
root_window = A.create_main_window()
B = create_menu()
menu_window = B.create_main_window(root_window)
scrollbar = create_scrollbar()
win, canvas, scrollbar_root = scrollbar.create_scrollbar(root_window)
B.default_gui()
A.default_gui(win)
A.loop()