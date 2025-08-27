from init_midi import init_midi_in, init_midi_out
from init_software import init_state_app, init_state_controller, init_options_play

from logic import knob_base_note, reset_key_degree, select_playMode, knob_key_note, select_playTypes, pad_pressed, pad_released

state_app = init_state_app()

state_controller = init_state_controller()

data_options_play = init_options_play()

state_app["midi_in"] = init_midi_in(name_midi_in)
state_app["midi_out"] = init_midi_out(name_midi_out)

##########################
# MIDI INTERFACE SECTION #
##########################
print("Routing MIDI from LPD8 to virtual port...")
try:
    for msg in midi_in:
        # Control change or knob change
        if msg.type == "control_change":
            # Knob 1: select_base_note  
            if msg.control == 70:
                knob_base_note(controller_settings, msg)
                
            # Knob 4: select_playMode
            elif msg.control == 73:
                controller_settings["mode"] = select_playMode(knob_values_playModes,
                                                            knob_quadrant_playModes,
                                                            msg)
                controller_settings["key_degree"] = reset_key_degree()

            # Knob 5: select_keyNote
            elif msg.control == 74:
                knob_key_note(controller_settings,
                            buffer_note,
                            state_pad,
                            msg)

            # Knob 8: select_playType
            elif msg.control == 77:
                controller_settings["play_type"] = select_playTypes(knob_values_playTypes,
                                                                    knob_quadrant_PlayType,
                                                                    msg) 
        
        # Note pressed
        elif msg.type == 'note_on':
            controller_settings = pad_pressed(controller_settings, msg)

        elif msg.type == 'note_off':
            controller_settings = pad_released(controller_settings, msg)

        # Unkown command/Error
        else:
            # Forward all other messages unchanged
            midi_out.send(msg)
        # print(f"NOTE:", {controller_settings["base_note"] + controller_settings["key_note"]})
except KeyboardInterrupt:
    print("Stopped.")
finally:
    midi_in.close()
    midi_out.close()
    print("Shutdown.")
    input("Press ENTER to exit...")