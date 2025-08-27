# 
def knob_base_note(controller_settings, message):
    any_pad_on = False
    for id_pad, pad_on in enumerate(controller_settings["state_pad"]):
        if pad_on:
            any_pad_on = True
            temp_note = check_note(controller_settings["buffer_note"][id_pad][0] + message.value-64)
            note_on(controller_settings, temp_note, id_pad)

    if not any_pad_on:
        controller_settings["base_note"] = select_base_note(message.value)

# Check if the note doesn't go below or above the maximum MIDI protocol values
# Used to prevent error when computing notes as they can go below and above
# those values
# min: 0
# max: 127
def check_note(note):
    if note > 127:
        return 127
    elif note < 0:
        return 0
    else:
        return note

# Reset the key_degree value from controller settings.
# Used when changing the mode
def reset_key_degree():
    print("Key degree: 0")
    return 0

# Select the note that serve as base for the rest.
def select_base_note(note_value):
    print(f"Base note: {note_value}")
    return note_value

def compute_pad_intervals(key_degree, tone_progression):
    tone_intervals = [-x for x in tone_progression[:key_degree]] + [0] + tone_progression[key_degree:]
    return tone_intervals

def note_off(note, velocity, id_pad):
    outport.send(mido.Message("note_off", note=note, velocity=velocity))
    print(f"Note off: {note} | Pad: {id_pad + 1}")

# Used to select the modes.
# Refer to "./data.py/knob_values_playModes" for more details about the possible values
def select_playMode(knob_values_playModes, knob_quadrant_playModes, message):
    print(f"Mode: {knob_values_playModes[int(message.value/knob_quadrant_playModes)]}\n")
    return knob_values_playModes[int(message.value/knob_quadrant_playModes)]

# Used to select the type of play, either chord like or single note.
# Refer to "./data.py/knob_values_playTypes" for more details about the possible values
def select_playTypes(knob_values_playTypes, knob_quadrant_PlayType, message):
    print(f"Play type: {knob_values_playTypes[int(message.value/knob_quadrant_PlayType)]}\n")
    return knob_values_playTypes[int(message.value/knob_quadrant_PlayType)]

#########################

def note_on(buffer_note, note, velocity, id_pad, pad_intervals, degree):
    
    if controller_settings["play_type"] == "Single":
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
    
# When using no mode, it is equivalent to select_base_node
# When using modes play, the mode stick to the base note to 
# determine the key we are in, but you can use the select_key_note
# to chose the note the pad will play from within the key.
# This allow for play within the key without loosing it.
# Easier than changing the mode and base_note and doing the mental acrobat.
# Tied to the key_note change, as it gives us an indication of 
# where we are in the key. This allow later to compute the adequat intervals
# to play the right notes. This is again done to simplify the process 
# of playing around in the same key.
def select_key_note(controller_settings, playModes_toneProg, tone_progression, note_value):
    temp_note = int((note_value-64)/3)
    degree = 0

    if controller_settings["mode"] == "None":
        return temp_note
        controller_settings["key_degree"] = 0

    else:
        octave = int(temp_note/7)*12
        inter_octave = 0

        if temp_note >= 0:
            temp = (temp_note%7)
            print(controller_settings["mode"])
            for val in playModes_toneProg[controller_settings["mode"]][:temp]:
                inter_octave = inter_octave + tone_progression[val]
                degree = degree + 1

        else:
            temp = (temp_note%-7)-1
            for val in playModes_toneProg[controller_settings["mode"]][:temp:-1]:
                inter_octave = inter_octave - tone_progression[val]
                degree = degree + 1

        print(f"Key note: {(octave + inter_octave)}")
        print(f"Key degree: {degree}")
        controller_settings["key_degree"] = degree
        return (octave+inter_octave)


############################
# PHYSICAL CONTROL SECTION #
############################

# Pad pressed
def pad_pressed(controller_settings, state_pad, buffer_note, buffer_velocity, message):
    id_pad = message.note - base_note_offset
    state_pad[id_pad] = 1
    
    note = check_note(message.note - base_note_offset + controller_settings["base_note"] + controller_settings["key_note"])
    
    buffer_velocity[id_pad] = message.velocity

    note_on(buffer_note, note, message.velocity, id_pad, [], controller_settings["key_degree"])

# Pad released
def pad_released(controller_settings, state_pad, buffer_note, buffer_velocity, message):
    state_pad[message.note - base_note_offset] = 0

    for note in buffer_note[message.note-base_note_offset]:
        note_off(note, buffer_velocity[message.note-base_note_offset], message.note - base_note_offset)   
            
    buffer_note[message.note-base_note_offset] = []
    buffer_velocity = 0

#
def knob_key_note(controller_settings, buffer_note, state_pad, message):
    any_pad_on = False
    for id_pad, pad_on in enumerate(state_pad):
        if pad_on:
            any_pad_on = True
            array_pad_interval = compute_pad_intervals(controller_settings["key_degree"])
            # WARNING I DON'T THINK THAT IS GOING TO WORKS ONCE THE KEY_NOTE IS CHANGED
            temp_note = check_note(buffer_note[id_pad][0]+ select_key_note(message.value))
            note_on(buffer_note, temp_note, buffer_velocity[id_pad], id_pad, controller_settings["key_degree"])

    if not any_pad_on:
        controller_settings["key_note"] = select_key_note(message.value)
        controller_settings["key_degree"] = select_key_degree(message.value)


