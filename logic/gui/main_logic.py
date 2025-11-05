from PySide6.QtCore import QObject, Signal, Slot
from logic.gui.main_logic_signal import MainLogicSignal
from logic.core.controller.controller_message_flag import ControllerMessageFlag


class MainLogic(QObject):
    id_knob_base_note = 70  # HARDCODED
    signal = MainLogicSignal()

    @Slot()
    def handle_midi(self, midi_controller_output):
        if midi_controller_output["flag"] == ControllerMessageFlag.BASE_NOTE_CHANGED:
            self.signal.base_note_changed.emit(
                midi_controller_output["state"]["base_note"]
            )
        elif midi_controller_output["flag"] == ControllerMessageFlag.KEY_NOTE_CHANGED:
            self.signal.key_note_changed.emit(
                {
                    "key_degree": midi_controller_output["state"]["key_degree"],
                    "key_degree_octave": midi_controller_output["state"][
                        "key_degree_octave"
                    ],
                    "key_note": midi_controller_output["state"]["key_note"],
                    "raw_key_knob": midi_controller_output["state"]["raw_key_knob"],
                }
            )
        elif midi_controller_output["flag"] == ControllerMessageFlag.MODE_CHANGED:
            self.signal.panel_mode_changed.emit(
                {
                    "raw_knob_mode": midi_controller_output["state"]["raw_knob_mode"],
                    "selected_mode": midi_controller_output["state"]["selected_mode"],
                }
            )
        elif midi_controller_output["flag"] == ControllerMessageFlag.CHORD_CHANGED:
            self.signal.panel_chord_changed.emit(
                {
                    "raw_knob_chord_type": midi_controller_output["state"][
                        "raw_knob_chord_type"
                    ],
                    "chord_type": midi_controller_output["state"]["chord_type"],
                }
            )
        elif midi_controller_output["flag"] == ControllerMessageFlag.PLAY_CHANGED:
            self.signal.panel_play_changed.emit(
                {
                    "raw_knob_play_type": midi_controller_output["state"][
                        "raw_knob_play_type"
                    ],
                    "selected_play_type": midi_controller_output["state"][
                        "selected_play_type"
                    ],
                }
            )
        elif (
            midi_controller_output["flag"] == ControllerMessageFlag.PAD_PRESSED
            or ControllerMessageFlag.PAD_RELEASED
        ):
            self.signal.pad_grid_changed.emit(
                {
                    "velocity": midi_controller_output["state"]["buffer"]["velocity"],
                    "key_degree": midi_controller_output["state"]["key_degree"],
                    "base_note": midi_controller_output["state"]["base_note"],
                    "key_note": midi_controller_output["state"]["key_note"],
                    "pad_intervals": midi_controller_output["state"]["pad_intervals"],
                    "key_degree_octave": midi_controller_output["state"][
                        "key_degree_octave"
                    ],  # Probably key_note and key_degree_octave are redundant
                }
            )

    def do_work(self):
        # Simulate logic
        new_state = "Logic updated!"
        self.state_changed.emit(new_state)  # Notify UI
