from PySide6.QtCore import QObject, Signal, Slot
from source.midi_bridge_message_out import MidiBridgeMessageOut


class MainLogic(QObject):

    @Slot()
    def handle_midi(self, list_midi_msg):
        print("received messages")

    def do_work(self):
        # Simulate logic
        new_state = "Logic updated!"
        self.state_changed.emit(new_state)  # Notify UI
