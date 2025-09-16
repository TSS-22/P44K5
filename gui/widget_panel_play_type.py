import tkinter as tk
from widget_utilities import WidgetUtilities
import math


class WidgetPanelPlayType(tk.Frame, WidgetUtilities):

    list_play_type = [
        "Single",
        "Normal",
        "Major",
        "Minor",
        "Dom7",
        "Dim",
    ]  # HARDCODED

    def __init__(
        self,
        master=None,
        canvas=None,
        widget_width=654,
        widget_height=266,
        canvas_width=1200,
        canvas_height=760,
        font_color="#340006",
        label_font="Arial",
        label_font_size=36,
        rel_x=0.078,
        rel_y=0.19,
    ):
        super().__init__(master=master, width=widget_width, height=widget_height)
        self.pos_x = int(canvas_width * rel_x) + 244  # HARDCODED
        self.pos_y = int(canvas_height * rel_y)

        # Background image
        self.tk_bckgnd_img = self.load_image(
            image_path="./res_2/png/backgnd-panel_play.png",
            width=widget_width,
            height=widget_height,
        )
        self.bckgnd = canvas.create_image(
            self.pos_x,
            self.pos_y,
            anchor=tk.CENTER,
            image=self.tk_bckgnd_img,
        )

        # Wheel slice image
        self.tk_wheel_slice_img = self.load_image(
            image_path="./res_2/png/camembert_play_225.png",
            width=int(widget_height * 0.6),  # HARDCODED
            height=int(widget_height * 0.6),  # HARDCODED
        )
        self.wheel_slice_img = canvas.create_image(
            self.pos_x - widget_width * 0.2,
            self.pos_y + int(widget_height * 0.118),
            anchor=tk.CENTER,
            image=self.tk_wheel_slice_img,
        )

        # Wheel image
        self.tk_wheel_img = self.load_image(
            image_path="./res_2/png/wheel_play_225.png",
            width=int(widget_height * 0.6),  # HARDCODED
            height=int(widget_height * 0.6),  # HARDCODED
        )
        self.wheel_img = canvas.create_image(
            self.pos_x - widget_width * 0.2,
            self.pos_y + int(widget_height * 0.118),
            anchor=tk.CENTER,
            image=self.tk_wheel_img,
        )

        # Knob image
        self.tk_knob_img = self.load_image(
            image_path="./res_2/png/knob.png",
            width=int(168 * 0.7),  # HARDCODED
            height=int(168 * 0.7),  # HARDCODED
        )
        self.knob_img = canvas.create_image(
            self.pos_x - widget_width * 0.2,
            self.pos_y + int(widget_height * 0.118),
            anchor=tk.CENTER,
            image=self.tk_knob_img,
        )

        # Labels background play
        for idx, play_type in enumerate(self.list_play_type):
            base = 135 + 18
            angle_deg = idx * (270 / 6) + base  # Evenly spaced angles
            angle_rad = math.radians(angle_deg)
            label_pos_x = (
                self.pos_x
                - widget_width * 0.2
                + int((widget_height * 1.1) / 3) * math.cos(angle_rad)
            )
            label_pos_y = (
                self.pos_y
                + int(widget_height * 0.118)
                + (int((widget_height * 1.1) / 3)) * math.sin(angle_rad)
            )
            if idx < 2:
                canvas.create_text(
                    label_pos_x,
                    label_pos_y,
                    text=play_type,  # Your label text
                    fill=font_color,  # Text color
                    font=(label_font, int(label_font_size * 0.5), "bold"),
                    anchor="e",  # Font style
                )

            elif idx == 2:
                canvas.create_text(
                    label_pos_x,
                    label_pos_y,
                    text=play_type,  # Your label text
                    fill=font_color,  # Text color
                    font=(label_font, int(label_font_size * 0.5), "bold"),
                    anchor="se",  # Font style
                )
            elif idx == 3:
                canvas.create_text(
                    label_pos_x,
                    label_pos_y,
                    text=play_type,  # Your label text
                    fill=font_color,  # Text color
                    font=(label_font, int(label_font_size * 0.5), "bold"),
                    anchor="sw",  # Font style
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
