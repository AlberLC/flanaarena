import itertools
import json
import threading
import time

import psutil
import requests

import constants

_basic_auth_password: str | None = None
_credentials_lock = threading.Lock()
_port: int | None = None


def accept_game() -> None:
    port, basic_auth_password = wait_for_league_credentials()
    requests.post(
        constants.LCU_ACCEPT_ENDPOINT_TEMPLATE.format(port),
        auth=(constants.LCU_BASIC_AUTH_USER, basic_auth_password),
        verify=False
    )


def fetch_missions_count() -> dict[int, int]:
    port, basic_auth_password = wait_for_league_credentials()

    missions_count = {}

    champion_uuid_batches = itertools.batched(
        constants.CHAMPION_ID_UUID_BIDICT.values(),
        constants.LCU_MISSIONS_ENDPOINT_MAX_IDS
    )
    for champion_uuids in champion_uuid_batches:
        response = requests.get(
            constants.LCU_MISSIONS_ENDPOINT_TEMPLATE.format(port=port, ids=json.dumps(champion_uuids)),
            auth=(constants.LCU_BASIC_AUTH_USER, basic_auth_password),
            verify=False
        )

        try:
            missions_data = response.json()['series']
        except KeyError:
            return missions_count

        for champion_missions_data in missions_data:
            champion_id = constants.CHAMPION_ID_UUID_BIDICT.inverse[champion_missions_data['configurationId']]

            mission_count = 0
            for champion_mission_data in champion_missions_data['missions']:
                if champion_mission_data['status'] == 'COMPLETED':
                    mission_count += 1

            missions_count[champion_id] = mission_count

    return missions_count


def wait_for_league_credentials() -> tuple[int, str]:
    global _basic_auth_password, _port

    with _credentials_lock:
        if not _basic_auth_password:
            while True:
                for proc in psutil.process_iter(['name', 'cmdline']):
                    if proc.info['name'] == constants.LOL_PROCESS_NAME:
                        cmdline = ' '.join(proc.info['cmdline'])
                        break
                else:
                    time.sleep(constants.LOL_PROCESS_SLEEP)
                    continue
                break

            _basic_auth_password = constants.LCU_PASSWORD_REGEX_PATTERN.search(cmdline).group(1)
            _port = constants.LCU_PORT_REGEX_PATTERN.search(cmdline).group(1)

    return _port, _basic_auth_password
