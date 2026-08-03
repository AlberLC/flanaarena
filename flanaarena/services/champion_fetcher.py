import requests

import constants
from models.champion import Champion


def fetch_champions(session: requests.Session) -> dict[int, Champion]:
    champions = {}

    for champion_data in session.get(constants.CHAMPIONS_ENDPOINT).json()['data'].values():
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
