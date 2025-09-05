class MidiControllerSettings:
    def __init__(self, data_options_play, data_settings):

        self.list_modes = data_options_play["knob_values_playModes"]
        self.list_play_type = data_options_play["knob_values_playTypes"]

        self.id_knob_base_note = data_settings["id_knob_base_note"]
        self.id_knob_key_note = data_settings["id_knob_key_note"]
        self.id_knob_mode = data_settings["id_knob_mode"]
        self.id_knob_play_type = data_settings["id_knob_play_type"]

        # Most likely will need to put that into a function to allow for user to change the settings.
        self.pot_max_value = (
            data_settings["pot_max_value"] + 1
        )  # For out of oundary error prevention

        # Division/quadrant magnitude between each mode or play type
        self.knob_div_modes = self.pot_max_value / len(self.list_modes)
        self.knob_div_playType = self.pot_max_value / len(self.list_play_type)

        self.list_modes = data_options_play["knob_values_playModes"]
        self.list_play_type = data_options_play["knob_values_playTypes"]
