import requests

from controllers.app_controller import AppController
from qt.apps.bases import GuiApp
from qt.windows.app_window import AppWindow


class App(GuiApp[AppWindow]):
    def __init__(self, session: requests.Session) -> None:
        super().__init__(AppWindow)

        controller = AppController(self, session)
        controller.start()

        self.window.show()
