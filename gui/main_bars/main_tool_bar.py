from PySide6.QtWidgets import QToolBar, QMainWindow, QComboBox
from PySide6.QtCore import Qt, QEvent, QSize
from gui.actions.action_bypass import QActionBypass
from gui.actions.action_load import QActionConfigLoad
from gui.actions.action_new import QActionConfigNew
from gui.actions.action_edit import QActionConfigEdit
from gui.actions.action_connect import QActionMidiConnect
from gui.actions.action_refresh import QActionMidiRefresh
from gui.configs.combo_midi_list import CmbBoxMidiController


class MainToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            border: none;
            background: #eeeeee;
            spacing: 2px;
            """
        )
        self.setIconSize(QSize(22, 22))
        self.setMovable(False)  # Prevents the toolbar from being dragged
        self.setFloatable(
            False
        )  # Prevents the toolbar from being detached as a floating window
        self.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        self.setVisible(True)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.action_new = QActionConfigNew()
        self.action_load = QActionConfigLoad()
        self.action_edit = QActionConfigEdit()

        self.action_connect = QActionMidiConnect()
        self.cmb_midi_controller = CmbBoxMidiController(["A", "B", "C"])
        self.action_refresh = QActionMidiRefresh()

        self.action_bypass = QActionBypass()

        self.addAction(self.action_new)
        self.addAction(self.action_load)
        # self.addAction(self.action_edit)
        self.addSeparator()
        self.addWidget(self.cmb_midi_controller)
        self.addAction(self.action_refresh)
        self.addSeparator()
        self.addAction(self.action_bypass)
        self.setContextMenuPolicy(Qt.NoContextMenu)

    def event(self, event):
        # Ignore hide events
        if event.type() == QEvent.Hide:
            self.setVisible(True)
            return True
        elif event.type() == QEvent.ContextMenu:
            event.ignore()
        return super().event(event)
