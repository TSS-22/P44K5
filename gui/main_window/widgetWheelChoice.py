import math

from PySide6.QtWidgets import (
    QFrame,
    QDial,
    QButtonGroup,
    QRadioButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont


class WidgetWheelChoice(QFrame):
    def __init__(
        self,
        list_val,
        widget_width,
        widget_height,
        lbl_font="Liberation sans",
        lbl_font_size=20,
        lbl_font_color="#340006",
        knob_color="#eeeeee",
        parent=None,
    ):
        super().__init__(parent)
        self.widget_width = widget_width
        self.widget_height = widget_height
        self.list_val = list_val
        self.setStyleSheet(
            """
            border: none;
            background: transparent;
            """
        )

        # Knob
        self.knob_size_ratio = 0.50
        self.knob_properties = {
            "size": self.widget_height * self.knob_size_ratio,
            "val_min": 0,
            "val_max": len(self.list_val),
            "val_start": 0,
        }
        self.knob = QDial(parent=self, notchesVisible=True)
        self.knob.setStyleSheet(
            """
            border: none;
            background: white;
            """
        )
        self.knob.setFixedSize(
            self.knob_properties["size"], self.knob_properties["size"]
        )
        self.knob.setMinimum(self.knob_properties["val_min"])
        self.knob.setMaximum(self.knob_properties["val_max"] - 1)
        self.knob.setValue(self.knob_properties["val_start"])

        self.knob_palette = self.knob.palette()
        self.knob_palette.setColor(QPalette.Button, QColor(knob_color))
        self.knob_palette.setColor(QPalette.Dark, QColor(lbl_font_color))
        self.knob.setPalette(self.knob_palette)

        # Radio buttons mode

        self.radio_button_properties = {
            "rot_center_x": self.widget_width * 0.5,
            "rot_center_y": self.widget_height * 0.5 + self.widget_height * 0.08,
            "angle_start": 240 - (300 / len(self.list_val) / 2),
            "angle_end": -60 + (300 / len(self.list_val) / 2),
            "radius": self.knob.height() * 0.6,
            "font": lbl_font,
            "font_size": lbl_font_size,
            "size": 1.6 * lbl_font_size,
            "style_sheet": """
                QRadioButton{
                    background:transparent;
                    text-align: center;
                }
                QRadioButton:checked {
                    color: #00ff00;
                }
                QRadioButton:disabled {
                    color: gray;
                }
            """,
        }
        # color: {lbl_font_color};
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(lbl_font_color))

        self.radio_button_font = QFont()
        self.radio_button_font.setFamily(self.radio_button_properties["font"])
        self.radio_button_font.setPointSize(self.radio_button_properties["font_size"])

        self.radio_button_group = QButtonGroup()
        self.radio_button = []

        size_x = 0
        for idx, mode in enumerate(self.list_val):
            if idx == 0:
                size_x = self.radio_button_properties["font_size"] * len(mode)
            elif self.radio_button_properties["font_size"] * len(mode) > size_x:
                size_x = self.radio_button_properties["font_size"] * len(mode)

        size_x = size_x + self.radio_button_properties["font_size"]

        for idx, mode in enumerate(self.list_val):
            radio = QRadioButton(mode, self)
            self.radio_button.append(radio)
            self.radio_button_group.addButton(radio, idx)

            # Set the radio button
            self.radio_button[idx].setStyleSheet(
                self.radio_button_properties["style_sheet"]
            )
            self.radio_button[idx].setPalette(palette)

            self.radio_button[idx].setFont(self.radio_button_font)
            if idx < len(self.list_val) / 2:
                self.radio_button[idx].setLayoutDirection(Qt.RightToLeft)

            self.radio_button[idx].setFixedSize(
                size_x,
                self.radio_button_properties["size"],
            )
            # Calculate angle for each radio button
            angle = math.radians(
                self.radio_button_properties["angle_start"]
                + (
                    self.radio_button_properties["angle_end"]
                    - self.radio_button_properties["angle_start"]
                )
                * idx
                / (len(self.list_val) - 1)
            )

            # Calculate position
            if idx < len(self.list_val) / 2:
                x = (
                    self.radio_button_properties["rot_center_x"]
                    - size_x
                    + self.radio_button_properties["radius"] * math.cos(angle)
                )
                y = (
                    self.radio_button_properties["rot_center_y"]
                    # - self.radio_button_properties["size"] / 2
                    - self.radio_button_properties["radius"] * math.sin(angle)
                ) * 0.95
            else:
                x = (
                    self.radio_button_properties["rot_center_x"]
                    # + size_x / 2
                    + self.radio_button_properties["radius"] * math.cos(angle)
                )
                y = (
                    self.radio_button_properties["rot_center_y"]
                    # - self.radio_button_properties["size"] / 2
                    - self.radio_button_properties["radius"] * math.sin(angle)
                ) * 0.95

            self.radio_button[idx].move(
                x,
                y,
            )

        self.radio_button[0].setChecked(True)

        # Widget positions
        self.knob_position = {
            "x": (self.widget_width - self.knob.width()) * 0.5,
            "y": (self.widget_height - self.knob.height()) * 0.5
            + self.widget_height * 0.1,
        }

        # Widget placement
        self.knob.move(self.knob_position["x"], self.knob_position["y"])
