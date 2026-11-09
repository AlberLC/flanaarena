from PySide6 import QtGui

import constants
from qt.apps.bases import GuiApp
from qt.controllers.updater_app_controller import UpdaterAppController
from qt.windows.updater_window import UpdaterWindow


class UpdaterApp(GuiApp[UpdaterWindow, UpdaterAppController]):
    def __init__(self) -> None:
        # noinspection bad-argument-type
        super().__init__(UpdaterWindow, UpdaterAppController)

        self._set_style()

    def _set_style(self) -> None:
        super()._set_style()

        self.setStyle('fusion')

        palette = self.palette()

        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(*constants.PALETTE_HIGHLIGHT_COLOR))

        self.setPalette(palette)
