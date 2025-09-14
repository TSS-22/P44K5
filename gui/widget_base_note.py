import tkinter as tk
from widget_utilities import WidgetUtilities


class WidgetBaseNote(tk.Frame, WidgetUtilities):

    arc_division = 315 / 128

    def __init__(
        self, master=None, canvas=None, width=168, height=415, arc_color="#00ff00"
    ):
        super().__init__(master=master, width=width, height=height)

        self.tk_bckgnd_img = self.load_image(
            image_path="./res_2/png/bckgnd-base_note.png",
            width=width,
            height=height,
        )
        canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_bckgnd_img)
        self.arc_knob = canvas.create_arc(
            101 - 100,
            475 - 100,
            101 + 100,
            475 + 100,  # Bounding box (x0, y0, x1, y1)
            start=0,  # Start angle (degrees)
            extent=self.arc_division * 10,  # Extent (degrees)
            fill=arc_color,  # Fill color
            outline="",  # Outline color
        )
