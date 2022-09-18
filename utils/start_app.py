import tkinter as tk
from tkinter import filedialog, ttk, W, CENTER, StringVar

from PIL import ImageFont
import os

from dec import EaD # Encript and Decript
from enum import Enum, auto

class start_app_state(Enum):
    ALIVE = auto()
    CLOSED = auto()
    DESTROYED = auto()
    LOADING_FILE = auto()

class start_app(EaD):
    def __init__(self) -> None:
        self.state = start_app_state.ALIVE
        self.width  = 300
        self.height = 400
        self.geometry = f"{str(self.width)}x{str(self.height)}"
        
        self.place_starting = 0.2
        self.place_step = 0.1
        self.place_in_center = 0.5
        self.place_width_porcentage = 0.125 #38
        self.place_width = int(self.place_width_porcentage * self.width)
        self.place_height_porcentage = self.place_width_porcentage/20
        self.place_height = 5
        
        self.font = "Times"
        self.font_size_h1 = 50
        self.font_size_n = 16
        self.title_font_color = "#d8de76"
        self.button_create_fg_color = "#ff7777"
        self.button_load_fg_color = "#87d2fa"
        self.bg_color = "#1e1e1e"
        
        self.show = "*"
        self.__file = None
        
    def __on_closing(self) -> None:
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.win.destroy()
        self.state = start_app_state.CLOSED
        
    def __on_enter(self, button: tk.Button, bg: str, fg: str) -> None:
        button["background"] = bg
        button["foreground"] = fg
    
    def __on_leave(self, button: tk.Button, bg: str, fg: str) -> None:
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
        self.win.title("SecKey")
        self.win.iconphoto(False, tk.PhotoImage(file=r"resources\sk.png"))
        #self.win.wm_attributes('-toolwindow', 'True') # Hide icon
        self.win.resizable(width=False, height=False)
        
        # Set the geometry of the window
        self.win.geometry(self.geometry)

        # Create a frame widget
        frame=tk.Frame(self.win,
                       width=self.width,
                       height=self.height,
                       bg = self.bg_color)
        frame.pack(fill = tk.X, padx=20, pady=20)
        frame.grid(row=0, column=0, sticky="NW")
        #frame.config(bg = "#fcfcfc")

        # Create a label widget
        Seckeys_label=tk.Label(self.win, text="SecKeys",
                       font=(self.font, self.font_size_h1),
                       fg = self.title_font_color,
                       bg = self.bg_color,
                       anchor = "w"
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
                                        border = 0
                                        )
        create_file_button.bind("<Enter>", lambda event: self.__on_enter(create_file_button,self.button_create_fg_color, self.bg_color))
        create_file_button.bind("<Leave>", lambda event: self.__on_leave(create_file_button,self.button_create_fg_color, self.bg_color))
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
        Load_key_button.bind("<Enter>", lambda event: self.__on_enter(Load_key_button,self.button_load_fg_color, self.bg_color))
        Load_key_button.bind("<Leave>", lambda event: self.__on_leave(Load_key_button,self.button_load_fg_color, self.bg_color))
        Load_key_button.place(relx=self.place_in_center, rely=0.825, anchor=CENTER)
        
        self.win.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.win.mainloop()
        return self.__file