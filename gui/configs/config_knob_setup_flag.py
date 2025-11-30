from enum import Enum


class ConfigSetupFlag(Enum):
    UNKOWN = "Unkown function"
    MODE = "Mode selection"
    CHORD_COMP = "Chord composition selection"
    CHORD_SIZE = "Chord size selection"
    BASE_NOTE = "Base note selection"
    KEY_DEGREE = "Key degree selection"
    PAD = "Pad configuration"
    NONE = "No setup running"
