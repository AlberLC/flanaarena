import ast
import os
import pathlib
import re
import sys

import requests
from bidict import bidict


def get_champion_id_uuid_bidict() -> bidict[int, str] | None:
    js = requests.get(CHAMPION_ID_TO_UUID_ENDPOINT).text

    matches = re.findall(r'ChampionIdToSeriesUuidMapping\s*=\s*({.*?})},', js)

    if matches:
        js_object_text = matches[-1]
        return bidict(ast.literal_eval(js_object_text))


APP_NAME = 'FlanaArena'
CHAMPION_ID_TO_UUID_ENDPOINT = 'https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-parties/global/default/rcp-fe-lol-parties.js'
CHAMPION_ID_UUID_BIDICT = get_champion_id_uuid_bidict()
CHAMPION_IMAGE_ENDPOINT_TEMPLATE = 'https://ddragon.leagueoflegends.com/cdn/{lol_version}/img/champion/{champion_name}.png'
CHAMPIONS_ENDPOINT_TEMPLATE = 'https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'
LCU_BASIC_AUTH_USER = 'riot'
LOADING_GIFS_SIZE = 128
LOL_PROCESS_NAME = 'LeagueClientUx.exe'
LOL_PROCESS_SLEEP = 1
LOL_VERSIONS_ENDPOINT = 'https://ddragon.leagueoflegends.com/api/versions.json'
LAST_LOL_VERSION = requests.get(LOL_VERSIONS_ENDPOINT).json()[0]
CHAMPIONS_ENDPOINT = CHAMPIONS_ENDPOINT_TEMPLATE.format(LAST_LOL_VERSION)
MISSION_RECT_COMPLETE_COLOR = '#969696aa'
MISSION_RECT_INCOMPLETE_COLOR = '#16b816aa'
LCU_HOST = '127.0.0.1'
LCU_ACCEPT_ENDPOINT_TEMPLATE = f'https://{LCU_HOST}:{{}}/lol-matchmaking/v1/ready-check/accept'
LCU_ASSIGNED_CHAMPION_URI = '/lol-chat/v1/me'
LCU_CHAMPION_SELECTED_URI_PART = '/lol-champ-select/v1/grid-champions'
LCU_CLEAR_BORDERS_ENDPOINT_TEMPLATE = f'https://{LCU_HOST}:{{}}/lol-regalia/v2/current-summoner/regalia'
LCU_CLEAR_BORDERS_PAYLOAD = {
    'preferredCrestType': 'prestige',
    'preferredBannerType': 'blank',
    'selectedPrestigeCrest': None
}
LCU_CLEAR_TOKENS_ENDPOINT_TEMPLATE = f'https://{LCU_HOST}:{{}}/lol-challenges/v1/update-player-preferences'
LCU_CLEAR_TOKENS_PAYLOAD = {'challengeIds': []}
LCU_GAMEFLOW_PHASE_URI = '/lol-gameflow/v1/gameflow-phase'
LCU_MATCHMAKING_URI = '/lol-lobby-team-builder/v1/matchmaking'
LCU_MISSIONS_ENDPOINT_MAX_IDS = 50
LCU_MISSIONS_ENDPOINT_TEMPLATE = f'https://{LCU_HOST}:{{port}}/lol-cap-missions/v1/getmissions?Ids={{ids}}'
LCU_PASSWORD_REGEX_PATTERN = re.compile(r'--remoting-auth-token=(\S+)')
LCU_PORT_REGEX_PATTERN = re.compile(r'--app-port=(\d+)')
LCU_SOCKET_URL_TEMPLATE = f'wss://{LCU_HOST}:{{}}'
LCU_UPDATE_MISSIONS_COUNT_SLEEP = 10
LCU_UPDATED_MISSIONS_URI = '/lol-missions/v1/missions'
LCU_UX_STATE_URI = '/riotclient/ux-state/request'

# Paths
IS_DEVELOPMENT = not getattr(sys, 'frozen', False) or not hasattr(sys, '_MEIPASS')

PYTHON_SOURCE_PATH = pathlib.Path(__file__).parent.resolve()
WORKING_DIRECTORY_PATH = PYTHON_SOURCE_PATH if IS_DEVELOPMENT else PYTHON_SOURCE_PATH.parent
if not IS_DEVELOPMENT:
    os.chdir(WORKING_DIRECTORY_PATH)
DIST_PATH = WORKING_DIRECTORY_PATH.parent / 'dist' if IS_DEVELOPMENT else WORKING_DIRECTORY_PATH.parent

# Resources
RESOURCES_PATH = PYTHON_SOURCE_PATH / 'resources'
CONFIG_PATH = RESOURCES_PATH / 'config.json'

# Images
IMAGES_PATH = RESOURCES_PATH / 'images'
LOGO_PATH = IMAGES_PATH / 'logo.png'
TICK_PATH = IMAGES_PATH / 'tick.svg'

# Loading gifs
LOADING_GIFS_PATH = RESOURCES_PATH / 'loading_gifs'

# Uis
UIS_PATH = RESOURCES_PATH / 'uis'
UI_PATH = UIS_PATH / 'flanaarena.ui'
