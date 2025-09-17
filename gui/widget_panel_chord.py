import tkinter as tk
import math
from gui.image_item import ImageItem


class WidgetPanelChordType(tk.Frame):

    list_play_type = [
        "5",
        "X",
        "6",
        "7",
        "9",
        "11",
        "13",
    ]  # HARDCODED

    def __init__(
        self,
        master=None,
        canvas=None,
        widget_width=230,
        widget_height=250,
        canvas_width=1200,
        canvas_height=760,
        font_color="#340006",
        label_font="Arial",
        label_font_size=36,
        rel_x=0.228,
        rel_y=0.19,
    ):
        super().__init__(master=master, width=widget_width, height=widget_height)
        self.pos_x = int(canvas_width * rel_x) + 244  # HARDCODED
        self.pos_y = int(canvas_height * rel_y)
        self.widget_width = widget_width
        self.widget_height = widget_height

        # Wheel slice image
        self.img_wheel_slice = ImageItem(
            canvas=canvas,
            image_path="./res_2/png/camembert_chord_type.png",
            width=int(widget_height * 0.6),  # HARDCODED
            height=int(widget_height * 0.6),  # HARDCODED
            x=self.pos_x,
            y=self.pos_y + int(widget_height * 0.118),
        )

        # Wheel image
        self.img_wheel = ImageItem(
            canvas=canvas,
            image_path="./res_2/png/wheel_chord_type_225.png",
            width=int(widget_height * 0.6),  # HARDCODED
            height=int(widget_height * 0.6),  # HARDCODED
            x=self.pos_x,
            y=self.pos_y + int(widget_height * 0.118),
        )

        # Knob image
        self.img_knob = ImageItem(
            canvas=canvas,
            image_path="./res_2/png/knob.png",
            width=int(168 * 0.85),  # HARDCODED
            height=int(168 * 0.85),  # HARDCODED
            x=self.pos_x,
            y=self.pos_y + int(widget_height * 0.118),
        )

        # Labels background play
        for idx, play_type in enumerate(self.list_play_type):
            base = 135 + 18
            angle_deg = idx * (270 / 7) + base  # Evenly spaced angles
            angle_rad = math.radians(angle_deg)
            label_pos_x = self.pos_x + int((widget_height * 1.0) / 3) * math.cos(
                angle_rad
            )
            label_pos_y = (
                self.pos_y
                + int(widget_height * 0.118)
                + (int((widget_height * 1.0) / 3)) * math.sin(angle_rad)
            )
            if idx < 3:
                canvas.create_text(
                    label_pos_x,
                    label_pos_y,
                    text=play_type,  # Your label text
                    fill=font_color,  # Text color
                    font=(label_font, int(label_font_size * 0.5), "bold"),
                    anchor="e",  # Font style
                )

            elif idx == 3:
                canvas.create_text(
                    label_pos_x,
                    label_pos_y * 1.1,
                    text=play_type,  # Your label text
                    fill=font_color,  # Text color
                    font=(label_font, int(label_font_size * 0.5), "bold"),
                    anchor="s",  # Font style
                )
            else:
                canvas.create_text(
                    label_pos_x,
                    label_pos_y,
                    text=play_type,  # Your label text
                    fill=font_color,  # Text color
                    font=(label_font, int(label_font_size * 0.5), "bold"),
                    anchor="w",  # Font style
                )
