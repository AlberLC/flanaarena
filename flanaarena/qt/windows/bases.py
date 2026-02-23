from collections.abc import Callable
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

import constants


class GuiWindow[T](QtWidgets.QMainWindow):
    def __init__(self, icon_path: str | Path, central_widget_factory: Callable[[], T], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.icon = QtGui.QIcon(str(icon_path))
        self.central_widget = central_widget_factory()

        self.setWindowTitle(constants.APP_NAME)
        self.setWindowIcon(self.icon)
        # noinspection PyTypeChecker
        self.setCentralWidget(self.central_widget)


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
