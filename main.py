from init_midi import init_midi_in, init_midi_out
from midi_controller import MidiController

midi_controller = MidiController()

midi_bridge = MidiBridge()

# Do it in a class with a send and receive value for them, woudln't that works better ?
state_controller["midi_in"] = init_midi_in(state_app["name_midi_in"])
state_controller["midi_out"] = init_midi_out(state_app["name_midi_out"])

##########################
# MIDI INTERFACE SECTION #
##########################
print("Routing MIDI from LPD8 to virtual port...")
try:
    for msg in state_app["midi_in"]:
        # Control change or knob change
        if msg.type == "control_change":
            # Knob 1: select_base_note  
            if msg.control == 70:
                knob_base_note(state_controller, msg)
                
            # Knob 4: select_playMode
            elif msg.control == 73:
                state_controller["mode"] = select_playMode(knob_values_playModes,
                                                            knob_quadrant_playModes,
                                                            msg)
                state_controller["key_degree"] = reset_key_degree()

            # Knob 5: select_keyNote
            elif msg.control == 74:
                knob_key_note(state_controller,
                            buffer_note,
                            state_pad,
                            msg)

            # Knob 8: select_playType
            elif msg.control == 77:
                state_controller["play_type"] = select_playTypes(knob_values_playTypes,
                                                                    knob_quadrant_PlayType,
                                                                    msg) 
        
        # Note pressed
        elif msg.type == 'note_on':
            pad_pressed(state_controller, state_app["base_note_offset"], msg)

        elif msg.type == 'note_off':
            pad_released(state_controller, state_app["base_note_offset"], msg)

        # Unkown command/Error
        else:
            # Forward all other messages unchanged
            state_app["midi_out"].send(msg)
        # print(f"NOTE:", {state_controller["base_note"] + state_controller["key_note"]})
except KeyboardInterrupt:
    print("Stopped.")
finally:
    state_app["midi_in"].close()
    state_app["midi_out"].close()
    print("Shutdown.")
    input("Press ENTER to exit...")