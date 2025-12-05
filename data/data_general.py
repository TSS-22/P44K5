from PySide6.QtCore import Qt

chords = {
    "major": [0, 4, 7, 9, 11, 14, 17, 21],
    "minor": [0, 3, 7, 8, 10, 14, 17, 20],
    "dominant": [0, 4, 7, 9, 10, 14, 17, 21],
    "diminished": [0, 3, 6, 9, 9, 14, 17, 21],
    "augmented": [0, 4, 8, 9, 11, 14, 17, 21],
    "sus2": [0, 2, 7, 9, 10, 14, 17, 21],
    "sus4": [0, 5, 7, 9, 10, 14, 17, 21],
}

knob_values_chord_comp = [
    {"name": "Normal", "chord": [0]},
    {"name": "Major", "chord": chords["major"]},
    {"name": "Minor", "chord": chords["minor"]},
    {"name": "Dom", "chord": chords["dominant"]},
    {"name": "Dim", "chord": chords["diminished"]},
    {"name": "Aug", "chord": chords["augmented"]},
    {"name": "Sus2", "chord": chords["sus2"]},
    {"name": "Sus4", "chord": chords["sus4"]},
]

hc_chord_comp_name = [item["name"] for item in knob_values_chord_comp]

tone_progression = [2, 2, 1, 2, 2, 2, 1]

tone_prog_mode = {
    "Ionian": [0, 1, 2, 3, 4, 5, 6],
    "Dorian": [1, 2, 3, 4, 5, 6, 0],
    "Phrygian": [2, 3, 4, 5, 6, 0, 1],
    "Lydian": [3, 4, 5, 6, 0, 1, 2],
    "Myxolydian": [4, 5, 6, 0, 1, 2, 3],
    "Aeolian": [5, 6, 0, 1, 2, 3, 4],
    "Locrian": [6, 0, 1, 2, 3, 4, 5],
}

chord_prog_mode = {
    "Ionian": [0, 1, 2, 3, 4, 5, 6, 7],
    "Dorian": [1, 2, 3, 4, 5, 6, 7, 0],
    "Phrygian": [2, 3, 4, 5, 6, 7, 0, 1],
    "Lydian": [3, 4, 5, 6, 7, 0, 1, 2],
    "Myxolydian": [4, 5, 6, 7, 0, 1, 2, 3],
    "Aeolian": [5, 6, 7, 0, 1, 2, 3, 4],
    "Locrian": [6, 7, 0, 1, 2, 3, 4, 5],
}

knob_values_chord_size = [
    {"name": "Single", "comp": [0]},
    {"name": "5", "comp": [0, 2]},
    {"name": "Triad", "comp": [0, 1, 2]},
    {"name": "6", "comp": [0, 1, 2, 3]},
    {"name": "7", "comp": [0, 1, 2, 4]},
    {"name": "9", "comp": [0, 1, 2, 4, 5]},
    {"name": "11", "comp": [0, 1, 2, 4, 5, 6]},
    {"name": "13", "comp": [0, 1, 2, 4, 5, 6, 7]},
]
hc_chord_size_name = [item["name"] for item in knob_values_chord_size]

ionian_chord_prog = [
    "major",
    "minor",
    "minor",
    "major",
    "dominant",
    "minor",
    "diminished",
    "major",
]

hc_chromatic_scale = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
]

hc_len_chromatic_scale = 12

hc_offset_midi_octave = -2

hc_knob_mode_multiplier = 15.875
hc_knob_chord_comp_multiplier = 21.166667
hc_knob_chord_size_multiplier = 18.142857142

hc_list_note_startup = [
    "C" + " " + str(hc_offset_midi_octave),
    "C#" + " " + str(hc_offset_midi_octave),
    "D" + " " + str(hc_offset_midi_octave),
    "D#" + " " + str(hc_offset_midi_octave),
    "E" + " " + str(hc_offset_midi_octave),
    "F" + " " + str(hc_offset_midi_octave),
    "F#" + " " + str(hc_offset_midi_octave),
    "G" + " " + str(hc_offset_midi_octave),
]

hc_list_mode = [
    "Chromatic",
    "Ionian",
    "Dorian",
    "Phrygian",
    "Lydian",
    "Myxolydian",
    "Aeolian",
    "Locrian",
]

hc_name_chord_prog = {
    "Ionian": [
        "Maj",
        "Min",
        "Min",
        "Maj",
        "Dom",
        "Min",
        "Dim",
    ],
    "Dorian": [
        "Min",
        "Min",
        "Maj",
        "Dom",
        "Min",
        "Dim",
        "Maj",
    ],
    "Phrygian": [
        "Min",
        "Maj",
        "Dom",
        "Min",
        "Dim",
        "Maj",
        "Min",
    ],
    "Lydian": [
        "Maj",
        "Dom",
        "Min",
        "Dim",
        "Maj",
        "Min",
        "Min",
    ],
    "Myxolydian": [
        "Dom",
        "Min",
        "Dim",
        "Maj",
        "Min",
        "Min",
        "Maj",
    ],
    "Aeolian": [
        "Min",
        "Dim",
        "Maj",
        "Min",
        "Min",
        "Maj",
        "Dom",
    ],
    "Locrian": [
        "Dim",
        "Maj",
        "Min",
        "Min",
        "Maj",
        "Dom",
        "Min",
    ],
}

hc_dialog_select_device = "Select a device"

hc_name_midi_out = "P44D5_virt"

hc_file_filter = "Midi controller configuration files (*.cnfmidi);;All Files (*);;"

hc_file_extension = "cnfmidi"

hc_diag_knob_setup_txt = """
Move the knob you want to associate with
"""

hc_pad_mode_note = "note"
hc_pad_mode_cc = "control_change"

hc_shortcut_pads = [
    Qt.Key_S,
    Qt.Key_D,
    Qt.Key_F,
    Qt.Key_G,
    Qt.Key_H,
    Qt.Key_J,
    Qt.Key_K,
    Qt.Key_L,
]

hc_event_type_shortcut_override = 51
hc_event_type_key_release = 7

hc_path_default_config = "./configurations/default.cnfmidi"
hc_path_user_settings = "./user_settings.json"
