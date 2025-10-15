class MidiControllerBuffer:
    def __init__(self):
        self.velocity = [0, 0, 0, 0, 0, 0, 0, 0]
        self.notes = [[], [], [], [], [], [], [], []]

    def to_dict(self):
        return {
            "velocity": self.velocity,
            "notes": self.notes,
        }

    def to_tuple(self):
        return (("velocity", self.velocity), ("notes", self.notes))
