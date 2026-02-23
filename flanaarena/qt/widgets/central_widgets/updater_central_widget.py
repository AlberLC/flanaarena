from PySide6 import QtCore, QtWidgets

import constants
from qt.widgets.bases import UiWidget


class UpdaterCentralWidget(UiWidget):
    label_state: QtWidgets.QLabel

    progress: QtWidgets.QProgressBar

    progress_signal = QtCore.Signal(float)
    state_signal = QtCore.Signal(str)

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(constants.UPDATER_APP_UI_PATH, parent=parent)

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.progress_signal.connect(self.update_progress, QtCore.Qt.ConnectionType.QueuedConnection)
        self.state_signal.connect(self.update_state, QtCore.Qt.ConnectionType.QueuedConnection)

    def update_progress(self, progress: float) -> None:
        self.progress.setValue(round(progress * 100))

    def update_state(self, text: str) -> None:
        self.label_state.setText(text)
