import requests

from qt.apps.bases import GuiApp
from qt.controllers.app_controller import AppController
from qt.windows.app_window import AppWindow


class App(GuiApp[AppWindow, AppController]):
    def __init__(self, session: requests.Session) -> None:
        # noinspection bad-argument-type
        super().__init__(AppWindow, lambda app, window: AppController(app, window, session))
