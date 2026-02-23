import pathlib

from PySide6 import QtCore, QtGui, QtWidgets


class TitleButton(QtWidgets.QPushButton):
    signal_resize = QtCore.Signal()

    def __init__(
        self,
        icon: str | bytes | pathlib.Path | QtGui.QIcon,
        parent: QtWidgets.QWidget,
        index: int,
        size=(32, 32),
        top_margin=0,
        bottom_margin=0,
        right_margin=0,
        icon_size=(16, 16),
        checkable=False
    ) -> None:
        if isinstance(icon, bytes):
            pixmap = QtGui.QPixmap()
            # noinspection PyTypeChecker
            pixmap.loadFromData(icon, 'svg')
            icon = QtGui.QIcon(pixmap)
        elif isinstance(icon, str | pathlib.Path):
            icon = QtGui.QIcon(str(icon))
        # noinspection PyArgumentList
        super().__init__(icon=icon, parent=parent)

        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.parent = parent
        self.index = index
        self.size = (size[0] - top_margin - bottom_margin, size[1] - top_margin - bottom_margin)
        self.top_margin = top_margin
        self.bottom_margin = bottom_margin
        self.right_margin = right_margin

        self.setFlat(True)
        # noinspection PyArgumentList
        self.setIconSize(QtCore.QSize(*icon_size))
        self.setStyleSheet('QPushButton:checked{background-color: rgb(50, 50, 180)}')
        self.setCheckable(checkable)

        self.connect_signals()

        self.updateGeometry()

    def connect_signals(self) -> None:
        self.signal_resize.connect(
            lambda: self.setGeometry(
                self.parent.width() - self.size[0] * (self.index + 1) - self.right_margin,
                self.top_margin,
                self.size[0],
                self.size[1]
            ),
            QtCore.Qt.ConnectionType.QueuedConnection
        )

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        self.setFlat(False)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.setFlat(True)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mouseMoveEvent(event)

        if self.rect().contains(event.position().toPoint()):
            self.setFlat(False)
        else:
            self.setFlat(True)

    def updateGeometry(self) -> None:
        super().updateGeometry()
        self.signal_resize.emit()
