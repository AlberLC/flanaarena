import io
import shutil
import threading
import zipfile

import requests
from PySide6 import QtGui

import constants
from exceptions import UpdateDownloadError
from qt.apps.bases import GuiApp
from qt.windows.updater_window import UpdaterWindow
from services import update
from utils import system


class UpdaterApp(GuiApp[UpdaterWindow]):
    # noinspection PyArgumentList
    def __init__(self) -> None:
        super().__init__(UpdaterWindow)

        self.setStyle('fusion')

        palette = self.palette()

        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(*constants.PALETTE_HIGHLIGHT_COLOR))

        self.setPalette(palette)

    @staticmethod
    def _clean_old_files() -> None:
        system.delete_recently_active_directory(constants.APP_PATH)

        for path in constants.APPS_PATH.iterdir():
            if path.is_dir():
                if path.name != constants.UPDATER_APP_NAME:
                    shutil.rmtree(path)
            else:
                path.unlink()

    def _download(self) -> io.BytesIO:
        self.gui.state_signal.emit('Descargando actualizaciones...')

        try:
            response = requests.get(
                constants.FLANASERVER_API_DOWNLOAD_ENDPINT,
                stream=True,
                timeout=constants.FLANASERVER_API_TIMEOUT
            )
        except (requests.ConnectionError, requests.Timeout):
            raise UpdateDownloadError

        if not response.ok:
            raise UpdateDownloadError

        content_length = int(response.headers['content-length'])

        buffer = io.BytesIO()
        downloaded = 0

        for chunk in response.iter_content(chunk_size=constants.CHUNK_SIZE):
            buffer.write(chunk)
            downloaded += len(chunk)
            self.gui.progress_signal.emit(downloaded / content_length)

        return buffer

    def _install(self, buffer: io.BytesIO) -> None:
        self.gui.progress_signal.emit(0)
        self.gui.state_signal.emit('Instalando actualizaciones...')

        savable_data = system.read_savable_files(constants.SAVABLE_PATHS)
        self._clean_old_files()

        temporary_path = constants.APPS_PATH / '_'
        temporary_apps_path = temporary_path / constants.APP_NAME

        with zipfile.ZipFile(buffer) as zip_file:
            zip_infos = zip_file.infolist()

            for i, zip_info in enumerate(zip_infos, start=1):
                zip_file.extract(zip_info, temporary_path)
                self.gui.progress_signal.emit(i / len(zip_infos))

        (temporary_apps_path / constants.APP_NAME).move(constants.APP_PATH)
        (temporary_apps_path / constants.UPDATER_APP_NAME).move(
            constants.UPDATER_APP_PATH.with_name(f'{constants.UPDATER_APP_NAME}_')
        )
        shutil.rmtree(temporary_path)

        system.write_savable_files(savable_data)

        update.launch_app()
        self.close_signal.emit()

    def _update(self) -> None:
        self._install(self._download())

    def update(self) -> None:
        threading.Thread(target=self._update, daemon=True).start()
