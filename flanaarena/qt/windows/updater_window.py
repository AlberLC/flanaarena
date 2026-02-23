from PySide6 import QtCore, QtGui

import constants
from qt.buttons import TitleButton
from qt.widgets.central_widgets.updater_central_widget import UpdaterCentralWidget
from qt.windows.bases import GuiWindow, MovableWindow


class UpdaterWindow(MovableWindow, GuiWindow[UpdaterCentralWidget]):
    def __init__(self) -> None:
        super().__init__(constants.LOGO_PATH, lambda: UpdaterCentralWidget(self))

        self.button_close = TitleButton(constants.CLOSE_PATH, self, index=0, right_margin=2, top_margin=2)

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.button_close.setStyleSheet('QPushButton:hover{background-color: darkred}')
        self.show()

        self.button_close.clicked.connect(self.close)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        super().paintEvent(event)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtGui.QColorConstants.White if self.isActiveWindow() else QtGui.QColorConstants.DarkGray)

        border_margin = 1
        radius = 5

        painter.drawRoundedRect(
            self.rect().adjusted(border_margin, border_margin, -border_margin, -border_margin),
            radius,
            radius
        )

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.updateGeometry()

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(300, 150)

    def updateGeometry(self) -> None:
        super().updateGeometry()

        self.button_close.updateGeometry()
