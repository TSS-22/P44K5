import mido


class MidiControllerOutput:
    def __init__(self, state, flag, list_message=[]):
        self.flag = flag
        self.state = state
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

    def to_dict(self):
        return {
            "flag": self.flag,
            "state": self.state.to_dict(),
        }
