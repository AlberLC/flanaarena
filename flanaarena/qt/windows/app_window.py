import constants
from qt.widgets.central_widgets.app_central_widget import AppCentralWidget
from qt.windows.bases import GuiWindow, MovableWindow
from windows_api import windows


class AppWindow(MovableWindow, GuiWindow[AppCentralWidget]):
    def __init__(self) -> None:
        super().__init__(constants.LOGO_PATH, lambda: AppCentralWidget(self))

    def bring_to_front(self) -> None:
        windows.bring_to_front(self.winId())
