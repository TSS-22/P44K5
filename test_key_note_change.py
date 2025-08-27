from midi_startup import init_midi_in, init_midi_out
from data import *

midi_in = init_midi_in(name_midi_in)
midi_out =init_midi_out(name_midi_out)

##########################
# MIDI INTERFACE SECTION #
##########################
print("Routing MIDI from LPD8 to virtual port...")
try:
    for msg in inport:
        # Control change or knob change
        if msg.type == "control_change":
            # Knob 1: select_base_note  
            if msg.control == 70:
                knob_base_note(controller_settings, buffer_note, state_pad, msg)
                
            # Knob 4: select_playMode
            elif msg.control == 73:
                controller_settings["mode"] = select_playMode(msg)
                controller_settings["key_degree"] = reset_key_degree()

            # Knob 5: select_keyNote
            elif msg.control == 74:
                knob_key_note(controller_settings, buffer_note, state_pad, msg)

            # Knob 8: select_playType
            elif msg.control == 77:
                controller_settings["play_type"] = select_playTypes(msg) 
        
        # Note pressed
        elif msg.type == 'note_on':
            pad_pressed(controller_settings, state_pad, buffer_note, buffer_velocity, msg)

        elif msg.type == 'note_off':
            pad_released(controller_settings, state_pad, buffer_note, buffer_velocity, msg)

        # Unkown command/Error
        else:
            # Forward all other messages unchanged
            outport.send(msg)
        # print(f"NOTE:", {controller_settings["base_note"] + controller_settings["key_note"]})
except KeyboardInterrupt:
    print("Stopped.")
finally:
    inport.close()
    outport.close()
    print("Shutdown.")
    input("Press ENTER to exit...")