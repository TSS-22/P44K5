from PySide6.QtCore import QObject, Signal


class MainLogicSignals(QObject):

    finished = Signal()
    stopped = Signal()
    base_note_changed = Signal(dict)
    key_note_changed = Signal(dict)
    panel_mode_changed = Signal(dict)
    panel_chord_comp_changed = Signal(dict)
    panel_chord_size_changed = Signal(dict)
    pad_grid_changed = Signal(dict)
