# SimpleTideFilter on MVC pattern 13/08/2026; Refactored for Nuitka build

import os
import sys
from PySide6 import QtWidgets
from stf_controller import Controller
from stf_model import Model
from stf_view import View
from stf_config import Config


if __name__ == '__main__':
    parentfold = os.path.dirname(sys.argv[0])

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')

    view = View()
    model = Model()
    config = Config()
    controller = Controller(config, view, model, parentfold)
    view.show()

    sys.exit(app.exec())

