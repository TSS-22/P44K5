import json
from utilities import correct_file_path as correct_file_path
from midi_controller_output import MidiControllerOutput
from midi_controller_buffer import MidiControllerBuffer
from midi_controller_settings import MidiControllerSettings


class MidiController:
    # TODO change the name of some function like knob_playMode()as the plya might not be necessary. Make them more intuitive and simple
    # TODO reorganize the code in subclasses or something else to make the class more digestable
    # TODO replace the rturn message from note_on etc, as a class?
    def __init__(self):
        with open(
            correct_file_path("../data/data_options_play.json"), "r"
        ) as file_options_play:
            data_options_play = json.load(file_options_play)

        with open(
            correct_file_path("../data/data_settings.json"), "r"
        ) as file_settings:
            data_settings = json.load(file_settings)

        self.controller_settings = MidiControllerSettings(
            data_options_play, data_settings
        )

        self.buffer = MidiControllerBuffer()

        self.selected_mode = self.controller_settings.list_modes[0]
        self.selected_play_type = self.controller_settings.list_play_type[0]
        self.base_note = 0
        self.key_note = 0
        self.key_degree = 0

        self.base_note_offset = data_settings["base_note_offset"]

        self.mode_prog_chord = {}
        self._init_mode_prog_chord(data_options_play)

        self.mode_prog_tone = {}
        self._init_mode_prog_tone(data_options_play)

        self.selected_pad_interval = []
        self.compute_pad_intervals()

        # TODO I think that the base list for chord should be just 7 chord as the 8th is always a repeat of the first one (and not twice a Major chord as it is now)
        self.selected_mode_chord_prog = []
        self.compute_mode_chord_prog()

        self.chord_play_type = (
            []
        )  # This architecture is prone to error, put list_play_type and chord_play_style together
        # Create a dic with "name", "chord", that way I always have the name for single and normal. Actually that will make single the same as any mono chords play type
        # Can't I make the normal one also just like any  other play type ?
        # TODO Put the user file parser into a function when the need arise once the GUI is in working
        self._init_chord_play_style(data_options_play)

    def _init_mode_prog_chord(self, data):
        for key in data["playModes_chordProg"]:
            self.mode_prog_chord.update({key: []})
            for val in data["playModes_chordProg"][key]:
                self.mode_prog_chord[key].append(data[data["ionian_chord_prog"][val]])
        self.mode_prog_chord.update({"None": [[0]] * 8})

    def _init_mode_prog_tone(self, data):
        for key in data["playModes_toneProg"]:
            self.mode_prog_tone.update({key: []})
            for val in data["playModes_toneProg"][key]:
                self.mode_prog_tone[key].append(data["tone_progression"][val])

    def _init_chord_play_style(self, data):
        self.chord_play_type.append(
            {"name": "chord_major", "intervals": data["chord_major"]}
        )
        self.chord_play_type.append(
            {"name": "chord_minor", "intervals": data["chord_minor"]}
        )
        self.chord_play_type.append(
            {"name": "chord_dom7", "intervals": data["chord_dom7"]}
        )
        self.chord_play_type.append(
            {"name": "chord_dim", "intervals": data["chord_dim"]}
        )
        # Add user play style chord file processing here

    #############################
    # GENERAL LOGIC / UTILITIES #
    #############################
    # Check if the note doesn't go below or above the maximum MIDI protocol values
    # Used to prevent error when computing notes as they can go below and above
    # those values
    # min: 0
    # max: 127
    def check_note(self, note):
        if note > 127:
            return 127
        elif note < 0:
            return 0
        else:
            return note

    # Reset the key_degree value from controller settings.
    # Used when changing the mode
    def reset_key_degree(self):
        self.key_degree = 0
        self.compute_pad_intervals()
        self.compute_mode_chord_prog()

    def compute_pad_intervals(self):
        if self.selected_mode == "None":
            self.selected_pad_interval = [0] + [1] * 7
        else:
            self.selected_pad_interval = (
                [0]
                + self.mode_prog_tone[self.selected_mode][self.key_degree :]
                + self.mode_prog_tone[self.selected_mode][: self.key_degree]
            )

    def compute_mode_chord_prog(self):
        if self.selected_mode != "None":
            self.selected_mode_chord_prog = (
                self.mode_prog_chord[self.selected_mode][:-1][
                    self.key_degree :
                ]  # -1 to discard the double major atm
                + self.mode_prog_chord[self.selected_mode][:-1][: self.key_degree]
                + [self.mode_prog_chord[self.selected_mode][:-1][self.key_degree]]
            )

    def count_interval(self, id_pad):
        return sum(self.selected_pad_interval[: id_pad + 1])

    ##################
    # PHYSICAL LOGIC #
    ##################
    # Pad pressed
    def pad_pressed(self, input):
        id_pad = input.note - self.base_note_offset
        self.buffer.velocity[id_pad] = input.velocity
        note = self.check_note(
            input.note
            - self.base_note_offset
            + self.base_note
            + self.key_note
            + self.count_interval(id_pad)
            - id_pad
        )
        return MidiControllerOutput(self.note_on(note, input.velocity, id_pad))

    # Pad released
    def pad_released(self, input):
        id_pad = input.note - self.base_note_offset
        self.buffer.velocity[id_pad] = 0
        list_note_off = []
        for note in self.buffer.note[id_pad]:
            skip = False
            for idx, pad in enumerate(self.buffer.velocity):
                if pad > 0:
                    for note_other_pad in self.buffer.note[idx]:
                        if note_other_pad == note:
                            skip = True
                            break
                if skip:
                    break
            if skip:
                continue
            list_note_off.append(self.note_off(note, id_pad))
        self.buffer.note[id_pad] = []
        return MidiControllerOutput(list_note_off)

    #
    def knob_base_note(self, input):
        any_pad_on = False
        for id_pad, pad in enumerate(self.buffer.velocity):
            if pad > 0:
                any_pad_on = True
                temp_note = self.check_note(
                    self.buffer.note[id_pad][0] + input.value - 64
                )
                return MidiControllerOutput(
                    self.note_on(temp_note, self.buffer.velocity[id_pad], id_pad)
                )

        if not any_pad_on:
            self.select_base_note(input.value)
            print(f"Base note: {self.base_note}")
            return MidiControllerOutput()

    #
    def knob_key_note(self, input):
        any_pad_on = False
        for id_pad, pad in enumerate(self.buffer.velocity):
            if pad > 0:
                any_pad_on = True
                temp_note = self.check_note(
                    self.buffer.note[id_pad][0] + self.select_key_note(input.value)
                )
                return MidiControllerOutput(
                    self.note_on(temp_note, self.buffer.velocity[id_pad], id_pad)
                )

        if not any_pad_on:
            self.select_key_note(input.value)
            print(f"Key note: {self.key_note}")
            print(f"Key degree: {self.key_degree}")
            return MidiControllerOutput()

    ########################
    # BUSINESS LOGIC LAYER #
    ########################
    def select_base_note(self, note_value):
        self.base_note = note_value
        return MidiControllerOutput()

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
    def select_key_note(self, input_val):
        temp_note = int((input_val - 64) / 3)
        degree = 0
        if self.selected_mode == "None":
            self.key_note = temp_note
            self.reset_key_degree()
            return temp_note

        else:
            octave = int(temp_note / 7) * 12
            inter_octave = 0

            if temp_note >= 0:
                temp = temp_note % 7
                for val in self.mode_prog_tone[self.selected_mode][:temp]:
                    inter_octave = inter_octave + abs(val)
                    degree = degree + 1

            else:
                temp = temp_note % -7 - 1  # To test
                for val in self.mode_prog_tone[self.selected_mode][:temp:-1]:
                    inter_octave = inter_octave - abs(val)
                    degree = degree + 1
                if degree != 0:
                    degree = abs(degree - 7)

            self.key_degree = degree
            self.key_note = octave + inter_octave
            self.compute_pad_intervals()
            self.compute_mode_chord_prog()

            return octave + inter_octave

    # Used to select the modes.
    # Refer to "./data.py/knob_values_playModes" for more details about the possible values
    def knob_playMode(self, input):
        # Should I reset or not ? good question
        self.reset_key_degree()
        self.selected_mode = self.controller_settings.list_modes[
            int(input.value / self.controller_settings.knob_div_modes)
        ]
        print(
            f"Mode: {self.controller_settings.list_modes[int(input.value/self.controller_settings.knob_div_modes)]}\n"
        )
        return MidiControllerOutput()

    # Used to select the type of play, either chord like or single note.
    # Refer to "./data.py/knob_values_playTypes" for more details about the possible values
    def knob_playTypes(self, input):
        self.selected_play_type = self.controller_settings.list_play_type[
            int(input.value / self.controller_settings.knob_div_playType)
        ]
        print(
            f"Play type: {self.controller_settings.list_play_type[int(input.value/self.controller_settings.knob_div_playType)]}\n"
        )
        return MidiControllerOutput()

    ##########################
    # MIDI MESSAGES COMMANDS #
    ##########################
    def note_off(self, note, velocity):
        return {"message": "note_off", "note": note, "velocity": velocity}

    def note_on(self, note, velocity, id_pad):
        midi_message_note_on = []

        # Isn't the issue with the is not needed, just a problem that mode = "None" is just not where/assessed where it should be ?
        if self.selected_play_type["name"] == "Normal" and self.selected_mode != "None":
            for chord_interval in self.selected_mode_chord_prog[id_pad]:
                midi_message_note_on.append(
                    self.append_note_on(note + chord_interval, velocity, id_pad)
                )

        else:
            for chord_interval in self.selected_play_type["chord"]:
                midi_message_note_on.append(
                    self.append_note_on(note + chord_interval, velocity, id_pad)
                )

        return midi_message_note_on

    def append_note_on(self, note, velocity, id_pad):
        self.buffer.note[id_pad].append(note)
        print(f"Note on: {note} | Pad: {id_pad + 1}")
        return {"message": "note_on", "note": note, "velocity": velocity}

    #######################
    # COMMUNICATION LAYER #
    #######################
    # C'est un peu degueux ce manque de standardisation de l'ouput : empty/message
    def receive_message(self, message):
        output = MidiControllerOutput([message])
        # Note pressed
        if message.type == "note_on":
            output = self.pad_pressed(message)

        elif message.type == "note_off":
            output = self.pad_released(message)

        elif message.type == "control_change":
            # Knob 1: select_base_note
            if message.control == self.controller_settings.id_knob_base_note:
                output = self.knob_base_note(message)

            # Knob 5: select_keyNote
            elif message.control == self.controller_settings.id_knob_key_note:
                output = self.knob_key_note(message)

            # Knob 4: select_playMode
            elif message.control == self.controller_settings.id_knob_mode:
                output = self.knob_playMode(message)

            # Knob 8: select_playType
            elif message.control == self.controller_settings.id_knob_play_type:
                output = self.knob_playTypes(message)

            # Unassigned command
            else:
                # output = MidiControllerOutputmessage
                pass

        # Unassigned command
        else:
            # output = message
            pass

        return output
