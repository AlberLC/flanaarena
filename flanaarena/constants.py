import os
import pathlib
import re
import sys

import requests

APP_NAME = 'FlanaArena'
NORMALIZED_APP_NAME = APP_NAME.lower()
UPDATER_APP_NAME = 'Updater'

CHAMPION_ID_TO_UUID_ENDPOINT = 'https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-parties/global/default/rcp-fe-lol-parties.js'
CHAMPION_IMAGE_ENDPOINT_TEMPLATE = 'https://ddragon.leagueoflegends.com/cdn/{lol_version}/img/champion/{champion_name}.png'
CHAMPIONS_ENDPOINT_TEMPLATE = 'https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'
CHUNK_SIZE = 65536
FLANASERVER_API_HOST = 'flanaserver.duckdns.org'
FLANASERVER_API_HTTP_BASE_URL = f'https://{FLANASERVER_API_HOST}/api'
FLANASERVER_API_DOWNLOAD_ENDPINT = f'{FLANASERVER_API_HTTP_BASE_URL}/{NORMALIZED_APP_NAME}/download'
FLANASERVER_API_VERSION_ENDPINT = f'{FLANASERVER_API_HTTP_BASE_URL}/{NORMALIZED_APP_NAME}/version'
FLANASERVER_API_TIMEOUT = (3, 10)
LCU_BASIC_AUTH_USER = 'riot'
LOADING_GIFS_SIZE = 128
LOL_PROCESS_NAME = 'LeagueClientUx.exe'
LOL_PROCESS_SLEEP = 1
LOL_VERSIONS_ENDPOINT = 'https://ddragon.leagueoflegends.com/api/versions.json'
LAST_LOL_VERSION = requests.get(LOL_VERSIONS_ENDPOINT).json()[0]
CHAMPIONS_ENDPOINT = CHAMPIONS_ENDPOINT_TEMPLATE.format(LAST_LOL_VERSION)
MILLISECONDS_PER_SECOND = 1000
MISSION_RECT_COMPLETE_COLOR = '#969696aa'
MISSION_RECT_INCOMPLETE_COLOR = '#16b816aa'
LCU_HOST = '127.0.0.1'
LCU_ACCEPT_ENDPOINT_TEMPLATE = f'https://{LCU_HOST}:{{}}/lol-matchmaking/v1/ready-check/accept'
LCU_ASSIGNED_CHAMPION_URI = '/lol-chat/v1/me'
LCU_CHAMPION_SELECT_URI_PART = '/lol-champ-select/v1/summoners'
LCU_CHAMPION_SELECTED_URI_PART = '/lol-champ-select/v1/grid-champions'
LCU_CLEAR_BORDERS_ENDPOINT_TEMPLATE = f'https://{LCU_HOST}:{{}}/lol-regalia/v2/current-summoner/regalia'
LCU_CLEAR_BORDERS_PAYLOAD = {
    'preferredCrestType': 'prestige',
    'preferredBannerType': 'blank',
    'selectedPrestigeCrest': None
}
LCU_CLEAR_TOKENS_ENDPOINT_TEMPLATE = f'https://{LCU_HOST}:{{}}/lol-challenges/v1/update-player-preferences'
LCU_CLEAR_TOKENS_PAYLOAD = {'challengeIds': []}
LCU_CURRENT_SEASON_ENDPOINT_TEMPLATE = f'https://{LCU_HOST}:{{}}/lol-seasons/v1/season/name/a'
LCU_GAMEFLOW_PHASE_URI = '/lol-gameflow/v1/gameflow-phase'
LCU_MATCHMAKING_URI = '/lol-lobby-team-builder/v1/matchmaking'  # same as '/lol-gameflow/v1/session' and checking event_data['phase'] == 'ReadyCheck' but several events earlier
LCU_MISSIONS_ENDPOINT_MAX_IDS = 50
LCU_MISSIONS_ENDPOINT_TEMPLATE = f'https://{LCU_HOST}:{{port}}/lol-cap-missions/v1/getmissions?Ids={{ids}}'
LCU_PASSWORD_REGEX_PATTERN = re.compile(r'--remoting-auth-token=(\S+)')
LCU_PORT_REGEX_PATTERN = re.compile(r'--app-port=(\d+)')
LCU_SELECT_CHAMPION_ENDPOINT_TEMPLATE = f'https://{LCU_HOST}:{{port}}/lol-champ-select/v1/session/actions/{{cell_id}}'
LCU_SOCKET_URL_TEMPLATE = f'wss://{LCU_HOST}:{{}}'
LCU_UPDATE_MISSIONS_COUNT_SLEEP = 10
LCU_UPDATED_MISSIONS_URI = '/lol-missions/v1/missions'
LCU_UX_STATE_URI = '/riotclient/ux-state/request'
PALETTE_HIGHLIGHT_COLOR = (79, 114, 195)
RYZE_ID = 13
SEASON_SPLITS = 3
VERSION = '1.1.3'

# Paths
IS_DEVELOPMENT = not getattr(sys, 'frozen', False)
SOURCE_PATH = pathlib.Path(__file__).parent

if IS_DEVELOPMENT:
    DIST_PATH = SOURCE_PATH.parent / 'dist'
else:
    DIST_PATH = SOURCE_PATH.parent.parent.parent

APPS_PATH = DIST_PATH / APP_NAME
APP_PATH = APPS_PATH / APP_NAME
UPDATER_APP_PATH = APPS_PATH / UPDATER_APP_NAME

PYINSTALLER_INTERNAL_NAME = '_internal'

if not IS_DEVELOPMENT:
    os.chdir(DIST_PATH)

APP_EXE_PATH = (APP_PATH / APP_NAME).with_suffix('.exe')
APP_MAIN_PATH = SOURCE_PATH / 'main.py'
UPDATER_APP_EXE_PATH = (UPDATER_APP_PATH / UPDATER_APP_NAME).with_suffix('.exe')
UPDATER_APP_MAIN_PATH = SOURCE_PATH / f'{UPDATER_APP_NAME.lower()}_main.py'

# Resources
RESOURCES_PATH = SOURCE_PATH / 'resources' if IS_DEVELOPMENT else APP_PATH / PYINSTALLER_INTERNAL_NAME / 'resources'
# Images
IMAGES_PATH = RESOURCES_PATH / 'images'
CLOSE_PATH = IMAGES_PATH / 'close.svg'
LOGO_PATH = IMAGES_PATH / 'logo.png'
TICK_PATH = IMAGES_PATH / 'tick.svg'
# Loading gifs
LOADING_GIFS_PATH = RESOURCES_PATH / 'loading_gifs'
# Uis
UIS_PATH = RESOURCES_PATH / 'uis'
APP_UI_PATH = UIS_PATH / 'flanaarena.ui'
UPDATER_APP_UI_PATH = UIS_PATH / 'updater.ui'
# Files
CONFIG_PATH = RESOURCES_PATH / 'config.json'

SAVABLE_PATHS = (CONFIG_PATH,)
