import json

def init_state_app():
    with open("settings.json", "r") as file_settings:
        data_settings = json.load(file_settings)

    with open("data_options_play.json", "r") as file_options_play:
        data_options_play = json.load(file_options_play)

    return ({
        "name_midi_in": data_settings["name_midi_in"],
        "name_midi_out": data_settings["name_midi_out"],
        "base_note_offset": data_settings["base_note_offset"],
        "pot_max_value": data_settings["pot_max_value"] + 1,
        "knob_quadrant_playModes": (pot_max_value/len(data_options_play["knob_values_playModes"])),
        "knob_quadrant_PlayType": (pot_max_value/len(data_options_play["knob_values_playTypes"])),
        "midi_in": None,
        "midi_out": None,
    })

def init_state_controller():
    with open("data_options_play.json", "r") as file_options_play:
        data_options_play = json.load(file_options_play)
    
    return ({
        "mode": data_options_play["knob_values_playModes"][0],
        "base_note": 0,
        "key_note": 0,
        "key_degree": 0,
        "play_type": data_options_play["knob_values_playTypes"][0],
        "state_pad": [0,0,0,0,0,0,0,0],
        "buffer_velocity": [0,0,0,0,0,0,0,0],
        "buffer_note": [[],[],[],[],[],[],[],[]]
    })

def init_options_play():
    with open("data_options_play.json", "r") as file_options_play:
        data_options_play = json.load(file_options_play)

    return ({
        "knob_values_playModes": data_options_play["knob_values_playModes"],
        "knob_values_playTypes": data_options_play["knob_values_playTypes"],
        "playModes_toneProg": data_options_play["playModes_toneProg"],
        "playModes_chordProg": data_options_play["playModes_chordProg"],
        "chord_major": data_options_play["chord_major"],
        "chord_minor": data_options_play["chord_minor"],
        "chord_dom7": data_options_play["chord_dom7"],
        "chord_dim": data_options_play["chord_dim"],
        "tone_progression": data_options_play["tone_progression"],
    })