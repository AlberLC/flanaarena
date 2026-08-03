import subprocess
import sys
import threading
from http import HTTPStatus
from pathlib import Path

import packaging.version
import requests

import constants
from models.enums import UpdateState
from utils import system


def _launch(main_path: str | Path, exe_path: str | Path) -> None:
    if constants.IS_DEVELOPMENT:
        subprocess.Popen((sys.executable, main_path))
    else:
        subprocess.Popen(exe_path)


def check_update_state(session: requests.Session) -> UpdateState:
    try:
        response = session.get(constants.FLANASERVER_API_VERSION_ENDPINT, timeout=constants.FLANASERVER_API_TIMEOUT)
    except (requests.ConnectionError, requests.Timeout):
        return UpdateState.UNKNOWN

    if response.status_code != HTTPStatus.OK:
        return UpdateState.UNKNOWN

    if packaging.version.parse(response.text) > packaging.version.parse(constants.VERSION):
        return UpdateState.OUTDATED
    else:
        return UpdateState.UPDATED


def ensure_updated(session: requests.Session) -> bool:
    if check_update_state(session) is UpdateState.OUTDATED:
        launch_updater()
        return False

    threading.Thread(target=replace_temporary_updater, daemon=True).start()

    return True


def launch_app() -> None:
    _launch(constants.APP_MAIN_PATH, constants.APP_EXE_PATH)


def launch_updater() -> None:
    _launch(constants.UPDATER_APP_MAIN_PATH, constants.UPDATER_APP_EXE_PATH)


def replace_temporary_updater() -> None:
    if not (temporary_path := Path(f'{constants.UPDATER_APP_PATH}_')).exists():
        return

    final_path = temporary_path.with_name(constants.UPDATER_APP_NAME)
    system.delete_recently_active_directory(final_path)
    temporary_path.rename(final_path)
