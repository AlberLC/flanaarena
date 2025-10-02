import base64
import json
import random
import ssl
import threading
import time

import requests
import websockets.sync.client

import constants
from models.champion import Champion
from qt.windows import MainWindow
from services import champion_fetcher, lcu


class Controller:
    def __init__(self, window: MainWindow) -> None:
        self._window = window
        self._gui = window.central_widget
        self._champions: dict[int, Champion] = {}
        self._current_champion_id: int | None = None
        self._champions_loaded_event = threading.Event()
        self._lcu_socket_connected_event = threading.Event()

        self._gui.check_auto_accept.toggled.connect(self._save_config)

    def _load_config(self) -> None:
        if not constants.CONFIG_PATH.is_file():
            constants.CONFIG_PATH.write_text('{}')

        config = json.loads(constants.CONFIG_PATH.read_text())

        self._gui.auto_accept = config.get('auto_accept', True)

    def _fetch_champions(self) -> None:
        self._champions = champion_fetcher.fetch_champions()
        self._champions_loaded_event.set()
        self._lcu_socket_connected_event.wait()
        self._gui.loaded_signal.emit()

    def _run_socket_listener(self) -> None:
        port, basic_auth_password = lcu.wait_for_credentials()

        lcu_basic_auth_token = base64.b64encode(
            f'{constants.LCU_BASIC_AUTH_USER}:{basic_auth_password}'.encode()
        ).decode()

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        while True:
            try:
                websocket = websockets.sync.client.connect(
                    constants.LCU_SOCKET_URL_TEMPLATE.format(port),
                    ssl=ssl_context,
                    additional_headers={'Authorization': f'Basic {lcu_basic_auth_token}'},
                    max_size=None
                )
            except (ConnectionRefusedError, websockets.exceptions.InvalidStatus):
                time.sleep(constants.LOL_PROCESS_SLEEP)
            else:
                break

        websocket.send(json.dumps([5, 'OnJsonApiEvent']))  # Based on other libraries
        websocket.recv()
        self._lcu_socket_connected_event.set()

        while True:
            try:
                message = websocket.recv()
            except websockets.exceptions.ConnectionClosedError:
                self._gui.close_signal.emit()
                break

            message_data = json.loads(message)[2]
            event_data = message_data['data']
            event_type = message_data['eventType']
            uri = message_data['uri']

            if constants.LCU_CHAMPION_SELECTED_URI_PART in uri:
                if event_data and event_data['selectionStatus']['selectedByMe']:
                    self._update_champion(event_data['id'])
            elif uri == constants.LCU_UX_STATE_URI:
                if event_data and event_data['state'] == 'ShowMain':
                    self._window.force_foreground()
            elif uri == constants.LCU_GAMEFLOW_PHASE_URI:
                if event_data == 'ChampSelect':
                    self._window.force_foreground()
            elif uri == constants.LCU_UPDATED_MISSIONS_URI:
                if event_type == 'Update':
                    self._update_missions_count()
            elif uri == constants.LCU_ASSIGNED_CHAMPION_URI:
                if event_data and (lol_data := event_data.get('lol')) and (champion_id := lol_data['championId']):
                    self._update_champion(int(champion_id))
            elif uri == constants.LCU_MATCHMAKING_URI:
                if (
                    self._gui.auto_accept
                    and
                    event_data
                    and
                    event_data.get('searchState') == 'Found'
                    and
                    (ready_check_data := event_data.get('readyCheck'))
                    and
                    not ready_check_data['autoAccept']
                    and
                    ready_check_data['state'] == 'InProgress'
                ):
                    lcu.accept_game()

    @staticmethod
    def _save_config(state: bool) -> None:
        constants.CONFIG_PATH.write_text(json.dumps({'auto_accept': state}))

    def _update_champion(self, champion_id: int) -> None:
        self._current_champion_id = champion_id
        self._gui.update_signal.emit(self._champions[champion_id])

    def _update_missions_count(self) -> None:
        # Socket messages jsut before missions update
        # [8,"OnJsonApiEvent",{"data":{"ackRequired":false,"id":"","payload":"{\"version\":362,\"updatedGroups\":[\"a0ed106f-a444-4263-9b6a-f8d0adb9564d\"]}","resource":"cap/progression/v1/notifications/cache/invalidate","service":"cap.progression","timestamp":1758674837048,"version":"1.0"},"eventType":"Create","uri":"/riot-messaging-service/v1/message/cap/progression/v1/notifications/cache/invalidate"}]
        # [8,"OnJsonApiEvent",{"data":{"payload":"{\"deltaEventId\":\"04dd8cd0-98e0-11f0-8ef4-b0e153d01caa\",\"ownerId\":\"198b92e9-a8bc-53e5-82f4-289ca9847eb9\",\"namespace\":\"\",\"updatedMissions\":[\"65304025-c57b-405b-b2ff-95667c6258e1\",\"aa23565b-e1eb-43fe-92f4-62bea88a35d8\"]}","resource":"cap/missions/v1/notifications","service":"cap.missions","timestamp":1758674837055,"version":"1.0.0"},"eventType":"Update","uri":"/lol-cap-missions/v1/invalidatecache"}]
        # [8,"OnJsonApiEvent",{"data":{"ackRequired":false,"id":"","payload":"{\"deltaEventId\":\"04dd8cd0-98e0-11f0-8ef4-b0e153d01caa\",\"ownerId\":\"198b92e9-a8bc-53e5-82f4-289ca9847eb9\",\"namespace\":\"\",\"updatedMissions\":[\"65304025-c57b-405b-b2ff-95667c6258e1\",\"aa23565b-e1eb-43fe-92f4-62bea88a35d8\"]}","resource":"cap/missions/v1/notifications","service":"cap.missions","timestamp":1758674837055,"version":"1.0.0"},"eventType":"Create","uri":"/riot-messaging-service/v1/message/cap/missions/v1/notifications"}]
        # [8,"OnJsonApiEvent",{"data":[],"eventType":"Update","uri":"/lol-missions/v1/missions"}]
        # [8,"OnJsonApiEvent",{"data":[],"eventType":"Update","uri":"/lol-npe-tutorial-path/v1/tutorials"}]
        # [8,"OnJsonApiEvent",{"data":[],"eventType":"Update","uri":"/lol-event-mission/v1/event-mission"}]
        # [8,"OnJsonApiEvent",{"data":{"counters":[{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","counterValue":45400,"groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22"}],"groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","milestones":[{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"85e56ece-800c-4342-9628-18f4981751f9","milestoneId":"51f79a8c-e7b6-498c-8f5f-bf7c3b9ac342","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":100,"triggered":true,"triggeredTimestamp":"2025-08-30T00:16:16.118556379Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"c2657645-2a4b-42d9-83e3-044491f1dd12","milestoneId":"a74066e1-88a3-4888-8384-6cdcc4bd518f","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":1600,"triggered":true,"triggeredTimestamp":"2025-09-01T01:21:04.283521927Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"4bde074c-b01a-4c8d-b9f0-70c92a5fca00","milestoneId":"535e2217-6a79-4373-a906-d2ad93362cf7","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":3600,"triggered":true,"triggeredTimestamp":"2025-09-01T20:47:45.245349932Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"8a9688c3-4e35-4c4f-bc2d-01759d6269cd","milestoneId":"635265cf-81db-4516-b004-a297ade967bd","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":6100,"triggered":true,"triggeredTimestamp":"2025-09-02T02:09:51.388406720Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"817a06ec-7f3d-4e51-88d3-6578eb26365b","milestoneId":"99cb8007-48d4-4e9c-b012-205d75765ffe","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":9100,"triggered":true,"triggeredTimestamp":"2025-09-04T02:53:20.787205145Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"0de06f98-a835-4985-ab6a-21d7bb6fe252","milestoneId":"c124ede6-007b-4a92-b80b-cba2ba7a41d9","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":12600,"triggered":true,"triggeredTimestamp":"2025-09-05T02:52:19.586230534Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"cf6237d9-7bea-4d44-9e12-b8d92b6addfd","milestoneId":"e319ae0e-50a1-4c4b-b16a-59c1ef582fa2","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":16600,"triggered":true,"triggeredTimestamp":"2025-09-07T03:20:37.348550586Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"7a1f2e97-9a64-4e50-b999-ed13d7b159b3","milestoneId":"9fa631ad-d7f6-48b0-854a-18a3b9b42d87","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":21100,"triggered":true,"triggeredTimestamp":"2025-09-09T07:46:03.708291775Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"0ba95efd-3930-446d-a026-523f9c854866","milestoneId":"c5b0e342-a476-4d30-bf6b-68e9ef0de3b3","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":26100,"triggered":true,"triggeredTimestamp":"2025-09-12T06:56:54.130595425Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"d0699f8e-d673-433f-b277-3e82fd555ca1","milestoneId":"7cb59c8a-bc1a-4e3e-89a1-8b537279cd44","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":31600,"triggered":true,"triggeredTimestamp":"2025-09-17T03:25:25.573290608Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"aadef18a-31bd-4bfe-8b06-2d35fe2037d2","milestoneId":"41ee393b-05b8-4e03-9c3c-e4356d97759f","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":37600,"triggered":true,"triggeredTimestamp":"2025-09-22T01:52:01.043083263Z","triggers":[]},{"counterId":"493b96e8-41e5-4a43-be79-21136cbe2853","groupId":"a0ed106f-a444-4263-9b6a-f8d0adb9564d","instanceId":"","milestoneId":"9d9bc47a-8fee-4e27-aaeb-bc355c52c16d","ownerId":"198b92e9-a8bc-53e5-82f4-289ca9847eb9","productId":"d1c2664a-5938-4c41-8d1b-61fd51052c22","repeatSequence":0,"triggerValue":47600,"triggered":false,"triggeredTimestamp":"","triggers":[]}]},"eventType":"Update","uri":"/lol-progression/v1/groups/a0ed106f-a444-4263-9b6a-f8d0adb9564d/instanceData"}]

        self._champions_loaded_event.wait()
        self._lcu_socket_connected_event.wait()

        while True:
            try:
                missions_count = lcu.fetch_missions_count()
            except requests.exceptions.ConnectionError:
                pass
            else:
                for champion_id, champion_missions_count in missions_count.items():
                    self._champions[champion_id].missions_count = champion_missions_count

                if self._current_champion_id:
                    self._update_champion(self._current_champion_id)

                break

            time.sleep(constants.LCU_UPDATE_MISSIONS_COUNT_SLEEP)

    def load(self) -> None:
        threading.Thread(target=self._fetch_champions, daemon=True).start()
        threading.Thread(target=self._run_socket_listener, daemon=True).start()
        threading.Thread(target=self._update_missions_count, daemon=True).start()

        self._load_config()
        self._gui.set_loading_movie(random.choice(tuple(constants.LOADING_GIFS_PATH.iterdir())))
