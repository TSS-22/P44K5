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

