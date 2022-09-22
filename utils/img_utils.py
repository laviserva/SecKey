from PIL import Image, ImageTk
import numpy as np

def resize_image(img: str, width=14, height=14) -> ImageTk:
        image = Image.open(img)
        resize = image.resize((width, height))
        return ImageTk.PhotoImage(resize)

def from_array_to_img(array: np.ndarray):
        img = Image.fromarray(array)
        return ImageTk.PhotoImage(image = img)