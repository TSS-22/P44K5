from logic.core.controller.midi_controller_buffer import MidiControllerBuffer


class MidiControllerState:
    def __init__(
        self,
        selected_mode=None,
        selected_play_type=None,
        selected_chord_type=None,
        selected_chord_comp=None,
    ):
        self.bypass = False
        self.buffer = MidiControllerBuffer()
        self.base_note = 0
        self.key_note = 0
        self.key_degree = 0
        self.key_degree_octave = 0
        self.selected_mode = selected_mode
        self.selected_play_type = selected_play_type
        self.selected_chord_comp = selected_chord_comp
        self.chord_type = selected_chord_type
        self.raw_key_knob = 0
        self.raw_knob_mode = 0
        self.raw_knob_play_type = 0
        self.raw_knob_chord_type = 0
        self.pad_intervals = []
        self.pad_values = []
        self.pad_notes = [
            "C -3",
            "C# -3",
            "D -3",
            "D# -3",
            "E -3",
            "F -3",
            "F# -3",
            "G -3",
        ]
        self.pad_octaves = [
            -3,
            -3,
            -3,
            -3,
            -3,
            -3,
            -3,
            -3,
        ]
        self.pad_roots = [
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]

    def to_dict(self):
        return {
            "buffer": self.buffer.to_dict(),
            "base_note": self.base_note,
            "key_note": self.key_note,
            "key_degree": self.key_degree,
            "key_degree_octave": self.key_degree_octave,
            "selected_mode": self.selected_mode,
            "selected_play_type": self.selected_play_type,
            "selected_chord_comp": self.selected_chord_comp,
            "chord_type": self.chord_type,
            "raw_key_knob": self.raw_key_knob,
            "raw_knob_mode": self.raw_knob_mode,
            "raw_knob_play_type": self.raw_knob_play_type,
            "raw_knob_chord_type": self.raw_knob_chord_type,
            "pad_intervals": self.pad_intervals,
            "pad_values": self.pad_values,
            "pad_notes": self.pad_notes,
            "pad_octaves": self.pad_octaves,
            "pad_roots": self.pad_roots,
        }

    def to_tuple(self):
        return (
            ("buffer", self.buffer.to_tuple()),
            ("base_note", self.base_note),
            ("key_note", self.key_note),
            ("key_degree", self.key_degree),
            ("key_degree_octave", self.key_degree_octave),
            ("selected_mode", self.selected_mode),
            ("selected_play_type", self.selected_play_type),
            ("selected_chord_comp", self.selected_chord_comp),
            ("chord_type", self.chord_type),
            ("raw_key_knob", self.raw_key_knob),
            ("raw_knob_mode", self.raw_knob_mode),
            ("raw_knob_play_type", self.raw_knob_play_type),
            ("raw_knob_chord_type", self.raw_knob_chord_type),
            ("pad_intervals", self.pad_intervals),
            ("pad_values", self.pad_values),
            ("pad_notes", self.pad_notes),
            ("pad_octaves", self.pad_octaves),
            ("pad_roots", self.pad_roots),
        )
