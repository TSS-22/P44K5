import sys
import math
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import QThread, QThreadPool, Slot

from gui_qt.widgetBaseNote import WidgetBaseNote
from gui_qt.widgetKeyNote import WidgetKeyNote
from gui_qt.widgetPanelMode import WidgetPanelMode
from gui_qt.widgetPanelChord import WidgetPanelChord
from gui_qt.widgetPadGrid import WidgetPadGrid

from qt_logic.qt_midi_connector import QtMidiConnector
from qt_logic.main_logic import MainLogic
from qt_logic.map_note import map_note


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.logic = MainLogic()
        self.logic.signal.base_note_changed.connect(self.updt_base_note)
        self.logic.signal.key_note_changed.connect(self.updt_key_degree)
        self.logic.signal.panel_mode_changed.connect(self.updt_panel_mode)
        self.logic.signal.panel_chord_changed.connect(self.updt_panel_chord)
        self.logic.signal.panel_play_changed.connect(self.updt_panel_play)
        self.logic.signal.pad_grid_changed.connect(self.updt_pad_grid)

        # Connecting the MidiCOntroller and MidiBridge to the UI
        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        self.worker = QtMidiConnector()

        self.worker.signals.midi_messages.connect(self.logic.handle_midi)

        self.threadpool.start(self.worker)

        self.setWindowTitle("8P4K PowerHouse")
        self.setStyleSheet(
            """            
            background-repeat: no-repeat;
            background-position: center;
            border: none; 	
            background-image: url(qt-ressources/png/bckgnd-app.png);
            """
        )

        self.wdgt_base_note = WidgetBaseNote(self)
        self.wdgt_key_note = WidgetKeyNote(self)
        self.wdgt_panel_mode = WidgetPanelMode(self)
        self.wdgt_panel_chord = WidgetPanelChord(self)
        self.wdgt_pad_grid = WidgetPadGrid(self)

        self.layout_col = QVBoxLayout(self)
        self.layout_row_up = QHBoxLayout(self)
        self.layout_row_down = QHBoxLayout(self)

        self.layout_row_up.addWidget(self.wdgt_panel_mode)
        self.layout_row_up.addWidget(self.wdgt_panel_chord)

        self.layout_row_down.addWidget(self.wdgt_base_note)
        self.layout_row_down.addWidget(self.wdgt_pad_grid)
        self.layout_row_down.addWidget(self.wdgt_key_note)

        self.layout_col.addLayout(self.layout_row_up)
        self.layout_col.addLayout(self.layout_row_down)

        self.layout_container = QWidget()
        self.layout_container.setLayout(self.layout_col)
        self.setCentralWidget(self.layout_container)

    def closeEvent(self, event):
        # Ask the worker to stop
        self.worker.stop()
        event.accept()

    @Slot()
    def updt_base_note(self, base_note_val):
        self.wdgt_base_note.knob.setValue(base_note_val)
        note = map_note[base_note_val % 12]
        octave = int(base_note_val / 12) - 3
        self.wdgt_base_note.lbl_note.setText(f"{note} {octave}")

    @Slot()
    def updt_key_degree(self, key_deg_val):
        self.wdgt_key_note.lbl_key_val.setText(f"{key_deg_val["key_degree"]+1}")
        if key_deg_val["key_note"] >= 0:
            self.wdgt_key_note.lbl_octave_val.setText(
                f"{int(key_deg_val["key_degree_octave"]/12)}"
            )
        else:
            self.wdgt_key_note.lbl_octave_val.setText(
                f"{int(key_deg_val["key_degree_octave"]/12 - 1)}"
            )
        self.wdgt_key_note.knob.setValue(key_deg_val["raw_key_knob"])

    @Slot()
    def updt_panel_mode(self, panel_mode_val):
        self.wdgt_panel_mode.wheel_mode.knob.setValue(
            (panel_mode_val["raw_knob_mode"] / 127)
            * len(self.wdgt_panel_mode.list_mode)
        )
        idx = self.wdgt_panel_mode.list_mode.index(panel_mode_val["selected_mode"])
        self.wdgt_panel_mode.wheel_mode.radio_button[idx].setChecked(True)

    @Slot()
    def updt_panel_chord(self, panel_chord_val):
        print(panel_chord_val["raw_knob_chord_type"])
        print(panel_chord_val["chord_type"])
        self.wdgt_panel_chord.wheel_comp.knob.setValue(
            (panel_chord_val["raw_knob_chord_type"] / 127)
            * len(self.wdgt_panel_chord.list_chord_comp)
        )
        # idx = self.wdgt_panel_chord.list_chord_comp.index(panel_chord_val["chord_type"])
        # self.wdgt_panel_chord.wheel_comp.radio_button[idx].setChecked(True)

    @Slot()
    def updt_panel_play(self, panel_play_val):
        self.wdgt_panel_chord.wheel_type.knob.setValue(
            (panel_play_val["raw_knob_play_type"] / 127)
            * len(self.wdgt_panel_chord.list_chord_type)
        )
        #  Bad  data architecture correct this
        if panel_play_val["selected_play_type"] == "Single":
            idx = 0
        else:
            idx = self.wdgt_panel_chord.list_chord_type.index(
                panel_play_val["selected_play_type"]["name"]
            )
        self.wdgt_panel_chord.wheel_type.radio_button[idx].setChecked(True)

    @Slot()
    def updt_pad_grid(self, pad_grid_val):
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
        print(list_note)
        if pad_grid_val["key_note"] >= 0:
            key_octave = pad_grid_val["key_degree_octave"] / 12
        else:
            key_octave = int(pad_grid_val["key_degree_octave"] / 12 - 1)
        octave_corrected = base_octave + key_octave
        for idx, velocity in enumerate(pad_grid_val["velocity"]):
            # Root
            if idx == pad_grid_val["key_degree"]:
                self.wdgt_pad_grid.pads[idx]["pad"].put_root_backgrnd(True)
            else:
                self.wdgt_pad_grid.pads[idx]["pad"].put_root_backgrnd(False)
            # Pressed
            if velocity > 0:
                print("test")
                self.wdgt_pad_grid.pads[idx]["pad"].put_pressed_backgrnd(True)
            else:
                self.wdgt_pad_grid.pads[idx]["pad"].put_pressed_backgrnd(False)
            # Note
            self.wdgt_pad_grid.pads[idx]["pad"].button.setText(list_note[idx])
            # if idx < pad_grid_val["key_degree"]:
            #     note_correction = -sum(
            #         pad_grid_val["pad_intervals"][::-1][
            #             idx + 1 : pad_grid_val["key_degree"] + 1
            #         ]
            #     )

            #     # self.wdgt_pad_grid.pads[idx]["pad"].button.setText(
            #     #     map_note[idx_base_note + note_correction]
            #     # )
            #     self.wdgt_pad_grid.pads[idx]["pad"].button.setText("P")
            # elif idx == pad_grid_val["key_degree"]:
            #     self.wdgt_pad_grid.pads[idx]["pad"].button.setText(
            #         map_note[idx_base_note]
            #     )
            # else:
            #     print(f"correction: {pad_grid_val["pad_intervals"]}\n")
            #     note_correction = sum(pad_grid_val["pad_intervals"][: idx + 1])
            #     self.wdgt_pad_grid.pads[idx]["pad"].button.setText(
            #         map_note[(idx_base_note + note_correction) % 12]
            #     )
