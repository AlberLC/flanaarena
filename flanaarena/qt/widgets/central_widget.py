import pathlib

from PySide6 import QtCore, QtGui, QtWidgets

import constants
from models.champion import Champion
from qt.widgets.ui_widget import UiWidget
from utils import visuals


class CentralWidget(UiWidget):
    label_image: QtWidgets.QLabel
    label_name: QtWidgets.QLabel

    button_profile: QtWidgets.QToolButton

    check_auto_accept: QtWidgets.QCheckBox

    horizontal_line_1: QtWidgets.QFrame
    horizontal_line_2: QtWidgets.QFrame

    show_profile_widgets_signal = QtCore.Signal()
    loaded_signal = QtCore.Signal()
    set_champion_signal = QtCore.Signal(object)
    close_signal = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(constants.UI_PATH, parent=parent)
        self._loading_movie = QtGui.QMovie()
        self._profile_menu = QtWidgets.QMenu(self.button_profile)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.clear_borders_action = QtGui.QAction('Quitar bordes', self._profile_menu, font=font)
        self.clear_tokens_action = QtGui.QAction('Quitar símbolos', self._profile_menu, font=font)

        self._profile_menu.addAction(self.clear_borders_action)
        self._profile_menu.addAction(self.clear_tokens_action)
        self.button_profile.setMenu(self._profile_menu)
        self.label_name.hide()
        self._show_profile_widgets(False)

        self._loading_movie.frameChanged.connect(self._update_movie_frame)
        self.show_profile_widgets_signal.connect(lambda: self._show_profile_widgets(True))
        self.loaded_signal.connect(self._on_loaded)
        self.set_champion_signal.connect(self._set_champion)
        self.close_signal.connect(self.window().close)

    def _on_loaded(self) -> None:
        self._loading_movie.stop()
        self.label_image.clear()
        self.label_name.show()

    def _set_champion(self, champion: Champion) -> None:
        image = QtGui.QPixmap()
        image.loadFromData(champion.image)
        visuals.draw_mission_indicators(image, champion.missions_count)
        self.label_image.setPixmap(image)

        self.label_name.setText(champion.name)

        self.window().resize(0, 0)

    def _show_profile_widgets(self, visible: bool) -> None:
        self.horizontal_line_2.setVisible(visible)
        self.button_profile.setVisible(visible)

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
