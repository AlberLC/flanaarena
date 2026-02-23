import pathlib
from collections.abc import Iterable

from PySide6 import QtCore, QtWidgets

from qt import ui_loader


class UiWidget(QtWidgets.QWidget):
    def __init__(
        self,
        ui_path: str | pathlib.Path,
        custom_widgets: Iterable[type[QtWidgets.QWidget]] = (),
        parent: QtCore.QObject | None = None
    ) -> None:
        super().__init__(parent)
        ui_loader.UiLoader(self, custom_widgets).load(pathlib.Path(ui_path))
