from PySide6.QtWidgets import QFrame, QVBoxLayout, QDial, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont


class WidgetKeyNote(QFrame):

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
            background-image: url(ressources/gui/png/bckgnd-key_note.png);
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
        self.knob.setEnabled(False)
        # Label info
        self.lbl_info_size_ratio = 0.8
        self.lbl_info_properties = {
            "size_x": self.widget_width * self.lbl_info_size_ratio,
            "size_y": self.widget_height * 0.1,
            "font": lbl_font,
            "font_size": lbl_txt_size,
            "color": lbl_txt_color,
        }
        ## Key degree
        self.lbl_key_info = QLabel("Key degree", parent=self)
        self.lbl_key_info.setStyleSheet(
            f"""
            color: {self.lbl_info_properties["color"]};
            background: transparent;
            qproperty-alignment: AlignCenter;
            """
        )
        self.lbl_key_info.setFixedSize(
            self.lbl_info_properties["size_x"], self.lbl_info_properties["size_y"]
        )

        ## Octave
        self.lbl_octave_info = QLabel("Octave", parent=self)
        self.lbl_octave_info.setStyleSheet(
            f"""
            color: {self.lbl_info_properties["color"]};
            background: transparent;
            qproperty-alignment: AlignCenter;
            """
        )
        self.lbl_octave_info.setFixedSize(
            self.lbl_info_properties["size_x"], self.lbl_info_properties["size_y"]
        )

        ## Font info
        self.font_info = self.lbl_key_info.font()
        self.font_info.setFamily(self.lbl_info_properties["font"])
        self.font_info.setPointSize(self.lbl_info_properties["font_size"])
        self.lbl_key_info.setFont(self.font_info)
        self.lbl_octave_info.setFont(self.font_info)

        # Label value
        self.lbl_val_size_ratio = 0.8
        self.lbl_val_properties = {
            "size_x": self.widget_width * self.lbl_val_size_ratio,
            "size_y": self.widget_height * 0.1,
            "font": lbl_font,
            "font_size": lbl_note_size,
            "color": lbl_note_color,
        }
        ## Key degree
        self.lbl_key_val = QLabel("1", parent=self)
        self.lbl_key_val.setStyleSheet(
            f"""
            color: {self.lbl_val_properties["color"]};
            background: transparent;
            qproperty-alignment: AlignCenter;
            """
        )
        self.lbl_key_val.setFixedSize(
            self.lbl_val_properties["size_x"], self.lbl_val_properties["size_y"]
        )

        ## Octave
        self.lbl_octave_val = QLabel("0", parent=self)

        self.lbl_octave_val.setStyleSheet(
            f"""
            color: {self.lbl_val_properties["color"]};
            background: transparent;
            qproperty-alignment: AlignCenter;
            """
        )
        self.lbl_octave_val.setFixedSize(
            self.lbl_val_properties["size_x"], self.lbl_val_properties["size_y"]
        )

        ## Font val
        self.font_val = self.lbl_key_val.font()
        self.font_val.setFamily(self.lbl_val_properties["font"])
        self.font_val.setPointSize(self.lbl_val_properties["font_size"])
        self.lbl_key_val.setFont(self.font_val)
        self.lbl_octave_val.setFont(self.font_val)

        # Widget position
        self.knob_position = {
            "x": self.widget_width * (1 - self.knob_size_ratio) / 2,
            "y": self.widget_height * 0.05,
        }
        self.lbl_key_info_position = {
            "x": self.widget_width * (1 - self.lbl_info_size_ratio) / 2,
            "y": self.widget_height * 0.36,
        }
        self.lbl_octave_info_position = {
            "x": self.widget_width * (1 - self.lbl_info_size_ratio) / 2,
            "y": self.widget_height * 0.66,
        }
        self.lbl_key_val_position = {
            "x": self.widget_width * (1 - self.lbl_val_size_ratio) / 2,
            "y": self.widget_height * 0.51,
        }
        self.lbl_octave_val_position = {
            "x": self.widget_width * (1 - self.lbl_val_size_ratio) / 2,
            "y": self.widget_height * 0.8,
        }

        # Widget placement
        self.knob.move(self.knob_position["x"], self.knob_position["y"])
        self.lbl_key_info.move(
            self.lbl_key_info_position["x"], self.lbl_key_info_position["y"]
        )
        self.lbl_octave_info.move(
            self.lbl_octave_info_position["x"], self.lbl_octave_info_position["y"]
        )
        self.lbl_key_val.move(
            self.lbl_key_val_position["x"], self.lbl_key_val_position["y"]
        )
        self.lbl_octave_val.move(
            self.lbl_octave_val_position["x"], self.lbl_octave_val_position["y"]
        )

    def update(self, state):
        self.lbl_key_val.setText(f"{state["key_degree"]+1}")
        if state["key_note"] >= 0:
            self.lbl_octave_val.setText(f"{int(state["key_degree_octave"]/12)}")
        else:
            self.lbl_octave_val.setText(f"{int(state["key_degree_octave"]/12 - 1)}")
        self.knob.setValue(state["raw_key_knob"])
