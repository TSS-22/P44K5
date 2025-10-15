from enum import Enum


class MessageType(Enum):
    PAD_ON = (0,)
    PAD_OFF = (1,)
    KNOB_BASE = (2,)
    KNOB_KEY = (3,)
    KNOB_SWING_BASE = (4,)
    KNOB_SWING_KEY = (5,)
    KNOB_CHORD_COMP = (6,)
    KNOB_MODE = (7,)
    KNOB_PLAY_TYPE = (8,)
    BYPASS = (9,)
    EMPTY = (10,)
