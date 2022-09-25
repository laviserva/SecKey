from PIL import Image, ImageTk
import numpy as np

def resize_image(img: str, width=14, height=14) -> ImageTk:
        image = Image.open(img)
        resize = image.resize((width, height))
        return ImageTk.PhotoImage(resize)

def from_array_to_img(array: np.ndarray):
        return ImageTk.PhotoImage(Image.fromarray(array))
    
def from_img_to_array(img) -> np.ndarray:
        return np.array(Image.open(img))

def change_img_colors(path:str, fg: list, bg:str = None):
    array = from_img_to_array(path)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if array[i,j,3] != 0:
                array[i, j] = fg
                continue
            if bg is None:
                continue
            if array[i,j,3] == 0:
                array[i,j,3] = bg
            
    return from_array_to_img(array)