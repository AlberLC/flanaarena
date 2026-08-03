import requests
import urllib3

from qt.apps.app import App
from services import update


def main() -> None:
    with requests.Session() as session:
        if not update.ensure_updated(session):
            return

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        App(session).exec()


if __name__ == '__main__':
    main()
