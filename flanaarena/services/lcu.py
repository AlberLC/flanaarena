import ast
import itertools
import json
import re
import threading
import time
from collections.abc import Sequence
from typing import Any

import requests
from bidict import bidict

import constants
from utils import system


def _get_champion_id_uuid_bidict() -> bidict[int, str] | None:
    global _champion_id_uuid_bidict

    with _champion_id_uuid_bidict_lock:
        if _champion_id_uuid_bidict:
            return _champion_id_uuid_bidict

        js = requests.get(constants.CHAMPION_ID_TO_UUID_ENDPOINT).text
        matched_mappings = re.findall(r'ChampionIdToSeriesUuidMapping\s*=\s*({.*?})},', js)
        mapping_index = min(_get_current_season_split() - 1, len(matched_mappings) - 1)
        _champion_id_uuid_bidict = bidict(ast.literal_eval(matched_mappings[mapping_index]))

    return _champion_id_uuid_bidict


def _get_current_season_data() -> dict[str, Any]:
    basic_auth_password, port = wait_for_credentials()

    return requests.get(
        constants.LCU_CURRENT_SEASON_ENDPOINT_TEMPLATE.format(port),
        auth=(constants.LCU_BASIC_AUTH_USER, basic_auth_password),
        verify=False
    ).json()


def _get_current_season_split() -> int:
    current_season_data = _get_current_season_data()
    current_split = current_season_data['metadata']['currentSplit']

    if time.time() * constants.MILLISECONDS_PER_SECOND <= current_season_data['seasonEnd']:
        return current_split
    else:
        return current_split % constants.SEASON_SPLITS + 1


def _get_missions_data(champion_uuids: Sequence[str]) -> list[dict]:
    missions_data = []

    basic_auth_password, port = wait_for_credentials()

    response = requests.get(
        constants.LCU_MISSIONS_ENDPOINT_TEMPLATE.format(port=port, ids=json.dumps(champion_uuids)),
        auth=(constants.LCU_BASIC_AUTH_USER, basic_auth_password),
        verify=False
    )

    try:
        missions_data = response.json()['series']
    except KeyError:
        pass

    return missions_data


def accept_game() -> None:
    basic_auth_password, port = wait_for_credentials()
    requests.post(
        constants.LCU_ACCEPT_ENDPOINT_TEMPLATE.format(port),
        auth=(constants.LCU_BASIC_AUTH_USER, basic_auth_password),
        verify=False
    )


def clear_borders() -> None:
    basic_auth_password, port = wait_for_credentials()
    requests.put(
        constants.LCU_CLEAR_BORDERS_ENDPOINT_TEMPLATE.format(port),
        json=constants.LCU_CLEAR_BORDERS_PAYLOAD,
        auth=(constants.LCU_BASIC_AUTH_USER, basic_auth_password),
        verify=False
    )


def clear_tokens() -> None:
    basic_auth_password, port = wait_for_credentials()
    requests.post(
        constants.LCU_CLEAR_TOKENS_ENDPOINT_TEMPLATE.format(port),
        json=constants.LCU_CLEAR_TOKENS_PAYLOAD,
        auth=(constants.LCU_BASIC_AUTH_USER, basic_auth_password),
        verify=False
    )


def fetch_missions_count() -> dict[int, int]:
    missions_count = {}

    if not (champion_id_uuid_bidict := _get_champion_id_uuid_bidict()):
        return missions_count

    champion_uuid_batches = itertools.batched(champion_id_uuid_bidict.values(), constants.LCU_MISSIONS_ENDPOINT_MAX_IDS)
    for champion_uuids in champion_uuid_batches:
        for champion_missions_data in _get_missions_data(champion_uuids):
            mission_count = 0

            for champion_mission_data in champion_missions_data['missions']:
                if champion_mission_data['status'] == 'COMPLETED':
                    mission_count += 1

            champion_id = champion_id_uuid_bidict.inverse[champion_missions_data['configurationId']]
            missions_count[champion_id] = mission_count

    return missions_count


def select_champion(cell_id: int, champion_id: int) -> None:
    basic_auth_password, port = wait_for_credentials()
    requests.patch(
        constants.LCU_SELECT_CHAMPION_ENDPOINT_TEMPLATE.format(port=port, cell_id=cell_id),
        json={'championId': champion_id},
        auth=(constants.LCU_BASIC_AUTH_USER, basic_auth_password),
        verify=False
    )


def wait_for_credentials() -> tuple[str, int]:
    global _basic_auth_password, _port

    with _credentials_lock:
        if _basic_auth_password:
            return _basic_auth_password, _port

        while not (processes := system.search_processes(constants.LOL_PROCESS_NAME)):
            time.sleep(constants.LOL_PROCESS_SLEEP)

        cmdline = ' '.join(processes[0].info['cmdline'])
        _basic_auth_password = constants.LCU_PASSWORD_REGEX_PATTERN.search(cmdline).group(1)
        _port = constants.LCU_PORT_REGEX_PATTERN.search(cmdline).group(1)

    return _basic_auth_password, _port


_basic_auth_password: str | None = None
_champion_id_uuid_bidict: bidict[int, str] | None = None
_champion_id_uuid_bidict_lock = threading.Lock()
_credentials_lock = threading.Lock()
_port: int | None = None
