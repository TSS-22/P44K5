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

from gui.widgetBaseNote import WidgetBaseNote
from gui.widgetKeyNote import WidgetKeyNote
from gui.widgetPanelMode import WidgetPanelMode
from gui.widgetPanelChord import WidgetPanelChord
from gui.widgetPadGrid import WidgetPadGrid

from logic.gui.main_logic import MainLogic

from logic.gui.map_note import map_note


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
        self.logic_worker.signals.panel_chord_changed.connect(self.updt_panel_chord)
        self.logic_worker.signals.panel_play_changed.connect(self.updt_panel_play)
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
        self.logic_worker.stop()
        event.accept()

    @Slot()
    def updt_base_note(self, base_note_val):
        self.wdgt_base_note.update(base_note_val)

    @Slot()
    def updt_key_degree(self, key_deg_val):
        self.wdgt_key_note.update(key_deg_val)

    @Slot()
    def updt_panel_mode(self, panel_mode_val):
        self.wdgt_panel_mode.update(panel_mode_val)

    @Slot()
    def updt_panel_chord(self, panel_chord_val):
        self.wdgt_panel_chord.update_chord(panel_chord_val)

    @Slot()
    def updt_panel_play(self, panel_play_val):
        self.wdgt_panel_chord.update_play(panel_play_val)

    @Slot()
    def updt_pad_grid(self, pad_grid_val):
        self.wdgt_pad_grid.update(pad_grid_val)
