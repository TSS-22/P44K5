#########################
# MIDI START UP SECTION #
#########################
import sys
import os
import rtmidi
import mido

def init_midi_in(midi_input):
    midiout = rtmidi.MidiOut()

    # List available ports
    print("Inputs:", mido.get_input_names())
    print("Outputs:", mido.get_output_names())

    # Open midi_input
    try:
        midi_in = mido.open_input(midi_input)
        print(f"Successfully opened MIDI input: {midi_input}")
        return midi_in

    except Exception as e:
        print(f"Failed to open MIDI input: {e}")
        input("Press ENTER to exit...")
        sys.exit(1)

def init_midi_out(midi_output):
    # Create virtual MIDI ouput
    if os.name == "posix":
        try:
            midiout.open_virtual_port(midi_output)
            print(f"Successfully created MIDI output: {midi_output}")
        
        except Exception as e:
            print(f"Failed to create MIDI output: {e}")
            input("Press ENTER to exit...")
            sys.exit(1)

    else:
        print(f"On windows, use loopMIDI to create a virtual MIDI port named : {midi_output}.\n https://www.tobias-erichsen.de/software/loopmidi.html")

    # Connect to the virtual output port
    try:
        midi_out = mido.open_output(midi_output) 
        print(f"Successfully opened MIDI output: {midi_output}")
        return midi_out

    except Exception as e:
        print(f"Failed to open MIDI output: {e}")
        input("Press ENTER to exit...")
        sys.exit(1)