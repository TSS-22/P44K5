from enum import Enum


class ControllerMessageFlag(Enum):
    PAD_PRESSED = "pad_pressed"
    PAD_RELEASED = "pad_released"
    BASE_NOTE_CHANGED = "base_note_changed"
    KEY_NOTE_CHANGED = "key_note_changed"
    MODE_CHANGED = "mode_changed"
    CHORD_SIZE_CHANGED = "CHORD_SIZE_CHANGED"
    CHORD_COMP_CHANGED = "chord_comp_changed"
    KNOB_BASE_SLIDE = "knob_base_slide"
    KNOB_KEY_SLIDE = "knob_key_slide"
    BYPASS = "bypass"
    GUI_CHANGE = "gui_change"
