import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from enum import Enum, auto
from turtle import width
from typing import Callable
from abc import abstractmethod

from img_utils import resize_image, change_img_colors
from dec import EaD # Encript and Decript

class create_windows_abs_state(Enum):
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
    def load_dict(dict: dict):
        global dicto
        dicto = dict
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
    button_load_fg_color = "#87d2fa"
    
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
        self.root.configure(bg = self.bg_color)
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
        if state == create_windows_abs_state.DEFAULT and label_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event, i=i, j=j: self.__expand_gui_num_users(i, j))
        elif state == create_windows_abs_state.CLOSE and label_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event: self.__default_gui())
        elif state == create_windows_abs_state.USER_PASS and button_text_bool:
            self.Buttons_win[i][0][j].bind('<Double-Button-1>', lambda event: self.__hide_show_password(i, j))
        elif state == create_windows_abs_state.USER_PASS and label_text_bool and button_expanded:
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
        Label_site = self.create_buttons(self.win, site, grid_cont, anchor=tk.CENTER ,justify=tk.CENTER, font_size = self.font_size_h1, width=25)
        button_site = self.create_buttons(self.win, num_users, next_grid_cont, anchor=tk.W , font_size = self.font_size_n)
        
        self.Buttons_win[i][0] = [Label_site, button_site]
        self.Buttons_win[i][1][1] = create_windows_abs_state.DEFAULT
        self.Buttons_win[i][2] = [grid_cont, last_grid]

        for i in range(len(self.Buttons_win)):
            for j in range(len(self.Buttons_win[i][0])):
                self.Buttons_win[i][0][j].config(command = lambda i=i, j=j: self.__button_index_helper_first_doubcl(i, j))
        self.__update_main_buttons()
        
    def __expand_gui_num_users(self, i:int, j: int) -> None:
        key = self.Buttons_win[i][1][0]
        self.Buttons_win[i][0][1].destroy()
        self.Buttons_win[i][1][1] = create_windows_abs_state.USER_PASS
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
                [key, create_windows_abs_state.DEFAULT],
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
    default_bg_color: str = "#2f2f2f"#"#3a7ff6"
    highlighted_fg_color: str = "#000000"
    highlighted_bg_color: str = "#ff7777"
    default_fg_color: str = "#000000"
    
    def __init__(self) -> None:
        super().__init__()
        self.ex = Window_Add_to_Encripted_File(file_path= file_path)
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
    
    def create_buttons(self, window: tk.Frame, image, command: Callable, relx: float, rely: float) -> tk.Button:
        button = tk.Button(window,
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
            functions = [self.test] + [lambda menu=self.menu: self.ex.add_data_to_file(menu)] + [self.test]*3
            for funct, img in zip(functions, self.all_imgs):
                button = self.create_buttons(self.menu, img, funct, 0, 0.1)
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

class Window_Add_to_Encripted_File(create_root):
    def __init__(self, file_path) -> None:
        super().__init__()
        self.show_password_image = os.path.join(self.resources_dir, "show_password.png")
        self.hide_password_image = os.path.join(self.resources_dir, "hide_password.png")
        self.file_path = file_path
        
        self.first_item = True
        
        self.entrys_color = "#2f2f2f"
        self.style = ttk.Style()
        #self.style.theme_use('default') 
        self.style.theme_create('combostyle', parent='vista',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': self.button_load_fg_color,
                                       'fieldbackground': self.entrys_color,
                                       'background': self.entrys_color,
                                       'foreground': self.button_load_fg_color,
                                       'selectBackground': self.button_load_fg_color,
                                       'selectforeground': self.entrys_color,
                                       }}}
                         )
        # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
        self.style.theme_use('combostyle') 
        #self.style.map('TCombobox', fieldbackground=[('readonly',self.entrys_color)])
        
    def add_data_to_file(self, window):
        window_add_data = tk.Toplevel(window, bg = self.bg_color)
        window_add_data.resizable(width=False, height=False)
        window_add_data.option_add("*TCombobox*Listbox*Background", self.entrys_color)
        window_add_data.title("New Window")
        window_add_data.iconphoto(False, tk.PhotoImage(file=os.path.join(self.resources_dir,"sk.png")))
        window_add_data.geometry(self.__get_geometry(window_add_data))
        tk.Label(window_add_data, bg = self.bg_color).grid(row= 0, column = 0, pady=15) # blank space
        return self.create_main_window(window_add_data)

    def __clean_labels(self):
        for key in self.entrys:
            text = tk.StringVar()
            text.set("")
            self.entrys[key]["textvariable"] = text
        for key in self.combobox:
            self.combobox[key]["textvariable"] = text
        
    def create_main_window(self, window):
        self.__image = resize_image(self.show_password_image)
        
        text = [f"{file_path}", "Site: ", "User: ", "Password: ", "Key: "]
        rows = [0, 2, 3, 5, 7]
        entrys_sensured = [5, 7]
        combobox = rows[1]
        self.file_path_text = rows[0]
        colonspan = [2] + [1 for i in range(len(rows) -1)]
        options = list(self.dicto) + ["otro"]
        option_menu_text = tk.StringVar()
        option_menu_text.set(options[-1])
        self.labels = dict()
        self.combobox = dict()
        self.entrys = dict()
        self.max_columnspan = 5
                
        button = self.create_labels(window, text=f"File: {file_path}", font=14, no_grid = True)
        button.grid(row = 0, column=0, columnspan = 3, pady=(40,20), padx=(40,0))
        
        btn = self.create_labels(window, text="Site: ", row=2, column=0, columnspan=1)
        combobox = self.create_combobox(window, options, row=2, column=1, columnspand=4)
        
        self.__change_button = self.create_buttons(window, text="Change", fg=self.button_create_fg_color, command=self.__open_encrypted_file, no_grid=True)
        self.__change_button.grid(row=self.file_path_text, column=3, pady=(40,20))
        
        btn = self.create_labels(window, text="User: ", row=3, column=0, columnspan=1)
        entry = self.create_entry(window, row=3, column=1, columnspand=4)
        
        btn = self.create_labels(window, text= "Password: ", row=5, column=0, columnspan=1)
        entry = self.create_entry(window, row=5, column=1, columnspand=4, sensure=True)

        btn = self.create_labels(window, text="Key: ", row=7, column=0, columnspan=1)
        entry = self.create_entry(window, row=7, column=1, columnspand=4, sensure=True)

        self.create_buttons_image(window, self.__image, row=5, column=5)
        self.create_buttons_image(window, self.__image, row=7, column=5)
        
        Ok_button = self.create_buttons(window, text="Ok", width = 3, height=3, fg=self.button_create_fg_color, row=8, column=0, pady=50, columnspan=2)
        Clean_button = self.create_buttons(window, text="Clean", width = 6, height=3, fg=self.button_create_fg_color, row=8, column=2, columnspan=5, pady=50, 
                                           padx = (15,0), command=self.__clean_labels)
        self.__on_buttons(self.__change_button, self.bg_color, self.button_create_fg_color)
        self.__on_buttons(Ok_button,self.bg_color, self.button_create_fg_color)
        self.__on_buttons(Clean_button,self.bg_color, self.button_create_fg_color)
        
    
    def create_entry(self, window, row, column, columnspand = 1, width=20, sensure=None):
        button = tk.Entry(window, width=width + 3, bg=self.entrys_color, fg = self.button_create_fg_color)
        if sensure:button.config(show="*")
        self.entrys.update({row: button})
        return button.grid(row=row, column=column, columnspan=columnspand)
    
    def create_combobox(self, window, options, row, column, columnspand = 1, width=20):
        combobox = ttk.Combobox(window, values=options, width=width)
        self.combobox.update({row: combobox})
        return combobox.grid(row = row, column=column, columnspan=columnspand)

    def create_labels(self, window: tk.Frame, text: str, row=0, column=0, columnspan = 1, rowspan = 1, justify=tk.RIGHT, anchor=tk.W, sticky=tk.E, font:int=12, no_grid=False) -> tk.Button:
        button = tk.Label(window,  
                        text= text,
                        anchor=anchor,
                        justify=justify,
                        fg=self.button_create_fg_color,
                        bg=self.bg_color,
                        font = font
                        )
        self.labels.update({row: button})
        if no_grid: return button
        button.grid(row = row, column=column, columnspan = columnspan, rowspan = rowspan, sticky=sticky)
        return button

    def create_buttons_image(self, window, image, row, column, sticky=tk.W):
        button = tk.Button(window,
                                   image=image,
                                    border = self.border,
                                    bg = self.bg_color,
                                    activebackground= self.bg_color).grid(row=row, column=column, sticky=sticky)
        return button
    
    def create_buttons(self, window: tk.Frame, text: str, fg: str, row: int = 0, column: int = 0, width:int= None, height:int= None,
                       font_size:int = None, pady:int=0, command:Callable = None, sticky=tk.E+tk.W, no_grid=False, columnspan:int=1,
                       padx = 0) -> tk.Button:
        if not font_size: font_size = self.font_size_n
        button = tk.Button(window,
                            text=text,
                            font=(self.font, font_size),
                            fg = fg,
                            bg = self.bg_color,
                            activebackground = fg,
                            activeforeground = self.bg_color,
                            border = self.border,
                            relief=tk.SUNKEN
                            )
        if width: button.config(width=width)
        if height: button.config(height=height)
        if command: button.config(command=command)
        if no_grid: return button
        button.grid(row = row, column=column, sticky=sticky, pady=pady, columnspan=columnspan, padx=padx)
        return button
    
    def __get_geometry(self, window):
        x_coordinates = window.winfo_screenwidth()//2 - self.width//2 - 50
        y_coordinates = window.winfo_screenheight()//2 - self.height//2 - 50
        return f"{str(self.width)}x{str(self.height)}+{x_coordinates}+{y_coordinates}"
    
    def __on_buttons(self, button: tk.Button, primary_color: str, secundary_color: str = None) -> None:
        button.bind("<Enter>", lambda event: self.__on_mouse(button, primary_color, secundary_color))
        button.bind("<Leave>", lambda event: self.__on_mouse(button, secundary_color, primary_color))
    
    def __on_mouse(self, button: tk.Button, fg: str, bg: str) -> None:
        button.config(bg = bg, fg = fg)
    
    def __open_encrypted_file(self) -> None:
        text_file_extensions = ['*.bin']
        self.__file = None
        ftypes = [
            ('.Bin (Encripted)', text_file_extensions)]
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                           filetypes=ftypes)
        if not filename:
            return

        self.__file = filename
        name = os.path.basename(filename)
        len_file = 26
        if len(name) > len_file: name = "..." + name[-len_file+3:]
        self.labels[self.file_path_text].config(text= f"File: {name}")

class encript_data:
    def __init__(self) -> None:
        self.ead = EaD()
    
    def Verify(self, file: str, key:bytes):
        self.ead.load_and_decript_file(file, key)
        

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
create_windows_abs.dicto = example_dict
root_window = A.create_main_window()
B = create_menu()
menu_window = B.create_main_window(root_window)
scrollbar = create_scrollbar()
win, canvas, scrollbar_root = scrollbar.create_scrollbar(root_window)
B.default_gui()
A.default_gui(win)
#ex = Window_Add_to_Encripted_File(file_path= file_path)
A.loop()