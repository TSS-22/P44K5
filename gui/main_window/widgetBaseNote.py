from PySide6.QtWidgets import QFrame, QDial, QLabel
from PySide6.QtGui import QPalette, QColor

from data.data_general import hc_offset_midi_octave, hc_chromatic_scale


class WidgetBaseNote(QFrame):
    def __init__(
        self,
        parent=None,
        widget_width=168,
        widget_height=416,
        canvas_width=1200,
        canvas_height=760,
        knob_color="#eeeeee",
        lbl_font="Liberation sans",
        lbl_txt_size=20,
        lbl_txt_color="#340006",
        lbl_note_size=36,
        lbl_note_color="#00ff00",
        rel_x=0.078,
        rel_y=0.715,
    ):
        super().__init__(parent)

        self.pos_x = int(canvas_width * rel_x)
        self.pos_y = int(canvas_height * rel_y)
        self.widget_width = widget_width
        self.widget_height = widget_height

        self.setFixedSize(self.widget_width, self.widget_height)
        self.setStyleSheet(
            """            
            background-repeat: no-repeat;
            background-position: center;
            border: none; 	
            background-image: url(ressources/gui/png/bckgnd-base_note.png);
            """
        )

        # Knob
        self.knob_size_ratio = 0.65
        self.knob_properties = {
            "size": self.widget_width * self.knob_size_ratio,
            "val_min": 0,
            "val_max": 127,
            "val_start": 0,
        }
        self.knob = QDial(parent=self, notchesVisible=True)
        self.knob.setFixedSize(
            self.knob_properties["size"], self.knob_properties["size"]
        )

        self.knob.setMinimum(self.knob_properties["val_min"])
        self.knob.setMaximum(self.knob_properties["val_max"])
        self.knob.setValue(self.knob_properties["val_start"])

        self.knob_palette = self.knob.palette()
        self.knob_palette.setColor(QPalette.Button, QColor(knob_color))
        self.knob_palette.setColor(QPalette.Dark, QColor(lbl_txt_color))
        self.knob.setPalette(self.knob_palette)

        # Label info
        self.lbl_txt_size_ratio = 0.8
        self.lbl_txt_properties = {
            "size_x": self.widget_width * self.lbl_txt_size_ratio,
            "size_y": self.widget_height * 0.1,
            "font": lbl_font,
            "font_size": lbl_txt_size,
            "color": lbl_txt_color,
        }
        self.lbl_txt = QLabel("Base note", parent=self)
        self.font_txt = self.lbl_txt.font()
        self.font_txt.setFamily(self.lbl_txt_properties["font"])
        self.font_txt.setPointSize(self.lbl_txt_properties["font_size"])
        self.lbl_txt.setFont(self.font_txt)
        self.lbl_txt.setStyleSheet(
            f"""
            color: {self.lbl_txt_properties["color"]};
            background: transparent;
            qproperty-alignment: AlignCenter;
            """
        )
        self.lbl_txt.setFixedSize(
            self.lbl_txt_properties["size_x"], self.lbl_txt_properties["size_y"]
        )

        # Label base note
        self.lbl_note_size_ratio = 0.8
        self.lbl_note_properties = {
            "size_x": self.widget_width * self.lbl_note_size_ratio,
            "size_y": self.widget_height * 0.1,
            "font": lbl_font,
            "font_size": lbl_note_size,
            "color": lbl_note_color,
        }
        self.lbl_note = QLabel("C -2", parent=self)
        self.font_txt = self.lbl_note.font()
        self.font_txt.setFamily(self.lbl_note_properties["font"])
        self.font_txt.setPointSize(self.lbl_note_properties["font_size"])
        self.lbl_note.setFont(self.font_txt)
        self.lbl_note.setStyleSheet(
            f"""
            color: {self.lbl_note_properties["color"]};
            background: transparent;
            qproperty-alignment: AlignCenter;
            """
        )
        self.lbl_note.setFixedSize(
            self.lbl_note_properties["size_x"], self.lbl_note_properties["size_y"]
        )

        # Widget position
        self.knob_position = {
            "x": self.widget_width * (1 - self.knob_size_ratio) / 2,
            "y": self.widget_height * 0.05,
        }
        self.lbl_txt_position = {
            "x": self.widget_width * (1 - self.lbl_txt_size_ratio) / 2,
            "y": self.widget_height * 0.4,
        }
        self.lbl_note_position = {
            "x": self.widget_width * (1 - self.lbl_note_size_ratio) / 2,
            "y": self.widget_height * 0.65,
        }
        # Widget placement
        self.knob.move(self.knob_position["x"], self.knob_position["y"])
        self.lbl_txt.move(self.lbl_txt_position["x"], self.lbl_txt_position["y"])
        self.lbl_note.move(self.lbl_note_position["x"], self.lbl_note_position["y"])

        self.setStatusTip("Select your root note and corresponding octave.")

    def update(self, state):
        self.knob.setValue(state)
        note = hc_chromatic_scale[state % 12]
        octave = int(state / 12) + hc_offset_midi_octave
        self.lbl_note.setText(f"{note} {octave}")
