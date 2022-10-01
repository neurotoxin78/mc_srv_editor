import sys
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtCore import Qt
import random
import string
from rich.console import Console
from configobj import ConfigObj

con = Console()

def extended_exception_hook(exec_type, value, traceback):
    # Print the error and traceback
    con.log(exec_type, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exec_type, value, traceback)
    sys.exit(1)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the UI Page
        self.config = None
        uic.loadUi('main.ui', self)
        self.setWindowTitle("MC Server: Редактор конфігурації")
        self.setStylesheet("main.qss")
        self.initUI()
        # Variables
        self.filename = 'server.properties'
        self.gamemode = None
        self.difficulity = None
        self.level_name = None
        self.seed = None
        self.hardcore = "false"
        # Open Config
        self.openConfig()

    def initUI(self):
        self.generateButton.clicked.connect(self.generateSID)
        self.savepushButton.clicked.connect(self.saveConfig)
        self.exitpushButton.clicked.connect(self.exitApp)
        self.hardcheckBox.toggled.connect(self.set_hardcore)
        self.comboInit()

    def comboInit(self):
        game_items = ["survival", "creative", "adventure", "spectator"]
        diff_items = ["peaceful", "easy", "normal", "hard"]
        self.gamecomboBox.addItems(game_items)
        self.gamecomboBox.currentIndexChanged.connect(self.gamemode_change)
        self.diffcomboBox.addItems(diff_items)
        self.diffcomboBox.currentIndexChanged.connect(self.difficulity_change)

    def set_hardcore(self):
        self.hardcore = str(self.hardcheckBox.isChecked()).lower()
        con.log(F"Hardcore: {self.hardcore}")

    def gamemode_change(self):
        self.gamemode = self.gamecomboBox.currentText()

    def difficulity_change(self):
        self.difficulity = self.diffcomboBox.currentText()

    def openConfig(self):
        self.config = ConfigObj(self.filename)
        self.level_name = self.config.get('level-name')
        self.difficulity = self.config.get('difficulty')
        self.gamemode = self.config.get('gamemode')
        self.levellineEdit.setText(self.level_name)
        print(self.gamemode, self.difficulity)
        gamemode_index = self.gamecomboBox.findText(self.gamemode)
        self.gamecomboBox.setCurrentIndex(gamemode_index)
        diff_index =  self.diffcomboBox.findText(self.difficulity)
        self.diffcomboBox.setCurrentIndex(diff_index)
        self.generateSID()

    def saveConfig(self):
        self.config.write_empty_values = True
        self.config['level-seed'] = self.sidlineEdit.text()
        self.config['difficulty'] = self.difficulity
        self.config['gamemode'] = self.gamemode
        self.config['level-name'] = self.levellineEdit.text()
        self.config['hardcore'] = self.hardcore
        self.config.write()
        con.log("Writed")

    def generateSID(self):
        # string.ascii_uppercase + string.digits
        seed = ''.join(random.choice(string.digits) for _ in range(16))
        con.log(seed)
        self.sidlineEdit.setText(seed)

    def setStylesheet(self, filename):
        with open(filename, "r") as fh:
            self.setStyleSheet(fh.read())

    def exitApp(self):
        pass


def main():
    sys._excepthook = sys.excepthook
    sys.excepthook = extended_exception_hook
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
