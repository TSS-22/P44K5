from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont
from gui.widgetWheelChoice import WidgetWheelChoice


class WidgetPanelMode(QFrame):

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
        parent=None,
        widget_width=488,
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
            background-image: url(ressources/gui/png/bckgnd-panel_choices.png);
            """
        )
        self.wheel_mode = WidgetWheelChoice(
            list_val=self.list_mode,
            widget_height=self.widget_height,
            widget_width=self.widget_width,
            parent=self,
        )

    def update(self, panel_mode_val):
        self.wdgt_panel_mode.wheel_mode.knob.setValue(
            (panel_mode_val["raw_knob_mode"] / 127)
            * len(self.wdgt_panel_mode.list_mode)
        )
        idx = self.wdgt_panel_mode.list_mode.index(panel_mode_val["selected_mode"])
        self.wdgt_panel_mode.wheel_mode.radio_button[idx].setChecked(True)
