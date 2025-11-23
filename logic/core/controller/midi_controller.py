import json
from logic.core.controller.midi_controller_output import MidiControllerOutput
from logic.core.controller.midi_controller_settings import MidiControllerSettings
from logic.core.controller.midi_controller_state import MidiControllerState
from logic.core.controller.controller_message_flag import ControllerMessageFlag
from logic.hardcoded import (
    hc_chromatic_scale,
    hc_len_chromatic_scale,
    hc_offset_midi_octave,
)


class MidiController:

    list_note = hc_chromatic_scale

    # TODO replace the rturn message from note_on etc, as a class?
    def __init__(self):
        with open(
            "./data/data_options_play.json", "r", encoding="UTF-8"
        ) as file_options_play:
            data_options_play = json.load(file_options_play)

        with open("./data/akai_lpd8_mk2.json", "r", encoding="UTF-8") as file_settings:
            midi_device_settings = json.load(file_settings)

        self.controller_settings = MidiControllerSettings(
            data_options_play, midi_device_settings
        )

        self.state = MidiControllerState(
            selected_mode=self.controller_settings.list_modes[0],
            selected_chord_comp=self.controller_settings.list_chord_comp[0],
            selected_chord_size=self.controller_settings.list_chord_size[0],
        )

        self.base_note_offset = midi_device_settings["base_note_offset"]

        self.mode_prog_chord = {}
        self._init_mode_prog_chord(data_options_play)

        self.mode_prog_tone = {}
        self._init_mode_prog_tone(data_options_play)

        self.selected_pad_interval = []
        self.compute_pad_intervals()

        self.state.selected_mode_chord_prog = []
        self.compute_mode_chord_prog()

        # self.chord_comp = (
        #     []
        # )  # This architecture is prone to error, put list_chord_comp and chord_play_style together
        # # Create a dic with "name", "chord", that way I always have the name for single and normal. Actually that will make single the same as any mono chords comp
        # # Can't I make the normal one also just like any  other chord comp ?
        # # TODO Put the user file parser into a function when the need arise once the GUI is in working
        # self._init_chord_comp(data_options_play)

    def _init_mode_prog_chord(self, data):
        for key in data["chord_prog_mode"]:
            self.mode_prog_chord.update({key: []})
            for val in data["chord_prog_mode"][key]:
                self.mode_prog_chord[key].append(data[data["ionian_chord_prog"][val]])
        self.mode_prog_chord.update({"None": [[0]] * 8})

    def _init_mode_prog_tone(self, data):
        for key in data["tone_prog_mode"]:
            self.mode_prog_tone.update({key: []})
            for val in data["tone_prog_mode"][key]:
                self.mode_prog_tone[key].append(data["tone_progression"][val])

    # def _init_chord_comp(self, data):
    #     self.chord_comp.append(
    #         {"name": "chord_major", "intervals": data["chord_major"]}
    #     )
    #     self.chord_comp.append(
    #         {"name": "chord_minor", "intervals": data["chord_minor"]}
    #     )
    #     self.chord_comp.append({"name": "chord_dom7", "intervals": data["chord_dom7"]})
    #     self.chord_comp.append({"name": "chord_dim", "intervals": data["chord_dim"]})

    def get_state(self):
        return self.state

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
        self.state.key_degree = 0
        self.state.key_note = 0
        self.compute_pad_intervals()
        self.compute_mode_chord_prog()

    def compute_pad_intervals(self):
        if self.state.selected_mode == "None":
            self.selected_pad_interval = [0] + [1] * 7
        else:
            self.selected_pad_interval = (
                [0]
                + self.mode_prog_tone[self.state.selected_mode][self.state.key_degree :]
                + self.mode_prog_tone[self.state.selected_mode][: self.state.key_degree]
            )
        self.state.pad_intervals = self.selected_pad_interval

    def compute_mode_chord_prog(self):
        if self.state.selected_mode != "None":
            self.state.selected_mode_chord_prog = (
                self.mode_prog_chord[self.state.selected_mode][:-1][
                    self.state.key_degree :
                ]  # -1 to discard the double major atm
                + self.mode_prog_chord[self.state.selected_mode][:-1][
                    : self.state.key_degree
                ]
                + [
                    self.mode_prog_chord[self.state.selected_mode][:-1][
                        self.state.key_degree
                    ]
                ]
            )

    def count_interval(self, id_pad):
        return sum(self.selected_pad_interval[: id_pad + 1])

    def toggle_bypass(self):
        self.state.bypass = not self.state.bypass

    def compute_pad_note(self):
        # Get the state of the pads
        pads_state = []
        for i in range(0, len(self.state.pad_intervals)):
            interval = 0
            for j in range(i + 1):
                interval += self.state.pad_intervals[j]
            pads_state.append(self.state.base_note + self.state.key_note + interval)

        pads_note = []
        pads_octave = []
        pads_root = []
        pads_note_chord = []
        for id_pad, pad_val in enumerate(pads_state):
            notes_chords = []
            # Compute the note associated with the index calculated above
            pads_note.append(self.list_note[pad_val % len(self.list_note)])
            # Compute the octave
            pads_octave.append(
                int(pad_val / hc_len_chromatic_scale) + hc_offset_midi_octave
            )
            # Compute root
            if (pad_val - self.state.base_note) % hc_len_chromatic_scale == 0:
                pads_root.append(True)
            else:
                pads_root.append(False)
            # Compute the chord notes
            for chord_index in self.state.selected_chord_size["comp"]:
                if self.state.selected_chord_comp["name"] == "Single" or (
                    self.state.selected_mode == "None"
                    and self.state.selected_chord_comp["name"] == "Normal"
                ):
                    notes_chords.append(self.list_note[pad_val % len(self.list_note)])
                    break
                elif (
                    self.state.selected_chord_comp["name"] == "Normal"
                    and self.state.selected_mode is not "None"
                ):
                    notes_chords.append(
                        self.list_note[
                            (
                                pad_val
                                + self.state.selected_mode_chord_prog[id_pad][
                                    chord_index
                                ]
                            )
                            % len(self.list_note)
                        ]
                    )
                else:
                    notes_chords.append(
                        self.list_note[
                            (
                                pad_val
                                + self.state.selected_chord_comp["chord"][chord_index]
                            )
                            % len(self.list_note)
                        ]
                    )
            pads_note_chord.append(notes_chords)

        self.state.pads_state = pads_state
        self.state.pad_notes = pads_note
        self.state.pad_octaves = pads_octave
        self.state.pad_roots = pads_root
        self.state.pad_notes_chords = pads_note_chord

    ##################
    # PHYSICAL LOGIC #
    ##################
    # Pad pressed
    def pad_pressed(self, input_val):
        id_pad = input_val.note - self.base_note_offset
        self.state.buffer.velocity[id_pad] = input_val.velocity
        note = self.check_note(
            input_val.note
            - self.base_note_offset
            + self.state.base_note
            + self.state.key_note
            + self.count_interval(id_pad)
            - id_pad
        )
        return MidiControllerOutput(
            flag=ControllerMessageFlag.PAD_PRESSED,
            state=self.get_state(),
            list_message=self.note_on(note, input_val.velocity, id_pad),
        )

    # Pad released
    def pad_released(self, input_val):
        id_pad = input_val.note - self.base_note_offset
        self.state.buffer.velocity[id_pad] = 0
        list_note_off = []
        for note in self.state.buffer.notes[id_pad]:
            skip = False
            for idx, pad in enumerate(self.state.buffer.velocity):
                if pad > 0:
                    for note_other_pad in self.state.buffer.notes[idx]:
                        if note_other_pad == note:
                            skip = True
                            break
                if skip:
                    break
            if skip:
                continue
            list_note_off.append(self.note_off(note, id_pad))
        self.state.buffer.notes[id_pad] = []
        return MidiControllerOutput(
            flag=ControllerMessageFlag.PAD_RELEASED,
            state=self.get_state(),
            list_message=list_note_off,
        )

    #
    def knob_base_note(self, input_val):
        any_pad_on = False
        for id_pad, pad in enumerate(self.state.buffer.velocity):
            if pad > 0:
                any_pad_on = True
                temp_note = self.check_note(
                    self.state.buffer.notes[id_pad][0] + input_val.value - 64
                )
                return MidiControllerOutput(
                    flag=ControllerMessageFlag.KNOB_BASE_SLIDE,
                    state=self.get_state(),
                    list_message=self.note_on(
                        temp_note, self.state.buffer.velocity[id_pad], id_pad
                    ),
                )

        if not any_pad_on:
            self.select_base_note(input_val.value)
            return MidiControllerOutput(
                flag=ControllerMessageFlag.BASE_NOTE_CHANGED, state=self.get_state()
            )

    #
    def knob_key_note(self, input_val):
        any_pad_on = False
        for id_pad, pad in enumerate(self.state.buffer.velocity):
            if pad > 0:
                any_pad_on = True
                temp_note = self.check_note(
                    self.state.buffer.notes[id_pad][0]
                    + self.select_key_note(input_val.value)
                )
                return MidiControllerOutput(
                    flag=ControllerMessageFlag.KNOB_KEY_SLIDE,
                    state=self.get_state(),
                    list_message=self.note_on(
                        temp_note, self.state.buffer.velocity[id_pad], id_pad
                    ),
                )

        if not any_pad_on:
            self.select_key_note(input_val.value)
            self.state.raw_key_knob = input_val.value
            return MidiControllerOutput(
                flag=ControllerMessageFlag.KEY_NOTE_CHANGED, state=self.get_state()
            )

    ########################
    # BUSINESS LOGIC LAYER #
    ########################
    def select_base_note(self, note_value):
        self.state.base_note = note_value
        return MidiControllerOutput(
            flag=ControllerMessageFlag.BASE_NOTE_CHANGED, state=self.get_state()
        )

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
        if self.state.selected_mode == "None":
            self.state.key_note = temp_note
            self.reset_key_degree()
            return temp_note

        else:
            octave = int(temp_note / 7) * 12
            inter_octave = 0

            if temp_note >= 0:
                temp = temp_note % 7
                for val in self.mode_prog_tone[self.state.selected_mode][:temp]:
                    inter_octave = inter_octave + abs(val)
                    degree = degree + 1

            else:
                temp = temp_note % -7 - 1  # To test
                for val in self.mode_prog_tone[self.state.selected_mode][:temp:-1]:
                    inter_octave = inter_octave - abs(val)
                    degree = degree + 1
                if degree != 0:
                    degree = abs(degree - 7)

            self.state.key_degree = degree
            self.state.key_degree_octave = octave
            self.state.key_note = octave + inter_octave
            self.compute_pad_intervals()
            self.compute_mode_chord_prog()

            return octave + inter_octave

    # Used to select the modes.
    # Refer to "./data.py/knob_values_mode" for more details about the possible values
    def knob_mode(self, input_val):
        self.state.raw_knob_mode = input_val.value
        return self.select_mode(
            int(input_val.value / self.controller_settings.knob_div_modes)
        )

    def select_mode(self, idx_mode):
        self.state.idx_mode = idx_mode
        self.state.selected_mode = self.controller_settings.list_modes[idx_mode]
        self.reset_key_degree()
        return MidiControllerOutput(
            flag=ControllerMessageFlag.MODE_CHANGED, state=self.get_state()
        )

    # Used to select the chord comp, either chord like or single note.
    # Refer to "./data.py/knob_values_chord_comp" for more details about the possible values
    def knob_chord_comp(self, input_val):
        self.state.raw_knob_chord_comp = input_val.value
        return self.select_chord_comp(
            int(input_val.value / self.controller_settings.knob_div_chord_comp)
        )

    def select_chord_comp(self, idx_chord_comp):
        self.state.idx_chord_comp = idx_chord_comp
        self.state.selected_chord_comp = self.controller_settings.list_chord_comp[
            idx_chord_comp
        ]
        return MidiControllerOutput(
            flag=ControllerMessageFlag.CHORD_COMP_CHANGED, state=self.get_state()
        )

    def knob_chord_size(self, input_val):
        self.state.raw_knob_chord_size = input_val.value
        return self.select_chord_size(
            int(input_val.value / self.controller_settings.knob_div_chord_size)
        )

    def select_chord_size(self, idx_chord_size):
        self.state.idx_chord_size = idx_chord_size
        self.state.selected_chord_size = self.controller_settings.list_chord_size[
            idx_chord_size
        ]
        return MidiControllerOutput(
            flag=ControllerMessageFlag.CHORD_SIZE_CHANGED, state=self.get_state()
        )

    ##########################
    # MIDI MESSAGES COMMANDS #
    ##########################
    def note_off(self, note, velocity):
        return {"message": "note_off", "note": note, "velocity": velocity}

    def note_on(self, note, velocity, id_pad):
        midi_message_note_on = []

        # Isn't the issue with the is not needed, just a problem that mode = "None" is just not where/assessed where it should be ?
        if (
            self.state.selected_chord_comp["name"] == "Normal"
            and self.state.selected_mode != "None"
        ):
            for chord_interval in [
                self.state.selected_mode_chord_prog[id_pad][i]
                for i in self.state.selected_chord_size["comp"]
            ]:
                midi_message_note_on.append(
                    self.append_note_on(note + chord_interval, velocity, id_pad)
                )

        else:
            for chord_interval in [
                self.state.selected_chord_comp["chord"][i]
                for i in self.state.selected_chord_size["comp"][
                    : len(self.state.selected_chord_comp["chord"])
                ]
            ]:
                midi_message_note_on.append(
                    self.append_note_on(note + chord_interval, velocity, id_pad)
                )

        return midi_message_note_on

    def append_note_on(self, note, velocity, id_pad):
        self.state.buffer.notes[id_pad].append(note)
        return {"message": "note_on", "note": note, "velocity": velocity}

    #######################
    # COMMUNICATION LAYER #
    #######################
    def receive_message(self, message):
        output = MidiControllerOutput(
            flag=ControllerMessageFlag.BYPASS,
            state=self.get_state(),
            list_message=[message],
        )
        if self.state.bypass is False:
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

                # Knob 4: select_mode
                elif message.control == self.controller_settings.id_knob_mode:
                    output = self.knob_mode(message)

                # Knob 8: select_chord_comp
                elif message.control == self.controller_settings.id_knob_chord_comp:
                    output = self.knob_chord_comp(message)

                # Knob 7:select_chord_size
                elif message.control == self.controller_settings.id_knob_chord_size:
                    output = self.knob_chord_size(message)

                # Unassigned command
                else:
                    # output = MidiControllerOutputmessage
                    pass

            # Unassigned command
            else:
                # output = message
                pass

        self.compute_pad_note()
        output.state = self.get_state()
        return output
