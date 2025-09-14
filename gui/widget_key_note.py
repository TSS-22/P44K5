import tkinter as tk
from widget_utilities import WidgetUtilities


class WidgetKeyNote(tk.Frame, WidgetUtilities):

    arc_division = -(315 / 128)
    arc_height = 72
    arc_width = arc_height

    def __init__(
        self,
        master=None,
        canvas=None,
        widget_width=168,
        widget_height=415,
        canvas_width=1200,
        canvas_height=760,
        bckgnd_color="#260006",
        font_color="#340006",
        arc_color="#00ff00",
        label_font="Arial",
        label_font_size=36,
        rel_x=1 - 0.078,
        rel_y=0.715,
    ):
        super().__init__(master=master, width=widget_width, height=widget_height)
        self.pos_x = int(canvas_width * rel_x)
        self.pos_y = int(canvas_height * rel_y)

        # Background arc
        canvas.create_rectangle(
            # Bouding box
            self.pos_x - int(widget_width * 0.4),  # x0
            self.pos_y - int(widget_height * 0.47),  # y0
            self.pos_x + int(widget_width * 0.4),  # x1
            self.pos_y - int(widget_height * 0.1),  # y1
            fill=bckgnd_color,
            outline="",
        )

        # Indicator key note knob position
        self.kob_arc = canvas.create_arc(
            # Bouding box
            self.pos_x - self.arc_height,  # x0
            self.pos_y - int(widget_height * 0.475),  # y0
            self.pos_x + self.arc_height,  # x1
            self.pos_y - int(widget_height * 0.475) + self.arc_height * 1.93,  # y1
            start=225,
            extent=self.arc_division * 100,
            fill=arc_color,
            outline="",
        )

        # Background image
        self.tk_bckgnd_img = self.load_image(
            image_path="./res_2/png/bckgnd-key_note.png",
            width=widget_width,
            height=widget_height,
        )
        self.bckgnd = canvas.create_image(
            self.pos_x,
            self.pos_y,
            anchor=tk.CENTER,
            image=self.tk_bckgnd_img,
        )

        # Knob image
        self.tk_knob_img = self.load_image(
            image_path="./res_2/png/knob.png",
            width=int(widget_width * 0.7),
            height=int(widget_width * 0.7),
        )
        self.knob_img = canvas.create_image(
            self.pos_x,
            self.pos_y - int(widget_height * 0.3),
            anchor=tk.CENTER,
            image=self.tk_knob_img,
        )

        # Label background key degree
        canvas.create_text(
            self.pos_x,
            self.pos_y - int(widget_height * 0.08),  # Center of the image
            text="Key degree",  # Your label text
            fill=font_color,  # Text color
            font=(label_font, int(label_font_size * 0.5), "bold"),  # Font style
        )

        # Label background octave
        canvas.create_text(
            self.pos_x,
            self.pos_y + int(widget_height * 0.21),  # Center of the image
            text="Octave",  # Your label text
            fill=font_color,  # Text color
            font=(label_font, int(label_font_size * 0.5), "bold"),  # Font style
        )

        # Label key degree value
        self.label_key_note_val = canvas.create_text(
            self.pos_x,
            self.pos_y + int(widget_height * 0.07),  # Center of the image
            text="7",  # Your label text
            fill=arc_color,  # Text color
            font=(label_font, label_font_size, "bold"),  # Font style
        )

        # Label octave value
        self.label_octave_val = canvas.create_text(
            self.pos_x,
            self.pos_y + int(widget_height * 0.35),  # Center of the image
            text="+3",  # Your label text
            fill=arc_color,  # Text color
            font=(label_font, label_font_size, "bold"),  # Font style
        )
