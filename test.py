import sys
import os
import mido
import rtmidi
from collections import deque

# Mapping
base_note_offset = 36
buffer_note = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]

buffer_velocity = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]
    

state_pad = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]
    

knob_values_playModes = [
    "None",
    "Ionian",
    "Dorian",
    "Phrygian",
    "Lydian",
    "Myxolydian",
    "Aeolian",
    "Locrian",
]


tone_progression = [
    2,
    2,
    1,
    2,
    2,
    2,
    1,
]

chord_major = [0, 4, 7]
chord_minor = [0, 3, 7]
chord_dom7 = [0, 4, 7]
chord_dim = [0, 3, 6]

play_type_chord_prog = {
    "Single": 0,
    "Normal": [chord_major,
                chord_minor,
                chord_minor,
                chord_major,
                chord_dom7,
                chord_minor,
                chord_dim,
                chord_major,
                ],
    "Major": chord_major,
    "Minor": chord_minor,
    "Dom7": chord_dom7,
    "Diminished": chord_dim,
}

playModes_chordProg = {
    "Ionian": [0,1,2,3,4,5,6,7],
    "Dorian": [1,2,3,4,5,6,7,0],
    "Phrygian": [2,3,4,5,6,7,0,1],
    "Lydian": [3,4,5,6,7,0,1,2],
    "Myxolydian": [4,5,6,7,0,1,2,3],
    "Aeolian": [5,6,7,0,1,2,3,4],
    "Locrian": [6,7,0,1,2,3,4,5],
}

playModes_toneProg = {
    "Ionian": [0,1,2,3,4,5,6],
    "Dorian": [1,2,3,4,5,6,0],
    "Phrygian": [2,3,4,5,6,0,1],
    "Lydian": [3,4,5,6,0,1,2],
    "Myxolydian": [4,5,6,0,1,2,3],
    "Aeolian": [5,6,0,1,2,3,4],
    "Locrian": [6,0,1,2,3,4,5],
}

knob_values_playTypes = [
    "Single",
    "Normal",
    "Major",
    "Minor",
    "Dom7",
    "Diminished",
]

note_progression = []

controls_values = 0

pot_max_value = 127 + 1 # +1 is for out of bound error handling

knob_quadrant_playModes = (pot_max_value/len(knob_values_playModes))
knob_quadrant_PlayType = (pot_max_value/len(knob_values_playTypes))

controller_settings = {
    "mode": knob_values_playModes[0],
    "base_note": 0,
    "key_note": 0,
    "key_degree":0,
    "play_type": knob_values_playTypes[0],
}

def check_note(note):
    if note > 127:
        return 127
    elif note < 0:
        return 0
    else:
        return note

def select_base_note(note_value):
    print(f"Base note: {note_value}")
    return note_value

def select_key_note(note_value):
    temp_note = int((note_value-64)/3)
    if controller_settings["mode"] == "None":
        return temp_note
    else:
        octave = int(temp_note/7)*12
        inter_octave = 0

        if temp_note >= 0:
            temp = (temp_note%7)
            for val in playModes_toneProg[controller_settings["mode"]][:temp]:
                inter_octave = inter_octave + tone_progression[val]
        else:
            temp = (temp_note%-7)-1
            for val in playModes_toneProg[controller_settings["mode"]][:temp:-1]:
                inter_octave = inter_octave - tone_progression[val]

        print(f"Note: {note_value}")
        print(f"Octave: {octave}")
        print(f"Inter: {inter_octave}")
        # print(f"Mod: {temp_note%-7}")
        print(f"Key note: {(octave + inter_octave)}")
        return (octave+inter_octave)


def select_playMode(message):
    print(f"Mode: {knob_values_playModes[int(message.value/knob_quadrant_playModes)]}\n")
    return knob_values_playModes[int(message.value/knob_quadrant_playModes)]

def select_playTypes(message):
    print(f"Play type: {knob_values_playTypes[int(message.value/knob_quadrant_PlayType)]}\n")
    return knob_values_playTypes[int(message.value/knob_quadrant_PlayType)]

def pad_pressed(controller_settings, state_pad, buffer_note, buffer_velocity, message):
    id_pad = message.note - base_note_offset
    state_pad[id_pad] = 1
    
    note = check_note(message.note - base_note_offset + controller_settings["base_note"] + controller_settings["key_note"])
    
    buffer_velocity[id_pad] = message.velocity

    note_on(buffer_note, note, message.velocity, id_pad)
    

def pad_released(controller_settings, state_pad, buffer_note, buffer_velocity, message):
    state_pad[message.note - base_note_offset] = 0

    for note in buffer_note[message.note-base_note_offset]:
        note_off(note, buffer_velocity[message.note-base_note_offset], message.note - base_note_offset)   
            
    buffer_note[message.note-base_note_offset] = []
    buffer_velocity = 0

def knob_base_note(controller_settings, buffer_note, state_pad, message):
    any_pad_on = False
    for id_pad, pad_on in enumerate(state_pad):
        if pad_on:
            any_pad_on = True
            temp_note = check_note(buffer_note[id_pad][0] + message.value-64)
            buffer_note[id_pad].append(temp_note)
            note_on(buffer_note, temp_note, buffer_velocity[id_pad], id_pad)

    if not any_pad_on:
        controller_settings["base_note"] = select_base_note(message.value)

def knob_key_note(controller_settings, buffer_note, state_pad, message):
    any_pad_on = False
    for id_pad, pad_on in enumerate(state_pad):
        if pad_on:
            any_pad_on = True
            temp_note = check_note(buffer_note[id_pad][0]+ select_key_note(message.value))
            buffer_note[id_pad].append(temp_note)
            note_on(buffer_note,temp_note, buffer_velocity[id_pad], id_pad)

    if not any_pad_on:
        controller_settings["key_note"] = select_key_note(message.value)

def note_on(buffer_note, note, velocity, id_pad):
    if controller_settings["mode"] == "None" or controller_settings["play_type"] == "Single":
        buffer_note[id_pad].append(note)
        outport.send(mido.Message("note_on", note=note, velocity=velocity))
        print(f"Note on: {note} | Pad: {id_pad + 1}")
    
    elif controller_settings["play_type"] == "Normal":
        for chord_interval in play_type_chord_prog[controller_settings["play_type"]][id_pad]:
            buffer_note[id_pad].append(note + chord_interval)
            outport.send(mido.Message("note_on", note=note + chord_interval, velocity=velocity))

    else:
        for chord_interval in play_type_chord_prog[controller_settings["play_type"]]:
            buffer_note[id_pad].append(note + chord_interval)
            outport.send(mido.Message("note_on", note=note + chord_interval, velocity=velocity))
    
def note_off(note, velocity, id_pad):
    outport.send(mido.Message("note_off", note=note, velocity=velocity))
    print(f"Note off: {note} | Pad: {id_pad + 1}")

#########################
# MIDI START UP SECTION #
#########################

LPD8 = 'LPD8 mk2 0'
virtual_midi_port = "test_virt_midi 2"

midiout = rtmidi.MidiOut()

# List available ports
print("Inputs:", mido.get_input_names())
print("Outputs:", mido.get_output_names())

# Open LPD8 as input
try:
    inport = mido.open_input(LPD8)
    print(f"Successfully opened MIDI input: {LPD8}")

except Exception as e:
    print(f"Failed to open MIDI input: {e}")
    input("Press ENTER to exit...")
    sys.exit(1)

# Create virtual MIDI ouput
if os.name == "posix":
    try:
        midiout.open_virtual_port(virtual_midi_port)
        print(f"Successfully created MIDI output: {virtual_midi_port}")
    
    except Exception as e:
        print(f"Failed to create MIDI output: {e}")
        input("Press ENTER to exit...")
        sys.exit(1)

else:
    print(f"On windows, use loopMIDI to create a virtual MIDI port named : {virtual_midi_port}.\n https://www.tobias-erichsen.de/software/loopmidi.html")

# Connect to the virtual output port
try:
    outport = mido.open_output(virtual_midi_port) 
    print(f"Successfully opened MIDI output: {virtual_midi_port}")
except Exception as e:
    print(f"Failed to open MIDI output: {e}")
    input("Press ENTER to exit...")
    sys.exit(1)


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