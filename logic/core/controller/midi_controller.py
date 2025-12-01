import json
from logic.core.controller.midi_controller_output import MidiControllerOutput
from logic.core.controller.input_pad import InputPad
from logic.core.controller.midi_controller_settings import MidiControllerSettings
from logic.core.controller.midi_controller_state import MidiControllerState
from logic.core.controller.controller_message_flag import ControllerMessageFlag
from data import data_general as dg


class MidiController:

    list_note = dg.hc_chromatic_scale

    def __init__(self):
        # Put the automatic loading of the last config here
        with open(
            "./data/user_settings.json", "r", encoding="UTF-8"
        ) as file_settings_user:
            self.user_settings = json.load(file_settings_user)
            with open(
                self.user_settings["last_load_config"], "r", encoding="UTF-8"
            ) as file_settings_controller:
                midi_device_settings = json.load(file_settings_controller)

        self.controller_settings = MidiControllerSettings(midi_device_settings)

        self.state = MidiControllerState(
            selected_mode=self.controller_settings.list_modes[0],
            selected_chord_comp=self.controller_settings.list_chord_comp[0],
            selected_chord_size=self.controller_settings.list_chord_size[0],
        )
        # Init state and class variables
        self.compute_pad_intervals()

        self.mode_prog_chord = {}
        self._init_mode_prog_chord()

        self.mode_prog_tone = {}
        self._init_mode_prog_tone()

        self.state.selected_mode_chord_prog = []
        self.compute_mode_chord_prog()

    def _init_mode_prog_chord(self):
        for key, val_list in dg.chord_prog_mode.items():
            self.mode_prog_chord[key] = [
                dg.chords[dg.ionian_chord_prog[val]] for val in val_list
            ]
        self.mode_prog_chord.update({"None": [[0]] * 8})

    def _init_mode_prog_tone(self):
        for key, val_list in dg.tone_prog_mode.items():
            self.mode_prog_tone[key] = [dg.tone_progression[val] for val in val_list]

    def get_state(self):
        return self.state

    def load_micro_controller_settings(self, midi_device_settings):
        # IMRPOVE
        # Add a check to see if the configuration is valid before loading.
        self.controller_settings = MidiControllerSettings(midi_device_settings)
        print(self.controller_settings)

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
        self.state.name_chords = self.compute_name_chord_prog()

    def compute_pad_intervals(self):
        if self.state.selected_mode == "None":
            self.state.pad_intervals = [0] + [1] * 7
        else:
            self.state.pad_intervals = (
                [0]
                + self.mode_prog_tone[self.state.selected_mode][self.state.key_degree :]
                + self.mode_prog_tone[self.state.selected_mode][: self.state.key_degree]
            )

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
        return sum(self.state.pad_intervals[: id_pad + 1])

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
                int(pad_val / dg.hc_len_chromatic_scale) + dg.hc_offset_midi_octave
            )
            # Compute root
            if (pad_val - self.state.base_note) % dg.hc_len_chromatic_scale == 0:
                pads_root.append(True)
            else:
                pads_root.append(False)
            # Compute the chord notes
            for chord_index in self.state.selected_chord_size["comp"]:
                if (
                    self.state.selected_mode == "None"
                    and self.state.selected_chord_comp["name"] == "Normal"
                ):
                    notes_chords.append(self.list_note[pad_val % len(self.list_note)])
                    break
                elif (
                    self.state.selected_chord_comp["name"] == "Normal"
                    and self.state.selected_mode != "None"
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
        self.state.name_chords = self.compute_name_chord_prog()

    def compute_name_chord_prog(self):
        name_chords = [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # IMPROVE
        # self.state.idx_chord_comp == 1, this smell like problem
        print(f"protential problem: {self.state.idx_chord_comp}")
        if self.state.selected_mode != "None" and self.state.idx_chord_comp == 1:
            print(f"protential problem value == 1: {self.state.idx_chord_comp}")
            name_chords = (
                dg.hc_name_chord_prog[self.state.selected_mode][self.state.key_degree :]
                + dg.hc_name_chord_prog[self.state.selected_mode][
                    : self.state.key_degree
                ]
                + [
                    dg.hc_name_chord_prog[self.state.selected_mode][
                        self.state.key_degree
                    ]
                ]
            )
        return name_chords

    ##################
    # PHYSICAL LOGIC #
    ##################
    # Pad pressed
    def pad_pressed(self, input_val):
        if self.controller_settings.base_note_offset:
            id_pad = input_val.note - self.controller_settings.base_note_offset
            self.state.buffer.velocity[id_pad] = input_val.velocity
            note = self.check_note(
                input_val.note
                - self.controller_settings.base_note_offset
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
        else:
            # IMPROVE
            # Handle case with improper config (prevent it when loading)
            pass

    # Pad released
    def pad_released(self, input_val):
        id_pad = input_val.note - self.controller_settings.base_note_offset
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
    def knob_base_note_changed(self, input_val):
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
    def knob_key_note_changed(self, input_val):
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
                temp = temp_note % -7 - 1
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
    def knob_mode_changed(self, input_val):
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
    def knob_chord_comp_changed(self, input_val):
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

    def knob_chord_size_changed(self, input_val):
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
            if self.controller_settings.pad_mode == dg.hc_pad_mode_note:
                # Note pressed
                if message.type == "note_on":
                    output = self.pad_pressed(message)

                elif message.type == "note_off":
                    output = self.pad_released(message)

            if message.type == "control_change":
                if self.controller_settings.pad_mode == dg.hc_pad_mode_cc:
                    if (
                        message.control >= self.controller_settings.base_note_offset
                    ) and (
                        message.control <= self.controller_settings.base_note_offset + 7
                    ):
                        if message.value > 0:
                            output = self.pad_pressed(
                                InputPad(note=message.control, velocity=message.value)
                            )
                        else:
                            output = self.pad_released(InputPad(note=message.control))

                # Knob 1: select_base_note
                if message.control == self.controller_settings.id_knob_base_note:
                    output = self.knob_base_note_changed(message)

                # Knob 2: select_keyNote
                elif message.control == self.controller_settings.id_knob_key_note:
                    if self.state.selected_mode != "None":
                        output = self.knob_key_note_changed(message)

                # Knob 3: select_mode
                elif message.control == self.controller_settings.id_knob_mode:
                    output = self.knob_mode_changed(message)

                # Knob 4: select_chord_comp
                elif message.control == self.controller_settings.id_knob_chord_comp:
                    output = self.knob_chord_comp_changed(message)

                # Knob 5:select_chord_size
                elif message.control == self.controller_settings.id_knob_chord_size:
                    if self.state.idx_chord_comp != 0:
                        output = self.knob_chord_size_changed(message)

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
