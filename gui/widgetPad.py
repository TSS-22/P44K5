from PySide6.QtWidgets import QFrame, QPushButton, QStackedLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont


class WidgetPad(QFrame):

    def __init__(
        self,
        parent=None,
        note="C -3",
        root=False,
        chord_name="",
        pad_pressed=False,
        widget_width=180,
        widget_height=180,
        font="Liberation sans",
        font_size=48,
        font_color="#00ff00",
    ):
        super().__init__(parent=parent)
        self.widget_width = widget_width
        self.widget_height = widget_height
        self.setFixedSize(self.widget_width, self.widget_height)
        self.root = root
        self.pad_pressed = pad_pressed

        if self.root:
            self.bckgnd_button = "bckgnd-pad_root.png"
        else:
            self.bckgnd_button = "bckgnd-pad.png"

        if self.pad_pressed:
            self.bckgnd_active = "bckgnd-pad_active.png"
        else:
            self.bckgnd_active = "bckgnd-pad_inactive.png"

        self.lbl_note_properties = {
            "font": font,
            "font_size": font_size,
            "color": font_color,
            "note": note,
        }

        self.setStyleSheet(
            """
                border: none; 
                background: transparent;	
            """
        )

        self.active = QLabel(parent=self, text="")
        self.active.setFixedSize(self.widget_width, self.widget_height)
        self.active.setStyleSheet(
            f"""
                background-repeat: no-repeat;
                background-position: center;
                border: none; 	
                background-image: url(ressources/gui/png/{self.bckgnd_active});
            """
        )

        self.note_font = QFont()
        self.note_font.setFamily(self.lbl_note_properties["font"])
        self.note_font.setPointSize(self.lbl_note_properties["font_size"])

        self.button = QPushButton(parent=self, text=self.lbl_note_properties["note"])
        self.button.setFont(self.note_font)
        self.button.setFixedSize(self.widget_width, self.widget_height)
        self.button.setStyleSheet(
            f"""
                background-repeat: no-repeat;
                background-position: center;
                border: none; 	
                background-image: url(ressources/gui/png/{self.bckgnd_button});
                color: {font_color};
            """
        )

        # Label chord comp
        self.lbl_chord = QLabel(note.split()[0], parent=self)
        self.lbl_chord_properties = {
            "size_x": self.widget_width,
            "size_y": self.widget_height * 0.1,
            "font": font,
            "font_size": font_size * 0.20,
            "color": font_color,
        }
        self.chord_font = self.lbl_chord.font()
        self.chord_font.setFamily(self.lbl_chord_properties["font"])
        self.chord_font.setPointSize(self.lbl_chord_properties["font_size"])
        self.lbl_chord.setFont(self.chord_font)

        self.lbl_chord.setStyleSheet(
            f"""
            color: {self.lbl_chord_properties["color"]};
            background: transparent; 
            """
        )
        self.lbl_chord.setFixedSize(
            self.lbl_chord_properties["size_x"], self.lbl_chord_properties["size_y"]
        )
        self.lbl_chord_position = {
            "x": self.widget_width * 0.1,
            "y": self.widget_height * 0.80,
        }
        self.lbl_chord.move(self.lbl_chord_position["x"], self.lbl_chord_position["y"])

        # Label chord name
        self.lbl_chord_name = QLabel(chord_name, parent=self)
        self.lbl_chord_name.setFont(self.chord_font)
        self.lbl_chord_name.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lbl_chord_name.setStyleSheet(
            f"""
            color: {self.lbl_chord_properties["color"]};
            background: transparent; 
            """
        )
        self.lbl_chord_name.setFixedSize(
            self.lbl_chord_properties["size_x"], self.lbl_chord_properties["size_y"]
        )
        self.lbl_chord_name_position = {
            "x": -0.1 * self.widget_height,
            "y": self.widget_height * 0.70,
        }
        self.lbl_chord_name.move(
            self.lbl_chord_name_position["x"], self.lbl_chord_name_position["y"]
        )

    def update_bckgrnd_only(self, widget, background_style):
        current_style = widget.styleSheet()
        properties = [p.strip() for p in current_style.split(";") if p.strip()]
        # Remove any existing border property
        properties = [p for p in properties if not p.startswith("background-image:")]
        # Add the new border style
        properties.append(background_style)
        # Rejoin and set
        widget.setStyleSheet(";".join(properties))

    #  Redo the whole structure of the pad background and stuff/ most likely resort to border in order to lower the computationnal cost
    def put_root_backgrnd(self, is_root):
        # Reapply the style sheet
        if is_root:
            background_style = (
                "background-image: url(ressources/gui/png/bckgnd-pad_root.png);"
            )
        else:
            background_style = (
                "background-image: url(ressources/gui/png/bckgnd-pad.png);"
            )
        self.update_bckgrnd_only(self.button, background_style)

    def put_pressed_backgrnd(self, is_pressed):
        if is_pressed:
            background_style = (
                "background-image: url(ressources/gui/png/bckgnd-pad_active.png);"
            )
        else:
            background_style = (
                "background-image: url(ressources/gui/png/bckgnd-pad_inactive.png);"
            )
        self.update_bckgrnd_only(self.active, background_style)
