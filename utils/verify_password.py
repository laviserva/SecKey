# Verify and decript
import tkinter as tk
from tkinter import ttk, W, CENTER, StringVar
from dec import EaD # Encript and Decript
from img_utils import resize_image

from enum import Enum, auto

class Verify_password_state(Enum):
    ALIVE = auto()
    DESTROYED = auto()
    RETURN_TO_MAIN = auto()

class verify_password(EaD):
    image = None
    def __init__(self) -> None:
        self.__out = None
        super().__init__()
        self.width  = 300
        self.height = 400
        
        self.__place_starting = 0.2
        self.__place_step = 0.1
        self.__place_in_center = 0.5
        self.__place_width_porcentage = 0.125 #38
        self.__place_width = int(self.__place_width_porcentage * self.width)
        self.__place_height_porcentage = 0.125/2 #38
        self.__place_height = int(self.__place_height_porcentage * self.height)
        
        self.font = "Times"
        self.font_size_h1 = 50
        self.font_size_n = 16
        self.title_font_color = "#d8de76"
        self.Label_color = "#87d2fa"
        self.ok_button_fg_color = "#87d2fa"
        self.return_button_fg_color = "#ff7777"
        self.bg_color = "#1e1e1e"

        self.__show = "*"
        self.__show_password_image = r"resources\show_password.png"
        self.__hide_password_image = r"resources\hide_password.png"
        self.__image = None
        self.__entry_value = None
        self.file = None
        
        self.state = Verify_password_state.ALIVE
    
    def __on_closing(self) -> None:
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.__closing()
    
    def __closing(self) -> None:
        self.win.destroy()
        self.state = Verify_password_state.DESTROYED
        
    def __on_enter(self, button: tk.Button, bg: str, fg: str) -> None:
        button["background"] = fg
        button["foreground"] = bg
    
    def __on_leave(self, button: tk.Button, bg: str, fg: str) -> None:
        button["background"] = bg
        button["foreground"] = fg
    
    def __return_button(self) -> None:
        self.state = Verify_password_state.RETURN_TO_MAIN
        self.win.destroy()

    def __create_windows(self) -> None:
        self.state = Verify_password_state.ALIVE
        self.win=tk.Tk()
        self.win.title("Verify Password")
        self.win.iconphoto(False, tk.PhotoImage(file=r"resources\sk.png"))
        screen_width  = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x_coordinates = screen_width//2 - self.width//2
        y_coordinates = screen_height//2 - self.height//2
        self.geometry = f"{str(self.width)}x{str(self.height)}+{x_coordinates}+{y_coordinates}"
        #self.win.wm_attributes('-toolwindow', 'True')
        self.win.resizable(width=False, height=False)
        
        # Set the geometry of the window
        self.win.geometry(self.geometry)
        
        # Create a frame widget
        frame=tk.Frame(self.win,
                       bg = self.bg_color,
                       width=self.width,
                       height=self.height)
        frame.grid(row=0, column=0, sticky="NW")

        # Create a label widget
        label=tk.Label(self.win,
                       text="SecKeys",
                       font = (self.font, self.font_size_h1),
                       fg = self.title_font_color,
                       bg = self.bg_color,
                       anchor="w")
        label.place(relx=self.__place_in_center, rely=self.__place_starting, anchor=CENTER)
        
        # Create a label widget
        key_entry_var = StringVar()
        text = "Key: "
        label=tk.Label(self.win,
                       text=text,
                       font = self.font,
                       bg = self.bg_color,
                       fg = self.Label_color
                       )
        label.place(relx=self.__place_width_porcentage-0.08, rely=self.__place_starting+self.__place_step*3, anchor=W)
        
        # Textbox input
        key_entry = tk.Entry(self.win,
                             width=31,
                             textvariable = key_entry_var,
                             bg=self.bg_color,
                             show=self.__show)
        key_entry.place(relx=0.56-0.08, rely=self.__place_starting+self.__place_step*3, anchor=CENTER)
        
        self.__image = resize_image(self.__show_password_image)
        show_pw_button = tk.Button(self.win,
                                    image=self.__image,
                                    width = 15,
                                    bg = self.bg_color,
                                    border = 0,
                                    activebackground = self.bg_color,
                                    command= lambda: self.__show_password(key_entry, show_pw_button))
        show_pw_button.place(relx=0.56+0.3, rely=self.__place_starting+self.__place_step*3, anchor=CENTER)

        # Ok button
        ok_button = tk.Button(self.win, text="Ok",
                              width  = self.__place_width//2 - 5,
                              height = self.__place_height//2 -5,
                              fg = self.ok_button_fg_color,
                              bg = self.bg_color,
                              border = 0,
                              activebackground = self.bg_color,
                              activeforeground = self.ok_button_fg_color,
                              command = lambda: self.__load_password(self.file, key_entry))
        ok_button.place(relx=self.__place_in_center - 0.2, rely=self.__place_starting+self.__place_step*6, anchor=CENTER)
        ok_button.bind("<Enter>", lambda event: self.__on_enter(ok_button, self.bg_color, self.ok_button_fg_color))
        ok_button.bind("<Leave>", lambda event: self.__on_leave(ok_button, self.bg_color, self.ok_button_fg_color))
        # Cancel button
        return_button = tk.Button(self.win,
                                  text="Back to main",
                                  width = self.__place_width//2 -5,
                                  height = self.__place_height//2 -5,
                                  fg = self.return_button_fg_color,
                                  bg = self.bg_color,
                                  activebackground = self.bg_color,
                                  activeforeground = self.return_button_fg_color,
                                  border = 0,
                                  command=self.__return_button)
        return_button.place(relx=self.__place_in_center + 0.2, rely=self.__place_starting+self.__place_step*6, anchor=CENTER)
        return_button.bind("<Enter>", lambda event: self.__on_enter(return_button, self.bg_color, self.return_button_fg_color))
        return_button.bind("<Leave>", lambda event: self.__on_leave(return_button, self.bg_color, self.return_button_fg_color))
        self.win.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.win.mainloop()
        
    def __show_password(self, key: tk.Entry, button: tk.Button) -> None:
        if self.__show == "*":
            self.__show = ""
            self.__image = resize_image(self.__hide_password_image)
        elif self.__show == "":
            self.__image = resize_image(self.__show_password_image)
            self.__show = "*"
        button.config(image=self.__image)
        key["show"] = self.__show

    def Validation(self, filename: str) -> None:
        self.file = filename
        self.__create_windows()
        return self.__out
        
    def __load_password(self, file, key_entry: tk.Entry) -> None:
        self.__entry_value = key_entry.get().encode()
        if file == None or file[-4:] != ".bin":
            raise Exception(ValueError("Error in file"))
        self.__out = self.load_and_decript_file(file, self.__entry_value)
        self.__closing()

#A = verify_password()
#A.Validation("file_encripted.bin")