from controllers.app_controller import AppController
from qt.apps.bases import GuiApp
from qt.windows.app_window import AppWindow


class App(GuiApp[AppWindow]):
    def __init__(self) -> None:
        super().__init__(AppWindow)

        controller = AppController(self)
        controller.load()

        self.window.show()
