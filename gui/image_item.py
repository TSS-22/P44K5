import tkinter as tk
from PIL import Image, ImageTk


class ImageItem:
    def __init__(self, canvas, image_path, x, y, anchor=tk.CENTER, **kwargs):
        self.canvas = canvas
        self.image_path = image_path
        self.x = x
        self.y = y
        self.anchor = anchor
        self.tk_image = self._load_image(**kwargs)
        self.canvas_item = canvas.create_image(x, y, anchor=anchor, image=self.tk_image)
        self.state = "normal"  # or "hidden"
        self.current_angle = 0

    def _load_image(self, width=None, height=None):
        img = Image.open(self.image_path)
        if width and height:
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        self.pil_image = img  # Store the PIL image for later manipulation
        return ImageTk.PhotoImage(img)

    def rotate(self, angle):
        """Rotate the image by the specified angle (in degrees)."""
        self.current_angle += angle
        # Rotate the PIL image
        rotated_img = self.pil_image.rotate(-self.current_angle, expand=True)
        # Update the Tkinter PhotoImage
        self.tk_image = ImageTk.PhotoImage(rotated_img)
        # Update the canvas item
        self.canvas.itemconfig(self.canvas_item, image=self.tk_image)

    def hide(self):
        self.state = "hidden"
        self.canvas.itemconfig(self.canvas_item, state="hidden")

    def show(self):
        self.state = "normal"
        self.canvas.itemconfig(self.canvas_item, state="normal")

    def toggle(self):
        self.state = "hidden" if self.state == "normal" else "normal"
        self.canvas.itemconfig(self.canvas_item, state=self.state)

    def get_path(self):
        return self.image_path
