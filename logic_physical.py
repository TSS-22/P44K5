############################
# PHYSICAL CONTROL SECTION #
############################
from settings import *

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
def knob_base_note(controller_settings, buffer_note, state_pad, message):
    any_pad_on = False
    for id_pad, pad_on in enumerate(state_pad):
        if pad_on:
            any_pad_on = True
            temp_note = check_note(buffer_note[id_pad][0] + message.value-64)
            note_on(buffer_note, temp_note, buffer_velocity[id_pad], id_pad)

    if not any_pad_on:
        controller_settings["base_note"] = select_base_note(message.value)

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