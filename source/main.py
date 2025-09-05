from midi_controller import MidiController
from midi_bridge import MidiBridge
from nicegui import ui


midi_controller = MidiController()

midi_bridge = MidiBridge()

#################
# UI DEFINITION #
#################
ui.label("Hello NiceGUI!")


midi_bridge.start(midi_controller)
