import tkinter as tk
import math
from gui.image_item import ImageItem


class WidgetPad(tk.Frame):

    def __init__(
        self,
        master=None,
        canvas=None,
        widget_width=180,
        widget_height=180,
        pos_x=0,
        pos_y=0,
        font_color="#00ff00",
        label_font="Arial",
        label_font_size=86,
        is_root=False,
        pad_note="C -3",
    ):
        super().__init__(master=master, width=widget_width, height=widget_height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.note = pad_note
        self.is_root = is_root
        self.widget_width = widget_width
        self.widget_height = widget_height

        # Active state image
        self.img_pad_active = ImageItem(
            canvas=canvas,
            image_path="./res_2/png/bckgnd-pad_active.png",
            x=self.pos_x,
            y=self.pos_y,
            width=self.widget_width,
            height=self.widget_height,
        )

        # Pad image
        self.img_pad = ImageItem(
            canvas=canvas,
            image_path="./res_2/png/bckgnd-pad.png",
            x=self.pos_x,
            y=self.pos_y,
            width=self.widget_width,
            height=self.widget_height,
        )
        self.img_pad_root = ImageItem(
            canvas=canvas,
            image_path="./res_2/png/bckgnd-pad_root.png",
            x=self.pos_x,
            y=self.pos_y,
            width=self.widget_width,
            height=self.widget_height,
        )
        if not self.is_root:
            self.img_pad_root.hide()

        # Note label
        self.note_label = canvas.create_text(
            self.pos_x,
            self.pos_y,  # Center of the image
            text=self.note,  # Your label text
            fill=font_color,  # Text color
            font=(label_font, int(label_font_size * 0.5), "bold"),  # Font style
        )
