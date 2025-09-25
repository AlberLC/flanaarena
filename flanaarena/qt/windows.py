from PySide6 import QtCore, QtGui, QtWidgets

import constants
from qt.widgets.central_widget import CentralWidget


class MovableWindow:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.last_position: QtCore.QPoint | None = None
        self.is_moving = False

    def _move(self) -> None:
        # noinspection PyUnresolvedReferences
        self.move(self.pos() + self.mapFromGlobal(self.cursor().pos()) - self.last_position)

    def _on_mouse_left_press(self, event: QtGui.QMouseEvent) -> None:
        self.last_position = event.pos()

    def _on_mouse_move(self, _: QtGui.QMouseEvent) -> None:
        self._move()

    # noinspection PyPep8Naming
    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        # noinspection PyUnresolvedReferences
        super().mouseMoveEvent(event)
        if self.last_position is None:
            return

        self.is_moving = True
        self._on_mouse_move(event)

    # noinspection PyPep8Naming
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # noinspection PyUnresolvedReferences
        super().mousePressEvent(event)
        # noinspection PyUnresolvedReferences
        self.setFocus()
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._on_mouse_left_press(event)

    # noinspection PyPep8Naming
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        # noinspection PyUnresolvedReferences
        super().mouseReleaseEvent(event)
        self.is_moving = False
        self.last_position = None


class MainWindow(MovableWindow, QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowIcon(QtGui.QIcon(str(constants.LOGO_PATH)))
        self.setWindowTitle(constants.APP_NAME)

        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)
