from PIL import Image, ImageTk


class WidgetUtilities:

    def load_image(self, image_path, width, height):
        image = Image.open(image_path)
        image = image.resize((width, height))
        return ImageTk.PhotoImage(image)
