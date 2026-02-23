import urllib3

from qt.apps.app import App
from services import update


def main() -> None:
    if not update.ensure_updated():
        return

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    App().exec()


if __name__ == '__main__':
    main()
