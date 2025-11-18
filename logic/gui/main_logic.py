from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from logic.core.controller.midi_controller import MidiController
from logic.core.bridge.midi_bridge import MidiBridge
from logic.gui.main_logic_signals import MainLogicSignals
from logic.gui.gui_input import GuiInput
from logic.core.controller.controller_message_flag import ControllerMessageFlag


class MainLogic(QRunnable):

    def __init__(self):
        super().__init__()
        self.signals = MainLogicSignals()
        self.midi_controller = MidiController()
        self.midi_bridge = MidiBridge()
        self._is_running = False

    def run(self):
        print("starting thread")
        self._is_running = True
        while self._is_running:
            try:
                for midi_msg in self.midi_bridge.input.iter_pending():
                    midi_controller_output = self.midi_bridge.bridge_out(
                        self.midi_controller.receive_message(midi_msg)
                    )
                    self.handle_midi(midi_controller_output.to_dict())

            except KeyboardInterrupt:
                print("Stopped.")

        self.midi_bridge.stop()
        self.signals.finished.emit()

    @Slot()
    def stop(self):
        self._is_running = False
        self.signals.stopped.emit()

    def handle_midi(self, midi_controller_output):
        if midi_controller_output["flag"] == ControllerMessageFlag.BASE_NOTE_CHANGED:
            self.signals.base_note_changed.emit(midi_controller_output["state"])
        elif midi_controller_output["flag"] == ControllerMessageFlag.KEY_NOTE_CHANGED:
            self.signals.key_note_changed.emit(midi_controller_output["state"])
        elif midi_controller_output["flag"] == ControllerMessageFlag.MODE_CHANGED:
            self.signals.panel_mode_changed.emit(midi_controller_output["state"])
        elif midi_controller_output["flag"] == ControllerMessageFlag.CHORD_COMP_CHANGED:
            self.signals.panel_chord_comp_changed.emit(midi_controller_output["state"])
        elif midi_controller_output["flag"] == ControllerMessageFlag.CHORD_SIZE_CHANGED:
            self.signals.panel_chord_size_changed.emit(midi_controller_output["state"])
        elif (
            midi_controller_output["flag"] == ControllerMessageFlag.PAD_PRESSED
            or ControllerMessageFlag.PAD_RELEASED
        ):
            self.signals.pad_grid_changed.emit(midi_controller_output["state"])

    @Slot()
    def toggle_bypass(self):
        self.midi_controller.toggle_bypass()

    @Slot()
    def gui_change_base_note(self, base_note):
        self.midi_controller.knob_base_note(GuiInput(base_note))
        self.signals.base_note_changed.emit(self.midi_controller.state.to_dict())

    @Slot()
    def gui_change_key_note(self, key_note):
        self.midi_controller.knob_key_note(GuiInput(key_note))
        self.signals.key_note_changed.emit(self.midi_controller.state.to_dict())

    @Slot()
    def gui_change_mode(self, knob_value):
        self.midi_controller.state.raw_knob_mode = knob_value * 15.875  # HARDCODED
        self.midi_controller.select_mode(knob_value)
        self.signals.panel_mode_changed.emit(self.midi_controller.state.to_dict())

    @Slot()
    def gui_change_chord_comp(self, knob_value):
        print(f"chord comp knob: {knob_value}")
        self.midi_controller.state.raw_knob_chord_comp = (
            knob_value * 21.16666667
        )  # HARDCODED
        self.midi_controller.select_chord_comp(knob_value)
        self.signals.panel_chord_comp_changed.emit(self.midi_controller.state.to_dict())

    @Slot()
    def gui_change_chord_size(self, knob_value):
        print(f"chord size knob: {knob_value}")
        self.midi_controller.state.raw_knob_chord_size = (
            knob_value * 18.142857142
        )  # HARDCODED
        self.midi_controller.select_chord_size(knob_value)
        self.signals.panel_chord_size_changed.emit(self.midi_controller.state.to_dict())
