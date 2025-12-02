import json
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QFileDialog,
)
from PySide6.QtCore import QThread, QThreadPool, Slot, QSize, Qt
from PySide6.QtGui import QIcon

from gui.main_window.widgetBaseNote import WidgetBaseNote
from gui.main_window.widgetKeyNote import WidgetKeyNote
from gui.main_window.widgetPanelMode import WidgetPanelMode
from gui.main_window.widgetPanelChord import WidgetPanelChord
from gui.main_window.widgetPadGrid import WidgetPadGrid
from gui.main_bars.main_tool_bar import MainToolBar
from gui.main_bars.main_status_bar import MainStatusBar

from gui.configs.ConfigNewWindow import ConfigNewWindow

from logic.gui.main_logic import MainLogic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        with open(
            "./data/user_settings.json", "r", encoding="UTF-8"
        ) as file_settings_user:
            self.user_settings = json.load(file_settings_user)

        # Connecting the MidiCOntroller and MidiBridge to the UI
        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        self.logic_worker = MainLogic()
        self.setFixedSize(1200, 760)
        # Window property
        self.setWindowTitle("8P4K PowerHouse")
        self.setStyleSheet(
            """            
            background-repeat: no-repeat;
            background-position: center;
            border: none; 	
            background-image: url(ressources/gui/png/bckgnd-app.png);
            """
        )

        self.status_bar = MainStatusBar()
        self.setStatusBar(self.status_bar)
        self.tool_bar = MainToolBar()
        self.addToolBar(self.tool_bar)

        self.wdgt_base_note = WidgetBaseNote(self)
        self.wdgt_key_note = WidgetKeyNote(self)
        self.wdgt_panel_mode = WidgetPanelMode(self)
        self.wdgt_panel_chord = WidgetPanelChord(self)
        self.wdgt_pad_grid = WidgetPadGrid(self)

        # QAction driven changes
        self.tool_bar.action_refresh.signal_clicked.connect(self.refresh_midi_input)
        self.tool_bar.action_new.signal_clicked.connect(self.open_new_config_window)
        self.tool_bar.cmb_midi_controller.currentTextChanged.connect(
            self.on_choice_controller_changed
        )
        self.tool_bar.action_load.sig_load_config.connect(self.on_load_midi_config)

        # User GUI driven changes signal connections
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
        self.wdgt_panel_mode.wheel_mode.radio_button_group.idClicked.connect(
            self.logic_worker.gui_change_mode
        )
        self.wdgt_panel_chord.wheel_chord_comp.radio_button_group.idClicked.connect(
            self.logic_worker.gui_change_chord_comp
        )
        self.wdgt_panel_chord.wheel_chord_size.radio_button_group.idClicked.connect(
            self.logic_worker.gui_change_chord_size
        )
        self.wdgt_pad_grid.sig_pad_pressed.connect(self.logic_worker.gui_pad_pressed)
        self.wdgt_pad_grid.sig_pad_released.connect(self.logic_worker.gui_pad_released)

        # Physically driven change
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

        self.config_new_window = ConfigNewWindow(parent=self)

        self._init_GUI()

    def closeEvent(self, event):
        # Ask the worker to stop
        self.logic_worker.stop()
        self.config_new_window.close()
        event.accept()

    def _init_GUI(self):
        state = self.logic_worker.midi_controller.get_state().to_dict()
        # state = state
        self.updt_base_note(state)
        self.updt_key_degree(state)
        self.updt_panel_mode(state)
        self.updt_panel_chord_comp(state)
        self.updt_panel_chord_size(state)
        self.updt_pad_grid(state)
        self.refresh_midi_input()
        if (
            self.tool_bar.cmb_midi_controller.findText(
                self.user_settings["last_connected_midi"],
                flags=Qt.MatchFlag.MatchContains,
            )
            > -1
        ):
            self.tool_bar.cmb_midi_controller.setCurrentIndex(
                self.tool_bar.cmb_midi_controller.findText(
                    self.user_settings["last_connected_midi"],
                    flags=Qt.MatchFlag.MatchContains,
                )
            )

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
                "idx_mode": state["idx_mode"],
                "selected_mode": state["selected_mode"],
            }
        )
        self.wdgt_panel_mode.wheel_mode.knob.blockSignals(False)
        self.updt_key_degree(state)
        self.updt_pad_grid(state)
        self.function_activation(state)

    @Slot()
    def updt_panel_chord_comp(self, state):
        self.wdgt_panel_chord.wheel_chord_comp.knob.blockSignals(True)
        self.wdgt_panel_chord.update_chord_comp(
            {
                "idx_chord_comp": state["idx_chord_comp"],
                "selected_chord_comp": state["selected_chord_comp"],
            }
        )
        self.wdgt_panel_chord.wheel_chord_comp.knob.blockSignals(False)
        self.function_activation(state)
        self.updt_pad_grid(state)

    @Slot()
    def updt_panel_chord_size(self, state):
        self.wdgt_panel_chord.wheel_chord_size.knob.blockSignals(True)
        self.wdgt_panel_chord.update_chord_size(
            {
                "idx_chord_size": state["idx_chord_size"],
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
                "name_chords": state["name_chords"],
            }
        )

    def function_activation(self, state):
        if (state["idx_mode"] == 0) and (state["idx_chord_comp"] == 0):
            self.wdgt_panel_chord.wheel_chord_size.setEnabled(False)
        else:
            self.wdgt_panel_chord.wheel_chord_size.setEnabled(True)

        if state["idx_mode"] == 0:
            self.wdgt_key_note.knob.setEnabled(False)
        else:
            self.wdgt_key_note.knob.setEnabled(True)

    @Slot()
    def refresh_midi_input(self):
        self.tool_bar.cmb_midi_controller.refresh(self.logic_worker.get_midi_input())

    @Slot()
    def refresh_midi_input_new_config_window(self):
        self.config_new_window.cmb_midi_controller.refresh(
            self.logic_worker.get_midi_input()
        )

    @Slot()
    def on_choice_controller_changed(self, controller_name):
        self.logic_worker.midi_bridge.disconnect()
        self.logic_worker.midi_bridge.connect_to_controller(controller_name)
        self.user_settings["last_connected_midi"] = controller_name
        self.logic_worker.save_user_settings(self.user_settings)

    @Slot()
    def open_new_config_window(self):
        self.config_new_window.show()

    @Slot()
    def on_load_midi_config(self, file_path):
        config_loaded = self.logic_worker.load_micro_controller_settings(
            file_path, self.user_settings
        )
        if config_loaded:
            basename = os.path.basename(file_path)
            name = os.path.splitext(basename)[0]
            self.status_bar.new_config_loaded(name)
        else:
            pass
