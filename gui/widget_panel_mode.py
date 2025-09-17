import tkinter as tk
import math
from gui.image_item import ImageItem


class WidgetPanelMode(tk.Frame):

    list_mode = [
        "None",
        "Ionian",
        "Dorian",
        "Phrygian",
        "Lydian",
        "Myxolydian",
        "Aeolian",
        "Locrian",
    ]  # HARDCODED

    def __init__(
        self,
        master=None,
        canvas=None,
        widget_width=488,
        widget_height=266,
        canvas_width=1200,
        canvas_height=760,
        font_color="#340006",
        label_font="Arial",
        label_font_size=36,
        rel_x=1 - 0.078,
        rel_y=0.19,
    ):
        super().__init__(master=master, width=widget_width, height=widget_height)
        self.pos_x = int(canvas_width * rel_x) - 161  # HARDCODED
        self.pos_y = int(canvas_height * rel_y)
        self.widget_width = widget_width
        self.widget_height = widget_height

        # Background image
        self.img_bckgnd = ImageItem(
            canvas=canvas,
            image_path="./res_2/png/bckgnd-panel_choices.png",
            width=widget_width,
            height=widget_height,
            x=self.pos_x,
            y=self.pos_y,
        )

        # Wheel slice image
        self.img_wheel_slice = ImageItem(
            canvas=canvas,
            image_path="./res_2/png/camembert_mode_225.png",
            width=int(widget_height * 0.6),
            height=int(widget_height * 0.6),
            x=self.pos_x,
            y=self.pos_y + int(widget_height * 0.118),
        )

        # Wheel image
        self.img_wheel = ImageItem(
            canvas=canvas,
            image_path="./res_2/png/wheel_mode_225.png",
            width=int(widget_height * 0.6),
            height=int(widget_height * 0.6),
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

        # Labels background mode
        for idx, mode in enumerate(self.list_mode):
            base = 135 + 18
            angle_deg = idx * (270 / 8) + base  # Evenly spaced angles
            angle_rad = math.radians(angle_deg)
            label_pos_x = self.pos_x + int((widget_height * 1.1) / 3) * math.cos(
                angle_rad
            )
            label_pos_y = (
                self.pos_y
                + int(widget_height * 0.118)
                + (int((widget_height * 1.1) / 3)) * math.sin(angle_rad)
            )
            if idx < 3:
                canvas.create_text(
                    label_pos_x,
                    label_pos_y,
                    text=mode,  # Your label text
                    fill=font_color,  # Text color
                    font=(label_font, int(label_font_size * 0.5), "bold"),
                    anchor="e",  # Font style
                )

            elif idx == 3:
                canvas.create_text(
                    label_pos_x,
                    label_pos_y,
                    text=mode,  # Your label text
                    fill=font_color,  # Text color
                    font=(label_font, int(label_font_size * 0.5), "bold"),
                    anchor="se",  # Font style
                )
            elif idx == 4:
                canvas.create_text(
                    label_pos_x,
                    label_pos_y,
                    text=mode,  # Your label text
                    fill=font_color,  # Text color
                    font=(label_font, int(label_font_size * 0.5), "bold"),
                    anchor="sw",  # Font style
                )
            else:
                canvas.create_text(
                    label_pos_x,
                    label_pos_y,
                    text=mode,  # Your label text
                    fill=font_color,  # Text color
                    font=(label_font, int(label_font_size * 0.5), "bold"),
                    anchor="w",  # Font style
                )
