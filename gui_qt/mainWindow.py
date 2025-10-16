import sys

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
        print(base_note_val)
        self.wdgt_base_note.knob.setValue(base_note_val)
        note = map_note[base_note_val % 12]
        octave = int(base_note_val / 12) - 3
        self.wdgt_base_note.lbl_note.setText(f"{note} {octave}")
