from PIL import Image, ImageTk
import numpy as np

def resize_image(img: str, width=14, height=14) -> ImageTk:
    image = Image.open(img)
    resize = image.resize((width, height))
    return ImageTk.PhotoImage(resize)

def from_array_to_img(array: np.ndarray, width:int = 14, height:int = 14) -> ImageTk:
    img = Image.fromarray(array)
    img = img.resize((width, height))
    return ImageTk.PhotoImage(img)
    
def from_img_to_array(img) -> np.ndarray:
    return np.array(Image.open(img))
    
def from_hexa_to_rgb(hexa_code: str) -> list:
    hexa_code = hexa_code[1:]
    rgb = list(int(hexa_code[i:i+2], 16) for i in (0, 2, 4))
    rgb = (*rgb, 255)
    return rgb

def change_img_colors(path:str, fg: str, bg:str, width:int=14, height:int=14) -> ImageTk:
    array = from_img_to_array(path)
    bg = from_hexa_to_rgb(bg)
    fg = from_hexa_to_rgb(fg)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if array[i,j,3] != 0:
                array[i, j] = fg
                continue
            if bg is None:
                continue
            if array[i,j,3] == 0:
                array[i,j] = bg
    return from_array_to_img(array, width=width, height=height)