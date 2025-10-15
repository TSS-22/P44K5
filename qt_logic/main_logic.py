from PySide6.QtCore import QObject, Signal, Slot
from source.midi_bridge_message_out import MidiBridgeMessageOut
from qt_logic.main_logic_signal import MainLogicSignal


class MainLogic(QObject):
    id_knob_base_note = 70  # HARDCODED
    signal = MainLogicSignal()

    @Slot()
    def handle_midi(self, midi_controller_state):
        pass

    def do_work(self):
        # Simulate logic
        new_state = "Logic updated!"
        self.state_changed.emit(new_state)  # Notify UI
