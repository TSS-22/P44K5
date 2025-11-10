from PySide6.QtWidgets import QFrame, QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont
from gui.widgetPad import WidgetPad
from logic.gui.map_note import map_note


class WidgetPadGrid(QFrame):

    list_note = [
        "C -3",
        "C# -3",
        "D -3",
        "D# -3",
        "E -3",
        "F -3",
        "F# -3",
        "G -3",
    ]  # HARDOCDED + TEST

    def __init__(
        self,
        parent=None,
        widget_width=818,
        widget_height=418,
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
            background-image: url(ressources/gui/png/bckgnd-pad_grid.png);
            """
        )
        self.pads = []
        self.grid_layout = QGridLayout(self)
        id_note = 0
        for row in range(1, -1, -1):
            for col in range(4):
                if row == 1 and col == 0:
                    pad = WidgetPad(
                        parent=self, root=True, note=self.list_note[id_note]
                    )
                else:
                    pad = WidgetPad(parent=self, note=self.list_note[id_note])
                self.pads.append(
                    {
                        "pad": pad,
                        "row": row,
                        "col": col,
                    }
                )
                self.grid_layout.addWidget(pad, row, col)
                id_note = id_note + 1

    def update(self, pad_grid_val):
        idx_base_note = pad_grid_val["base_note"] % 12
        base_octave = int(pad_grid_val["base_note"] / 12) - 3

        list_note = []
        temp_corrected_pad_intervals = (
            pad_grid_val["pad_intervals"][1:][::-1][: pad_grid_val["key_degree"]][::-1]
            + pad_grid_val["pad_intervals"][
                1 : len(pad_grid_val["pad_intervals"]) - pad_grid_val["key_degree"] :
            ]
        )
        corrected_pad_intervals = (
            [
                sum(
                    temp_corrected_pad_intervals[: pad_grid_val["key_degree"]][
                        : pad_grid_val["key_degree"]
                    ]
                )
            ]
            + temp_corrected_pad_intervals[pad_grid_val["key_degree"] :]
            + temp_corrected_pad_intervals[: pad_grid_val["key_degree"]]
        )
        for idx, _ in enumerate(pad_grid_val["velocity"]):
            note_correction = sum(corrected_pad_intervals[: idx + 1])
            list_note.append(map_note[(idx_base_note + note_correction) % 12])
        if pad_grid_val["key_note"] >= 0:
            key_octave = pad_grid_val["key_degree_octave"] / 12
        else:
            key_octave = int(pad_grid_val["key_degree_octave"] / 12 - 1)
        octave_corrected = base_octave + key_octave
        octave_correction = [0] * (8 - pad_grid_val["key_degree"] - 1) + [1] * (
            pad_grid_val["key_degree"] + 1
        )
        for idx, velocity in enumerate(pad_grid_val["velocity"]):
            # Root
            if idx == pad_grid_val["key_degree"]:
                self.pads[idx]["pad"].put_root_backgrnd(True)
            else:
                self.pads[idx]["pad"].put_root_backgrnd(False)
            # Pressed
            if velocity > 0:
                print("test")
                self.pads[idx]["pad"].put_pressed_backgrnd(True)
            else:
                self.pads[idx]["pad"].put_pressed_backgrnd(False)
            # Note
            self.pads[idx]["pad"].button.setText(
                f"{list_note[idx]} {int(octave_corrected + octave_correction[idx])}"
            )
            # if idx < pad_grid_val["key_degree"]:
            #     note_correction = -sum(
            #         pad_grid_val["pad_intervals"][::-1][
            #             idx + 1 : pad_grid_val["key_degree"] + 1
            #         ]
            #     )

            #     # self.pads[idx]["pad"].button.setText(
            #     #     map_note[idx_base_note + note_correction]
            #     # )
            #     self.pads[idx]["pad"].button.setText("P")
            # elif idx == pad_grid_val["key_degree"]:
            #     self.pads[idx]["pad"].button.setText(
            #         map_note[idx_base_note]
            #     )
            # else:
            #     print(f"correction: {pad_grid_val["pad_intervals"]}\n")
            #     note_correction = sum(pad_grid_val["pad_intervals"][: idx + 1])
            #     self.pads[idx]["pad"].button.setText(
            #         map_note[(idx_base_note + note_correction) % 12]
            #     )
