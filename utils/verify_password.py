# Verify and decript
import tkinter as tk
from tkinter import ttk, W, CENTER, StringVar
from dec import EaD # Encript and Decript

from PIL import Image, ImageTk

class verify_password(EaD):
    image = None
    def __init__(self) -> None:
        super().__init__()
        self.width  = 300
        self.height = 400
        self.geometry = f"{str(self.width)}x{str(self.height)}"
        
        self.__place_starting = 0.2
        self.__place_step = 0.1
        self.__place_in_center = 0.5
        self.__place_width_porcentage = 0.125 #38
        self.__place_width = int(self.__place_width_porcentage * self.width)
        self.__font = "arial.ttf"

        self.__show = "*"
        self.__show_password_image = r"resources\show_password.png"
        self.__hide_password_image = r"resources\hide_password.png"
        self.__image = None
        self.__entry_value = None
        self.file = None
    
    def __resize_image(self, img, width=20, height=20) -> ImageTk:
        image = Image.open(img)
        resize = image.resize((width, height))
        return ImageTk.PhotoImage(resize)

    def __create_windows(self) -> None:
        self.win=tk.Tk()
        self.win.title("Verify Password")
        self.win.wm_attributes('-toolwindow', 'True')
        self.win.resizable(width=False, height=False)
        
        # Set the geometry of the window
        self.win.geometry(self.geometry)
        
        # Create a frame widget
        frame=tk.Frame(self.win, width=self.width, height=self.height)
        frame.grid(row=0, column=0, sticky="NW")

        # Create a label widget
        label=tk.Label(self.win, text="SecKeys", font=self.__font)
        label.place(relx=self.__place_in_center, rely=self.__place_starting, anchor=CENTER)
        
        # Create a label widget
        key_entry_var = StringVar()
        text = "Key: "
        label=tk.Label(self.win, text=text)
        label.place(relx=self.__place_width_porcentage-0.08, rely=self.__place_starting+self.__place_step*3, anchor=W)
        
        # Textbox input
        key_entry = ttk.Entry(self.win, width=31, textvariable=key_entry_var, show=self.__show)
        key_entry.place(relx=0.56-0.08, rely=self.__place_starting+self.__place_step*3, anchor=CENTER)
        
        self.__image = self.__resize_image(self.__show_password_image)
        show_pw_button = ttk.Button(self.win,
                                    image=self.__image,
                                    width = 2,
                                    command= lambda: self.__show_password(key_entry, show_pw_button))
        show_pw_button.place(relx=0.56+0.3, rely=self.__place_starting+self.__place_step*3, anchor=CENTER)

        # Ok button
        ok_button = ttk.Button(self.win, text="Ok", width = self.__place_width//2 - 5, command = lambda: self.__load_password(key_entry))
        ok_button.place(relx=self.__place_in_center - 0.2, rely=self.__place_starting+self.__place_step*5, anchor=CENTER)
        
        # Cancel button
        cancel_button = ttk.Button(self.win, text="Cancelar", width = self.__place_width//2 -5)
        cancel_button.place(relx=self.__place_in_center + 0.2, rely=self.__place_starting+self.__place_step*5, anchor=CENTER)
        
        self.win.mainloop()
        
    def __show_password(self, key: tk.Entry, button: ttk.Button) -> None:
        if self.__show == "*":
            self.__show = ""
            self.__image = self.__resize_image(self.__hide_password_image)
        elif self.__show == "":
            self.__image = self.__resize_image(self.__show_password_image)
            self.__show = "*"
        button.config(image=self.__image)
        key["show"] = self.__show

    def Validation(self, filename: str) -> None:
        self.file = filename
        self.__create_windows()
        
    def __load_password(self, key_entry: ttk.Entry) -> None:
        self.__entry_value = key_entry.get()
        if self.file == None or self.file[-4:] != ".bin":
            raise Exception(ValueError("Error in file"))
        self.load_and_decript_file(self.file, self.__entry_value)
        self.win.destroy()