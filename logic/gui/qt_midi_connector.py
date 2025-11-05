from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from logic.core.controller.midi_controller import MidiController
from logic.core.bridge.midi_bridge import MidiBridge
from logic.gui.qt_midi_connector_signal import QtMidiConnectorSignal


class QtMidiConnector(QRunnable):

    def __init__(self):
        super().__init__()
        self.signals = QtMidiConnectorSignal()
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
                    self.signals.midi_messages.emit(midi_controller_output.to_dict())
                    # self.signals.midi_messages.emit(QObject())
            except KeyboardInterrupt:
                print("Stopped.")

        self.midi_bridge.stop()
        self.signals.finished.emit()

    @Slot()
    def stop(self):
        self._is_running = False
        self.signals.stopped.emit()

    def process_messages(self, messages):
        # Process the MidiBridgeMessageOut into a Signal that will send the new states for the widgets
        return
