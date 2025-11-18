from PySide6.QtWidgets import QFrame, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont
from gui.widgetWheelChoice import WidgetWheelChoice


class WidgetPanelChord(QFrame):

    list_chord_type = [
        "Single",
        "Normal",
        "Major",
        "Minor",
        "Dom",
        "Dim",
    ]

    list_chord_size = [
        "5",
        "X",
        "6",
        "7",
        "9",
        "11",
        "13",
    ]

    def __init__(
        self,
        parent=None,
        widget_width=654,
        widget_height=266,
        canvas_width=1200,
        canvas_height=760,
        knob_color="#eeeeee",
        lbl_font="Liberation sans",
        lbl_font_size=20,
        lbl_font_color="#340006",
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
            background-image: url(ressources/gui/png/backgnd-panel_play.png);
            """
        )

        self.wheel_type = WidgetWheelChoice(
            list_val=self.list_chord_type,
            widget_height=self.widget_height,
            widget_width=self.widget_width / 2,
            parent=self,
            lbl_font_size=lbl_font_size * 0.75,
        )

        self.wheel_chord_size = WidgetWheelChoice(
            list_val=self.list_chord_size,
            widget_height=self.widget_height,
            widget_width=self.widget_width / 2,
            parent=self,
        )

        self.layout = QHBoxLayout(self)

        self.layout.addWidget(self.wheel_type)
        self.layout.addWidget(self.wheel_chord_size)

    def update_chord(self, panel_chord_val):
        self.wheel_chord_size.knob.setValue(
            (panel_chord_val["raw_knob_chord_type"] / 127) * len(self.list_chord_size)
        )
        idx = self.list_chord_size.index(panel_chord_val["selected_chord_size"]["name"])
        self.wheel_chord_size.radio_button[idx].setChecked(True)

    def update_play(self, panel_play_val):
        self.wheel_type.knob.setValue(
            (panel_play_val["raw_knob_play_type"] / 127) * len(self.list_chord_type)
        )
        #  Bad  data architecture correct this
        if panel_play_val["selected_play_type"] == "Single":
            idx = 0
        else:
            idx = self.list_chord_type.index(
                panel_play_val["selected_play_type"]["name"]
            )
        self.wheel_type.radio_button[idx].setChecked(True)
