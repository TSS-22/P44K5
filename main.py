from init_midi import init_midi_in, init_midi_out
from midi_controller import MidiController
from midi_bridge import MidiBridge

midi_controller = MidiController()

midi_bridge = MidiBridge()

##########################
# MIDI INTERFACE SECTION #
##########################
print(f"Routing MIDI from {midi_bridge.get_selected_input().name} to virtual port {midi_bridge.get_selected_ouput().name}...")
try:
    for msg in midi_bridge.input:
       midi_bridge.bridge_out(midi_controller.receive_message(msg))

except KeyboardInterrupt:
        print("Stopped.")
finally:
        midi_bridge.stop()