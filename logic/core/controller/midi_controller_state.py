from logic.core.controller.midi_controller_buffer import MidiControllerBuffer
from data.data_general import hc_offset_midi_octave


class MidiControllerState:
    def __init__(
        self,
        selected_mode,
        selected_chord_comp,
        selected_chord_size,
        selected_mode_chord_prog=None,
    ):
        self.bypass = False
        # self.configuration = False
        self.buffer = MidiControllerBuffer()
        self.base_note = 0
        self.key_note = 0
        self.key_degree = 0
        self.key_degree_octave = 0
        self.selected_mode = selected_mode
        self.selected_mode_chord_prog = selected_mode_chord_prog
        self.selected_chord_comp = selected_chord_comp
        self.selected_chord_size = selected_chord_size
        self.idx_mode = 0
        self.idx_chord_comp = 0
        self.idx_chord_size = 0
        self.raw_key_knob = 0
        self.pad_intervals = []
        self.pad_values = []
        self.pad_notes = [
            "C",
            "C#",
            "D",
            "D#",
            "E",
            "F",
            "F#",
            "G",
        ]
        self.pad_octaves = [
            hc_offset_midi_octave,
            hc_offset_midi_octave,
            hc_offset_midi_octave,
            hc_offset_midi_octave,
            hc_offset_midi_octave,
            hc_offset_midi_octave,
            hc_offset_midi_octave,
            hc_offset_midi_octave,
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
        self.pad_notes_chords = [
            ["C"],
            ["C#"],
            ["D"],
            ["D#"],
            ["E"],
            ["F"],
            ["F#"],
            ["G"],
        ]
        self.name_chords = [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]

    def to_dict(self):
        return {
            "buffer": self.buffer.to_dict(),
            "base_note": self.base_note,
            "key_note": self.key_note,
            "key_degree": self.key_degree,
            "key_degree_octave": self.key_degree_octave,
            "selected_mode": self.selected_mode,
            "selected_chord_comp": self.selected_chord_comp,
            "selected_chord_size": self.selected_chord_size,
            "selected_mode_chord_prog": self.selected_mode_chord_prog,
            "idx_mode": self.idx_mode,
            "idx_chord_comp": self.idx_chord_comp,
            "idx_chord_size": self.idx_chord_size,
            "raw_key_knob": self.raw_key_knob,
            "pad_intervals": self.pad_intervals,
            "pad_values": self.pad_values,
            "pad_notes": self.pad_notes,
            "pad_octaves": self.pad_octaves,
            "pad_roots": self.pad_roots,
            "pad_notes_chords": self.pad_notes_chords,
            "name_chords": self.name_chords,
        }
