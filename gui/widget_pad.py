import tkinter as tk
from widget_utilities import WidgetUtilities
import math


class WidgetPad(tk.Frame, WidgetUtilities):

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

        # Active state image
        self.tk_pad_active_img = self.load_image(
            image_path="./res_2/png/bckgnd-pad_active.png",
            width=widget_width,
            height=widget_height,
        )
        self.img_pad_active = canvas.create_image(
            self.pos_x,
            self.pos_y,
            anchor=tk.CENTER,
            image=self.tk_pad_active_img,
        )

        # Pad image
        self.tk_pad_img = self.load_image(
            image_path=(
                "./res_2/png/bckgnd-pad_root.png"
                if is_root
                else "./res_2/png/bckgnd-pad.png"
            ),
            width=widget_width,
            height=widget_height,
        )
        self.pad_img = canvas.create_image(
            self.pos_x,
            self.pos_y,
            anchor=tk.CENTER,
            image=self.tk_pad_img,
        )

        # Note label
        canvas.create_text(
            self.pos_x,
            self.pos_y,  # Center of the image
            text=self.note,  # Your label text
            fill=font_color,  # Text color
            font=(label_font, int(label_font_size * 0.5), "bold"),  # Font style
        )
