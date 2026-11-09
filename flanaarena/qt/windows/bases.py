from collections.abc import Callable
from pathlib import Path
from typing import Any

from PySide6 import QtCore, QtGui, QtWidgets

import constants


class GuiWindow[TCentralWidget](QtWidgets.QMainWindow):
    def __init__(
        self,
        icon_path: str | Path,
        central_widget_factory: Callable[[], TCentralWidget],
        *args: Any,
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)

        self.icon = QtGui.QIcon(str(icon_path))
        self.central_widget = central_widget_factory()

        self.setWindowTitle(constants.APP_NAME)
        self.setWindowIcon(self.icon)
        self.setCentralWidget(self.central_widget)


class MovableWindow:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.last_position: QtCore.QPoint | None = None
        self.is_moving = False

    def _move(self) -> None:
        if not self.last_position:
            return

        # noinspection unresolved-references
        self.move(self.pos() + self.mapFromGlobal(self.cursor().pos()) - self.last_position)

    def _on_mouse_left_press(self, event: QtGui.QMouseEvent) -> None:
        self.last_position = event.pos()

    def _on_mouse_move(self, _: QtGui.QMouseEvent) -> None:
        self._move()

    # noinspection pep8-naming
    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        # noinspection unresolved-references
        super().mouseMoveEvent(event)

        self.is_moving = True
        self._on_mouse_move(event)

    # noinspection pep8-naming
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # noinspection unresolved-references
        super().mousePressEvent(event)

        # noinspection unresolved-references
        self.setFocus()

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._on_mouse_left_press(event)

    # noinspection pep8-naming
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        # noinspection unresolved-references
        super().mouseReleaseEvent(event)

        self.is_moving = False
        self.last_position = None
