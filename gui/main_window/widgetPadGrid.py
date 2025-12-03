from PySide6.QtWidgets import QFrame, QGridLayout
from PySide6.QtCore import Signal
from PySide6.QtGui import QShortcut
from PySide6.QtCore import Qt
from gui.main_window.widgetPad import WidgetPad
from data.data_general import hc_list_note_startup, hc_shortcut_pads


class WidgetPadGrid(QFrame):
    list_note = hc_list_note_startup
    sig_pad_pressed = Signal(int)
    sig_pad_released = Signal(int)

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
                        parent=self,
                        id_pad=id_note,
                        root=True,
                        note=self.list_note[id_note],
                    )
                else:
                    pad = WidgetPad(
                        parent=self, id_pad=id_note, note=self.list_note[id_note]
                    )
                self.pads.append(
                    {
                        "pad": pad,
                        "row": row,
                        "col": col,
                    }
                )
                self.grid_layout.addWidget(pad, row, col)
                self.pads[id_note]["pad"].sig_pressed.connect(self.on_pad_pressed)
                self.pads[id_note]["pad"].sig_released.connect(self.on_pad_released)
                id_note = id_note + 1

    def update(self, state):
        for idx, velocity in enumerate(state["velocity"]):
            # Note/Chord display
            self.pads[idx]["pad"].button.setText(
                f"{state['pad_notes'][idx]} {state['pad_octaves'][idx]}"
            )
            self.pads[idx]["pad"].lbl_chord.setText(
                " - ".join(state["pad_notes_chords"][idx])
            )
            self.pads[idx]["pad"].lbl_chord_name.setText(state["name_chords"][idx])
            # Root
            self.pads[idx]["pad"].put_root_backgrnd(state["pad_roots"][idx])

            # Pressed
            if velocity > 0:
                self.pads[idx]["pad"].put_pressed_backgrnd(True)
            else:
                self.pads[idx]["pad"].put_pressed_backgrnd(False)

    def on_pad_pressed(self, id_pad):
        self.sig_pad_pressed.emit(id_pad)

    def on_pad_released(self, id_pad):
        self.sig_pad_released.emit(id_pad)
