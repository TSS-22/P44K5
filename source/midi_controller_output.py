import mido


class MidiControllerOutput:

    def __init__(self, list_message=[]):
        self.messages = []
        for msg in list_message:
            if isinstance(msg, mido.Message):
                self.messages.append(msg)
            else:  # msg["message"] == "note_on" or msg["message"] == "note_off"
                print(type(msg))
                self.messages.append(
                    mido.Message(
                        msg["message"], note=msg["note"], velocity=msg["velocity"]
                    )
                )
