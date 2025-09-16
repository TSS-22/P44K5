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
        font_color="#340006",
        label_font="Arial",
        label_font_size=36,
    ):
        super().__init__(master=master, width=widget_width, height=widget_height)
        self.pos_x = pos_x
        self.pos_y = pos_y

        # Background image
        self.tk_bckgnd_img = self.load_image(
            image_path="./res_2/png/bckgnd-pad.png",
            width=widget_width,
            height=widget_height,
        )
        self.bckgnd = canvas.create_image(
            self.pos_x,
            self.pos_y,
            anchor=tk.CENTER,
            image=self.tk_bckgnd_img,
        )
