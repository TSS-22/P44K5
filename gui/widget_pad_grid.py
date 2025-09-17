import tkinter as tk
import math
from gui.widget_pad import WidgetPad
from gui.image_item import ImageItem


class WidgetPadGrid(tk.Frame):

    list_note = [
        "C -3",
        "D -3",
        "E -3",
        "F -3",
        "G -3",
        "A -3",
        "B -3",
        "C -2",
    ]  # HARDOCDED + TEST

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
        self.widget_width = widget_width
        self.widget_height = widget_height
        self.pad_list = []

        # Background image
        self.img_bckgnd = ImageItem(
            canvas=canvas,
            image_path="./res_2/png/bckgnd-pad_grid_2.png",
            x=self.pos_x,
            y=self.pos_y,
            width=self.widget_width,
            height=self.widget_height,
        )

        for id_pad, _ in enumerate(range(8)):
            pad_width = int(canvas_width * 0.15)
            if id_pad > 3:
                self.pad_list.append(
                    WidgetPad(
                        master=master,
                        canvas=canvas,
                        pos_x=self.pos_x
                        - widget_width * 0.5
                        + pad_width * 0.5
                        + (widget_width - (pad_width * 4)) / 2
                        + pad_width * (id_pad - 4),
                        pos_y=self.pos_y * 0.83,
                        widget_width=pad_width,
                        widget_height=pad_width,
                        pad_note=self.list_note[id_pad],
                    )
                )
            else:
                self.pad_list.append(
                    WidgetPad(
                        master=master,
                        canvas=canvas,
                        pos_x=self.pos_x
                        - widget_width * 0.5
                        + pad_width * 0.5
                        + (widget_width - (pad_width * 4)) / 2
                        + pad_width * id_pad,
                        pos_y=self.pos_y * 1.17,
                        widget_width=pad_width,
                        widget_height=pad_width,
                        is_root=True if (id_pad == 0) else False,
                        pad_note=self.list_note[id_pad],
                    )
                )
