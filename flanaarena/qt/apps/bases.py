from collections.abc import Callable
from typing import Any, Self

from PySide6 import QtCore, QtGui, QtWidgets

import constants
lazy from qt.controllers.bases import Controller


class BlueDarkApp(QtWidgets.QApplication):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._set_style()

    def _set_style(self) -> None:
        palette = self.palette()

        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(157, 157, 157))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(52, 52, 52))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ToolTipBase, QtGui.QColor(255, 255, 220))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ToolTipText, QtGui.QColor(0, 0, 0))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(255, 255, 255, 128))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, QtGui.QColor(157, 157, 157))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, QtGui.QColor(60, 60, 60))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(157, 157, 157))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(193, 230, 242))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Light, QtGui.QColor(120, 120, 120))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Midlight, QtGui.QColor(90, 90, 90))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Dark, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Mid, QtGui.QColor(40, 40, 40))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Shadow, QtGui.QColor(0, 0, 0))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(*constants.PALETTE_HIGHLIGHT_COLOR))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Link, QtGui.QColor(48, 140, 198))
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.LinkVisited, QtGui.QColor(255, 0, 255))

        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, QtGui.QColor(45, 45, 45))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(13, 23, 81))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ToolTipBase, QtGui.QColor(60, 60, 60))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ToolTipText, QtGui.QColor(212, 212, 212))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(255, 255, 255, 128))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, QtGui.QColor(60, 60, 60))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(193, 230, 242))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Light, QtGui.QColor(120, 120, 120))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Midlight, QtGui.QColor(90, 90, 90))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Dark, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Mid, QtGui.QColor(40, 40, 40))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Shadow, QtGui.QColor(0, 0, 0))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(*constants.PALETTE_HIGHLIGHT_COLOR))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Link, QtGui.QColor(*constants.PALETTE_HIGHLIGHT_COLOR))
        palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.LinkVisited, QtGui.QColor(13, 23, 81))

        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, QtGui.QColor(45, 45, 45))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(13, 23, 81))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ToolTipBase, QtGui.QColor(60, 60, 60))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ToolTipText, QtGui.QColor(212, 212, 212))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, QtGui.QColor(60, 60, 60))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(193, 230, 242))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Light, QtGui.QColor(120, 120, 120))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Midlight, QtGui.QColor(90, 90, 90))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Dark, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Mid, QtGui.QColor(40, 40, 40))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Shadow, QtGui.QColor(0, 0, 0))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Link, QtGui.QColor(*constants.PALETTE_HIGHLIGHT_COLOR))
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.LinkVisited, QtGui.QColor(13, 23, 81))

        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Window, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Base, QtGui.QColor(45, 45, 45))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(13, 23, 81))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.ToolTipBase, QtGui.QColor(60, 60, 60))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.ToolTipText, QtGui.QColor(212, 212, 212))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Text, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Button, QtGui.QColor(60, 60, 60))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(193, 230, 242))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Light, QtGui.QColor(120, 120, 120))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Midlight, QtGui.QColor(90, 90, 90))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Dark, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Mid, QtGui.QColor(40, 40, 40))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Shadow, QtGui.QColor(0, 0, 0))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(*constants.PALETTE_HIGHLIGHT_COLOR))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Link, QtGui.QColor(*constants.PALETTE_HIGHLIGHT_COLOR))
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.LinkVisited, QtGui.QColor(13, 23, 81))

        self.setPalette(palette)


class GuiApp[TWindow: QtWidgets.QMainWindow, TController: Controller](BlueDarkApp):
    close_signal = QtCore.Signal()

    def __init__(
        self,
        window_factory: Callable[[], TWindow],
        controller_factory: Callable[[Self, TWindow], TController],
        *args: Any,
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)

        self._window = window_factory()
        self._controller = controller_factory(self, self._window)

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.close_signal.connect(self.quit, QtCore.Qt.ConnectionType.QueuedConnection)

    def _start(self) -> None:
        self._controller.start()

    def run(self) -> int:
        self._start()
        self._window.show()

        return self.exec()
