from collections.abc import Callable

from PySide6 import QtCore, QtGui, QtWidgets

import constants


class BlueDarkApp(QtWidgets.QApplication):
    # noinspection PyArgumentList
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

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


class GuiApp[T](BlueDarkApp):
    close_signal = QtCore.Signal()

    def __init__(self, window_factory: Callable[[], T], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.window = window_factory()
        self.gui = self.window.central_widget

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.close_signal.connect(self.window.close)
