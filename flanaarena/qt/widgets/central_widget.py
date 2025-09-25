import pathlib

from PySide6 import QtCore, QtGui, QtWidgets

import constants
from models.champion import Champion
from qt.widgets.ui_widget import UiWidget
from utils import visuals


class CentralWidget(UiWidget):
    label_image: QtWidgets.QLabel
    label_name: QtWidgets.QLabel

    check_auto_accept: QtWidgets.QCheckBox

    loaded_signal = QtCore.Signal()
    update_signal = QtCore.Signal(object)
    close_signal = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(constants.UI_PATH, parent=parent)
        self._loading_movie = QtGui.QMovie()

        self._loading_movie.frameChanged.connect(self._update_movie_frame)
        self.loaded_signal.connect(self._clear_loading_movie)
        self.update_signal.connect(self._update_champion)
        self.close_signal.connect(self.window().close)

    def _clear_loading_movie(self) -> None:
        self._loading_movie.stop()
        self.label_image.clear()

    def _update_champion(self, champion: Champion) -> None:
        image = QtGui.QPixmap()
        image.loadFromData(champion.image)
        visuals.draw_mission_indicators(image, champion.missions_count)
        self.label_image.setPixmap(image)

        self.label_name.setText(champion.name)

        self.window().resize(0, 0)

    def _update_movie_frame(self) -> None:
        self.label_image.setPixmap(
            self._loading_movie.currentPixmap().scaled(
                constants.LOADING_GIFS_SIZE,
                constants.LOADING_GIFS_SIZE,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation
            )
        )

    @property
    def auto_accept(self) -> bool:
        return self.check_auto_accept.isChecked()

    @auto_accept.setter
    def auto_accept(self, state: bool) -> None:
        self.check_auto_accept.setChecked(state)

    def set_loading_movie(self, gif: str | pathlib.Path) -> None:
        self._loading_movie.setFileName(str(gif))
        self.label_image.setMovie(self._loading_movie)
        self.window().resize(0, 0)
        self._loading_movie.start()
