from PIL import Image, ImageTk

def resize_image(img, width=14, height=14) -> ImageTk:
        image = Image.open(img)
        resize = image.resize((width, height))
        return ImageTk.PhotoImage(resize)