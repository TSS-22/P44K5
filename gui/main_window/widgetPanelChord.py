from PySide6.QtWidgets import QFrame, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont
from gui.main_window.widgetWheelChoice import WidgetWheelChoice

from data.data_general import hc_chord_comp_name, hc_chord_size_name


class WidgetPanelChord(QFrame):
    # CLEAN
    # list_chord_comp = [
    #     "Single",
    #     "Normal",
    #     "Major",
    #     "Minor",
    #     "Dom",
    #     "Dim",
    # ]

    # list_chord_size = [
    #     "5",
    #     "X",
    #     "6",
    #     "7",
    #     "9",
    #     "11",
    #     "13",
    # ]

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
            background-image: url(ressources/gui/png/backgnd-panel_chord.png);
            """
        )

        self.wheel_chord_comp = WidgetWheelChoice(
            list_val=hc_chord_comp_name,
            widget_height=self.widget_height,
            widget_width=self.widget_width / 2,
            parent=self,
            lbl_font_size=lbl_font_size * 0.75,
        )

        self.wheel_chord_size = WidgetWheelChoice(
            list_val=hc_chord_size_name,
            widget_height=self.widget_height,
            widget_width=self.widget_width / 2,
            parent=self,
        )

        self.layout = QHBoxLayout(self)

        self.layout.addWidget(self.wheel_chord_comp)
        self.layout.addWidget(self.wheel_chord_size)

    def update_chord_comp(self, state):
        self.wheel_chord_comp.knob.setValue(state["idx_chord_comp"])
        idx = hc_chord_comp_name.index(state["selected_chord_comp"]["name"])
        self.wheel_chord_comp.radio_button[idx].setChecked(True)

    def update_chord_size(self, state):
        self.wheel_chord_size.knob.setValue(state["idx_chord_size"])
        idx = hc_chord_size_name.index(state["selected_chord_size"]["name"])
        self.wheel_chord_size.radio_button[idx].setChecked(True)
