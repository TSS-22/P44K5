from data import data_general as dg


class MidiControllerSettings:
    def __init__(self, midi_device_settings):

        self.list_modes = dg.hc_list_mode
        self.list_chord_comp = dg.knob_values_chord_comp
        self.list_chord_size = dg.knob_values_chord_size

        self.pad_mode = midi_device_settings["pad_mode"]
        self.base_note_offset = midi_device_settings["base_note_offset"]
        self.id_knob_mode = midi_device_settings["id_knob_mode"]
        self.id_knob_chord_comp = midi_device_settings["id_knob_chord_comp"]
        self.id_knob_chord_size = midi_device_settings["id_knob_chord_size"]
        self.id_knob_base_note = midi_device_settings["id_knob_base_note"]
        self.id_knob_key_note = midi_device_settings["id_knob_key_note"]

        # Most likely will need to put that into a function to allow for user to change the settings.
        self.pot_max_value = (
            midi_device_settings["pot_max_value"] + 1
        )  # For out of oundary error prevention

        # Division/quadrant magnitude between each mode or chord comp
        self.knob_div_modes = self.pot_max_value / len(self.list_modes)
        self.knob_div_chord_comp = self.pot_max_value / len(self.list_chord_comp)
        self.knob_div_chord_size = self.pot_max_value / len(self.list_chord_size)
