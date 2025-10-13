from PySide6.QtCore import QObject, Signal


class QtMidiConnectorSignal(QObject):

    midi_messages = Signal(list)
    finished = Signal()
    stopped = Signal()
