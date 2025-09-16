import tkinter as tk
from widget_utilities import WidgetUtilities
import math
from widget_pad import WidgetPad


class WidgetPadGrid(tk.Frame, WidgetUtilities):

    def __init__(
        self,
        master=None,
        canvas=None,
        widget_width=818,
        widget_height=418,
        canvas_width=1200,
        canvas_height=760,
        font_color="#340006",
        label_font="Arial",
        label_font_size=36,
        rel_x=0.5,
        rel_y=0.715,
    ):
        super().__init__(master=master, width=widget_width, height=widget_height)
        self.pos_x = int(canvas_width * rel_x)  # HARDCODED
        self.pos_y = int(canvas_height * rel_y)

        self.pad_list = []

        # Background image
        self.tk_bckgnd_img = self.load_image(
            image_path="./res_2/png/bckgnd-pad_grid_2.png",
            width=widget_width,
            height=widget_height,
        )
        self.bckgnd = canvas.create_image(
            self.pos_x,
            self.pos_y,
            anchor=tk.CENTER,
            image=self.tk_bckgnd_img,
        )

        for id_pad, _ in enumerate(range(8)):
            pad_width = int(canvas_width * 0.15)
            if id_pad > 3:
                self.pad_list.append(
                    WidgetPad(
                        master=master,
                        canvas=canvas,
                        pos_x=self.pos_x * 0.5
                        + (widget_width - (pad_width * 4)) / 2
                        + pad_width * (id_pad - 4),
                        pos_y=self.pos_y * 0.83,
                        widget_width=pad_width,
                        widget_height=pad_width,
                    )
                )
            else:
                self.pad_list.append(
                    WidgetPad(
                        master=master,
                        canvas=canvas,
                        pos_x=self.pos_x * 0.5
                        + (widget_width - (pad_width * 4)) / 2
                        + pad_width * id_pad,
                        pos_y=self.pos_y * 1.17,
                        widget_width=pad_width,
                        widget_height=pad_width,
                    )
                )
