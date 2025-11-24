chord_major = [0, 4, 7, 9, 11, 14, 17, 21]
chord_minor = [0, 3, 7, 8, 10, 14, 17, 20]
chord_dom = [0, 4, 7, 7, 10, 14, 17, 21]
chord_dim = [0, 3, 6, 9, 9, 14, 17, 21]

chords = {
    "major": [0, 4, 7, 9, 11, 14, 17, 21],
    "minor": [0, 3, 7, 8, 10, 14, 17, 20],
    "dominant": [0, 4, 7, 7, 10, 14, 17, 21],
    "diminished": [0, 3, 6, 9, 9, 14, 17, 21],
}

knob_values_chord_comp = [
    {"name": "Single", "chord": [0]},
    {"name": "Normal", "chord": [0]},
    {"name": "Major", "chord": chords["major"]},
    {"name": "Minor", "chord": chords["minor"]},
    {"name": "Dom", "chord": chords["dominant"]},
    {"name": "Dim", "chord": chords["diminished"]},
]

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
    {"name": "5", "comp": [0, 2]},
    {"name": "X", "comp": [0, 1, 2]},
    {"name": "6", "comp": [0, 1, 2, 3]},
    {"name": "7", "comp": [0, 1, 2, 4]},
    {"name": "9", "comp": [0, 1, 2, 4, 5]},
    {"name": "11", "comp": [0, 1, 2, 4, 5, 6]},
    {"name": "13", "comp": [0, 1, 2, 4, 5, 6, 7]},
]

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

hc_offset_midi_octave = -3

hc_knob_mode_multiplier = 15.875
hc_knob_chord_comp_multiplier = 21.166667
hc_knob_chord_size_multiplier = 18.142857142

hc_list_note_startup = [
    "C -3",
    "C# -3",
    "D -3",
    "D# -3",
    "E -3",
    "F -3",
    "F# -3",
    "G -3",
]

hc_list_mode = [
    "None",
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
