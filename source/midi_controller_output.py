import mido
from source.message_type import MessageType


class MidiControllerOutput:
    def __init__(self, midi_controller_state, list_message=[]):
        self.state = midi_controller_state
        self.messages = []
        for msg in list_message:
            if isinstance(msg, mido.Message):
                self.messages.append(msg)
            else:  # msg["message"] == "note_on" or msg["message"] == "note_off"
                self.messages.append(
                    mido.Message(
                        msg["message"], note=msg["note"], velocity=msg["velocity"]
                    )
                )
