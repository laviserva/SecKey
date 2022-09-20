import tkinter as tk

from enum import Enum, auto

class data_window_state(Enum):
    pass

class data_window:
    def __init__(self) -> None:
        self.width  = 300
        self.height = 400
    
    def __create_menu(self) -> None:
        self.menu = tk.Frame(self.win, width=100 ,background="#3a7ff6")
        self.menu.pack(side = "left",  fill = tk.BOTH)
        
        menu_button = tk.Button(self.menu, text = "aru")
        menu_button.place(relx=0.1, rely=0.10)
        
    def window(self):
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
        # Set the geometry of the window
        self.win.geometry(self.geometry)
        self.__create_menu()
        
        self.win.mainloop()

A = data_window()
A.window()
