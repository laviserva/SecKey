import tkinter as tk
from tkinter import NW, filedialog, CENTER, W

import os

from dec import EaD # Encript and Decript
from enum import Enum, auto
from data_window import Window_Create_Encripted_file

class start_app_state(Enum):
    ALIVE = auto()
    CLOSED = auto()
    DESTROYED = auto()
    FILE_CREATED = auto()
    LOADING_FILE = auto()

class start_app(EaD):
    width  = 300
    height = 400
    
    font = "Times"
    font_size_h1 = 50
    font_size_n = 16
    title_font_color = "#d8de76"
    button_create_fg_color = "#ff7777"
    button_load_fg_color = "#87d2fa"
    bg_color = "#1e1e1e"
        
    def __init__(self) -> None:
        self.state = start_app_state.ALIVE
        
        self.place_starting = 0.2
        self.place_step = 0.1
        self.place_in_center = 0.5
        self.place_width_porcentage = 0.125 #38
        self.place_width = int(self.place_width_porcentage * self.width)
        self.place_height_porcentage = self.place_width_porcentage/20
        self.place_height = 5
        
        self.show = "*"
        self.__file = None
    
    def __create_encrypted_file(self, window: tk.Frame, root: tk.Tk) -> None:
        """Create encrypted file and add data to it"""
        waef = Window_Create_Encripted_file()
        encripted_window = waef.add_data_to_file(window, root)
        window.wait_window(encripted_window)
        self.__file = waef.file
        self.win.destroy()
        self.state = start_app_state.FILE_CREATED
        self.data = waef.get_data()
        
    def __on_closing(self) -> None:
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.win.destroy()
        self.state = start_app_state.CLOSED
        
    def __on_enter_mouse(self, button: tk.Button, bg: str, fg: str) -> None:
        button["background"] = bg
        button["foreground"] = fg
    
    def __on_leave_mouse(self, button: tk.Button, bg: str, fg: str) -> None:
        button["background"] = fg
        button["foreground"] = bg
    
    def __open_encrypted_file(self) -> None:
        text_file_extensions = ['*.bin']
        ftypes = [
            ('.Bin (Encripted)', text_file_extensions)]
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                           filetypes=ftypes)
        if not filename:
            return
        self.__file =  filename
        self.win.destroy()
        self.state = start_app_state.LOADING_FILE
    
    def init_window(self) -> None:
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
        self.win.geometry(self.geometry)
        frame=tk.Frame(self.win,
                       width=self.width,
                       height=self.height,
                       bg = self.bg_color)
        frame.grid(row=0, column=0, sticky=NW)
        Seckeys_label=tk.Label(self.win, text="SecKeys",
                       font=(self.font, self.font_size_h1),
                       fg = self.title_font_color,
                       bg = self.bg_color,
                       anchor = W
                       )
        Seckeys_label.place(relx=self.place_in_center, rely=self.place_starting, anchor=CENTER)
        
        create_file_button = tk.Button(self.win,
                                        text="Create File",
                                        width = self.place_width,
                                        height = self.place_height,
                                        font=(self.font, self.font_size_n),
                                        fg = self.button_create_fg_color,
                                        bg = self.bg_color,
                                        activebackground = self.button_create_fg_color,
                                        activeforeground = self.bg_color,
                                        border = 0,
                                        command = lambda window=frame, root=self.win: self.__create_encrypted_file(window, root)
                                        )
        create_file_button.bind("<Enter>", lambda event: self.__on_enter_mouse(create_file_button,self.button_create_fg_color, self.bg_color))
        create_file_button.bind("<Leave>", lambda event: self.__on_leave_mouse(create_file_button,self.button_create_fg_color, self.bg_color))
        create_file_button.place(relx=self.place_in_center, rely=0.5, anchor=CENTER)
        
        Load_key_button = tk.Button(self.win, text="Load File",
                                     width  = self.place_width,
                                     height = self.place_height,
                                     font = (self.font, self.font_size_n),
                                     fg = self.button_load_fg_color,
                                     bg = self.bg_color,
                                     activebackground = self.button_load_fg_color,
                                     activeforeground = self.bg_color,
                                     border = 0,
                                     command=self.__open_encrypted_file)
        Load_key_button.bind("<Enter>", lambda event: self.__on_enter_mouse(Load_key_button,self.button_load_fg_color, self.bg_color))
        Load_key_button.bind("<Leave>", lambda event: self.__on_leave_mouse(Load_key_button,self.button_load_fg_color, self.bg_color))
        Load_key_button.place(relx=self.place_in_center, rely=0.825, anchor=CENTER)
        
        self.win.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.win.mainloop()
        return self.__file