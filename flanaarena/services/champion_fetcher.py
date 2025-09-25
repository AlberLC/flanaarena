import requests

import constants
from models.champion import Champion


def fetch_champions() -> dict[int, Champion]:
    session = requests.Session()

    champions = {}
    for champion_data in fetch_champions_data().values():
        id = int(champion_data['key'])
        name = champion_data['id']
        champions[id] = Champion(
            id,
            name,
            session.get(
                constants.CHAMPION_IMAGE_ENDPOINT_TEMPLATE.format(
                    lol_version=constants.LAST_LOL_VERSION,
                    champion_name=name
                )
            ).content
        )

    return champions


def fetch_champions_data() -> dict[str, dict]:
    return requests.get(constants.CHAMPIONS_ENDPOINT).json()['data']
