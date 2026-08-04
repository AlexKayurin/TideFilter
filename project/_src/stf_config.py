from PySide6 import QtWidgets
import _UI_Config

class Config(QtWidgets.QMainWindow, _UI_Config.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.b_ok.clicked.connect(self.ok)
        self.b_cancel.clicked.connect(self.cancel)


    def subscribe_controller(self, controller) -> None:
        self._controller = controller


    def ok(self):
        self._controller.handle_saveconfig()


    def cancel(self):
        self.close()