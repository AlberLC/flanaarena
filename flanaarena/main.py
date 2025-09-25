import urllib3
from PySide6 import QtWidgets

from controllers.controller import Controller
from qt.windows import MainWindow

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = QtWidgets.QApplication()

window = MainWindow()

controller = Controller(window.central_widget)
controller.load()

window.show()

app.exec()
