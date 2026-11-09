from qt.apps.bases import GuiApp
from qt.widgets.bases import UiWidget
from qt.windows.bases import GuiWindow


class Controller[TApp: GuiApp, TWindow: GuiWindow[UiWidget]]:
    def __init__(self, app: TApp, window: TWindow) -> None:
        self._app = app
        self._window = window
        self._gui = self._window.central_widget

    def start(self) -> None:
        pass
