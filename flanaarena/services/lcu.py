import ast
import base64
import itertools
import json
import re
import ssl
import time
from collections.abc import Generator, Sequence
from typing import Any

import requests
import websockets.sync.client
from bidict import bidict

import constants
from utils import system


class Lcu:
    def __init__(self, session: requests.Session) -> None:
        self._session = session
        self._basic_auth_password = ''
        self._port = ''
        self._auth_session = requests.Session()
        self._websocket: websockets.sync.client.ClientConnection | None = None
        self._champion_id_uuid_bidict: bidict[int, str] = bidict()

    def _fetch_champion_id_uuid_bidict(self) -> bidict[int, str]:
        js = self._session.get(constants.CHAMPION_ID_TO_UUID_ENDPOINT).text
        matched_mappings = re.findall(r'ChampionIdToSeriesUuidMapping\s*=\s*({.*?})},', js)
        mapping_index = min(self._get_current_season_split() - 1, len(matched_mappings) - 1)

        return bidict(ast.literal_eval(matched_mappings[mapping_index]))

    def _get_current_season_split(self) -> int:
        current_season_data = self._auth_session.get(
            constants.LCU_CURRENT_SEASON_ENDPOINT_TEMPLATE.format(self._port)
        ).json()
        current_split = current_season_data['metadata']['currentSplit']

        if time.time() * constants.MILLISECONDS_PER_SECOND <= current_season_data['seasonEnd']:
            return current_split
        else:
            return current_split % constants.SEASON_SPLITS + 1

    def _get_missions_data(self, champion_uuids: Sequence[str]) -> list[dict]:
        missions_data = []

        response = self._auth_session.get(
            constants.LCU_MISSIONS_ENDPOINT_TEMPLATE.format(port=self._port, ids=json.dumps(champion_uuids))
        )

        try:
            missions_data = response.json()['series']
        except KeyError:
            pass

        return missions_data

    @staticmethod
    def _wait_for_credentials() -> tuple[str, str]:
        while not (processes := system.search_processes(constants.LOL_PROCESS_NAME)):
            time.sleep(constants.LOL_PROCESS_SLEEP)

        cmdline = ' '.join(processes[0].info['cmdline'])
        basic_auth_password = constants.LCU_PASSWORD_REGEX_PATTERN.search(cmdline).group(1)
        port = constants.LCU_PORT_REGEX_PATTERN.search(cmdline).group(1)

        return basic_auth_password, port

    def accept_game(self) -> None:
        self._auth_session.post(constants.LCU_ACCEPT_ENDPOINT_TEMPLATE.format(self._port))

    def clear_borders(self) -> None:
        self._auth_session.put(
            constants.LCU_CLEAR_BORDERS_ENDPOINT_TEMPLATE.format(self._port),
            json=constants.LCU_CLEAR_BORDERS_PAYLOAD
        )

    def clear_tokens(self) -> None:
        self._auth_session.post(
            constants.LCU_CLEAR_TOKENS_ENDPOINT_TEMPLATE.format(self._port),
            json=constants.LCU_CLEAR_TOKENS_PAYLOAD
        )

    def connect_websocket(self) -> None:
        lcu_basic_auth_token = base64.b64encode(
            f'{constants.LCU_BASIC_AUTH_USER}:{self._basic_auth_password}'.encode()
        ).decode()

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        while True:
            try:
                self._websocket = websockets.sync.client.connect(
                    constants.LCU_SOCKET_URL_TEMPLATE.format(self._port),
                    ssl=ssl_context,
                    additional_headers={'Authorization': f'Basic {lcu_basic_auth_token}'},
                    max_size=None
                )
            except (ConnectionRefusedError, websockets.exceptions.InvalidStatus):
                time.sleep(constants.LOL_PROCESS_SLEEP)
            else:
                break

        # noinspection unresolved-references
        self._websocket.send(json.dumps([5, 'OnJsonApiEvent']))  # Based on other libraries
        # noinspection unresolved-references
        self._websocket.recv()

    def fetch_missions_count(self) -> dict[int, int]:
        if not self._champion_id_uuid_bidict:
            self._champion_id_uuid_bidict = self._fetch_champion_id_uuid_bidict()

        missions_count = {}

        champion_uuid_batches = itertools.batched(
            self._champion_id_uuid_bidict.values(),
            constants.LCU_MISSIONS_ENDPOINT_MAX_IDS
        )
        for champion_uuids in champion_uuid_batches:
            for champion_missions_data in self._get_missions_data(champion_uuids):
                mission_count = 0

                for champion_mission_data in champion_missions_data['missions']:
                    if champion_mission_data['status'] == 'COMPLETED':
                        mission_count += 1

                champion_id = self._champion_id_uuid_bidict.inverse[champion_missions_data['configurationId']]
                missions_count[champion_id] = mission_count

        return missions_count

    def iter_websocket_events(self) -> Generator[tuple[Any, str, str]]:
        assert self._websocket

        while True:
            try:
                message = self._websocket.recv()
            except websockets.exceptions.ConnectionClosedError:
                break

            try:
                message_data = json.loads(message)[2]
            except json.decoder.JSONDecodeError:
                continue

            yield message_data['data'], message_data['eventType'], message_data['uri']

    def load_credentials(self) -> None:
        self._basic_auth_password, self._port = self._wait_for_credentials()
        self._auth_session.auth = (constants.LCU_BASIC_AUTH_USER, self._basic_auth_password)
        self._auth_session.verify = False

    def select_champion(self, cell_id: int, champion_id: int) -> None:
        self._auth_session.patch(
            constants.LCU_SELECT_CHAMPION_ENDPOINT_TEMPLATE.format(port=self._port, cell_id=cell_id),
            json={'championId': champion_id}
        )
