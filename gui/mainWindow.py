import sys
import math
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QToolBar,
)
from PySide6.QtCore import QThread, QThreadPool, Slot, QSize, Qt
from PySide6.QtGui import QIcon

from gui.widgetBaseNote import WidgetBaseNote
from gui.widgetKeyNote import WidgetKeyNote
from gui.widgetPanelMode import WidgetPanelMode
from gui.widgetPanelChord import WidgetPanelChord
from gui.widgetPadGrid import WidgetPadGrid
from gui.action_bypass import QActionBypass

from logic.gui.main_logic import MainLogic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Connecting the MidiCOntroller and MidiBridge to the UI
        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        self.logic_worker = MainLogic()

        self.logic_worker.signals.base_note_changed.connect(self.updt_base_note)
        self.logic_worker.signals.key_note_changed.connect(self.updt_key_degree)
        self.logic_worker.signals.panel_mode_changed.connect(self.updt_panel_mode)
        self.logic_worker.signals.panel_chord_comp_changed.connect(
            self.updt_panel_chord_comp
        )
        self.logic_worker.signals.panel_chord_size_changed.connect(
            self.updt_panel_chord_size
        )
        self.logic_worker.signals.pad_grid_changed.connect(self.updt_pad_grid)

        self.threadpool.start(self.logic_worker)

        self.setWindowTitle("8P4K PowerHouse")
        self.setStyleSheet(
            """            
            background-repeat: no-repeat;
            background-position: center;
            border: none; 	
            background-image: url(ressources/gui/png/bckgnd-app.png);
            """
        )

        self.toolbar = QToolBar("Top bar action")
        self.toolbar.setStyleSheet(
            """
            border: none;
            background: #eeeeee;
            """
        )
        # Toolbar
        self.toolbar.setIconSize(QSize(22, 22))
        self.addToolBar(self.toolbar)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.icon_stop = QIcon("../ressources/gui/icons/prohibition.png")
        self.action_bypass = QActionBypass()
        self.action_bypass.signal_toggled.connect(self.logic_worker.toggle_bypass)
        self.toolbar.addAction(self.action_bypass)

        self.wdgt_base_note = WidgetBaseNote(self)
        self.wdgt_key_note = WidgetKeyNote(self)
        self.wdgt_panel_mode = WidgetPanelMode(self)
        self.wdgt_panel_chord = WidgetPanelChord(self)
        self.wdgt_pad_grid = WidgetPadGrid(self)

        self.wdgt_base_note.knob.valueChanged.connect(
            self.logic_worker.gui_change_base_note
        )
        self.wdgt_key_note.knob.valueChanged.connect(
            self.logic_worker.gui_change_key_note
        )
        self.wdgt_panel_mode.wheel_mode.knob.valueChanged.connect(
            self.logic_worker.gui_change_mode
        )
        self.wdgt_panel_chord.wheel_chord_comp.knob.valueChanged.connect(
            self.logic_worker.gui_change_chord_comp
        )
        self.wdgt_panel_chord.wheel_chord_size.knob.valueChanged.connect(
            self.logic_worker.gui_change_chord_size
        )

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
        self.logic_worker.stop()
        event.accept()

    @Slot()
    def updt_base_note(self, state):
        self.wdgt_base_note.knob.blockSignals(True)
        self.wdgt_base_note.update(state["base_note"])
        self.wdgt_base_note.knob.blockSignals(False)
        self.updt_pad_grid(state)

    @Slot()
    def updt_key_degree(self, state):
        self.wdgt_key_note.knob.blockSignals(True)
        self.wdgt_key_note.update(
            {
                "key_degree": state["key_degree"],
                "key_note": state["key_note"],
                "key_degree_octave": state["key_degree_octave"],
                "raw_key_knob": state["raw_key_knob"],
            }
        )
        self.wdgt_key_note.knob.blockSignals(False)
        self.updt_pad_grid(state)

    @Slot()
    def updt_panel_mode(self, state):
        self.wdgt_panel_mode.wheel_mode.knob.blockSignals(True)
        self.wdgt_panel_mode.update(
            {
                "raw_knob_mode": state["raw_knob_mode"],
                "selected_mode": state["selected_mode"],
            }
        )
        self.wdgt_panel_mode.wheel_mode.knob.blockSignals(False)
        self.updt_pad_grid(state)

    @Slot()
    def updt_panel_chord_comp(self, state):
        self.wdgt_panel_chord.wheel_chord_comp.knob.blockSignals(True)
        self.wdgt_panel_chord.update_chord_comp(
            {
                "raw_knob_chord_comp": state["raw_knob_chord_comp"],
                "selected_chord_comp": state["selected_chord_comp"],
            }
        )
        self.wdgt_panel_chord.wheel_chord_comp.knob.blockSignals(False)
        self.updt_pad_grid(state)

    @Slot()
    def updt_panel_chord_size(self, state):
        self.wdgt_panel_chord.wheel_chord_size.knob.blockSignals(True)
        self.wdgt_panel_chord.update_chord_size(
            {
                "raw_knob_chord_size": state["raw_knob_chord_size"],
                "selected_chord_size": state["selected_chord_size"],
            }
        )
        self.wdgt_panel_chord.wheel_chord_size.knob.blockSignals(False)
        self.updt_pad_grid(state)

    @Slot()
    def updt_pad_grid(self, state):
        self.wdgt_pad_grid.update(
            {
                "velocity": state["buffer"]["velocity"],
                "key_degree": state["key_degree"],
                "base_note": state["base_note"],
                "key_note": state["key_note"],
                "pad_intervals": state["pad_intervals"],
                "key_degree_octave": state["key_degree_octave"],
                "pad_notes": state["pad_notes"],
                "pad_octaves": state["pad_octaves"],
                "pad_roots": state["pad_roots"],
                "pad_notes_chords": state["pad_notes_chords"],
            }
        )
