import tkinter as tk
from PIL import Image, ImageTk
from gui.image_item import ImageItem
from gui.widget_base_note import WidgetBaseNote
from gui.widget_key_note import WidgetKeyNote
from gui.widget_panel_mode import WidgetPanelMode
from gui.widget_panel_play_type import WidgetPanelPlayType
from gui.widget_panel_chord import WidgetPanelChordType
from gui.widget_pad_grid import WidgetPadGrid


class UiCanvas(tk.Canvas):

    def __init__(
        self,
        master=None,
        canvas_height=760,
        canvas_width=1200,
        color_deep_brown="#340006",
        color_blue_active="#0BDBEE",
        color_red_root="#891A25",
        color_green_active="#00ff00",
        color_bckgnd="#260006",
        label_font="Arial",
        label_font_size_normal=36,
    ):
        super().__init__(
            master=master, bg=color_bckgnd, width=canvas_width, height=canvas_height
        )
        self.pack()
        # Background image
        self.img_bckgnd = ImageItem(
            canvas=self,
            image_path="./res_2/png/bckgnd-app.png",
            width=canvas_width,
            height=canvas_height,
            x=canvas_width * 0.5,
            y=canvas_height * 0.5,
        )

        widget_base_note = WidgetBaseNote(master=master, canvas=self)
        widget_key_note = WidgetKeyNote(master=master, canvas=self)
        widget_panel_mode = WidgetPanelMode(master=master, canvas=self)
        widget_panel_play_type = WidgetPanelPlayType(master=master, canvas=self)
        widget_panel_chord_type = WidgetPanelChordType(master=master, canvas=self)
        widget_pad_grid = WidgetPadGrid(master=master, canvas=self)
