import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import hta

# not used directly but employed by the qml that is loaded
from PyQt5 import QtQuick


class Gui(QObject):
    def __init__(self):
        QObject.__init__(self)

    # Signal sending results of run
    runResult = pyqtSignal(str, arguments=['run'])

    # Slot for running HTA
    @pyqtSlot(str, str, str)
    def run(self, arg1, arg2, arg3):
        print("run activated with arguments {}, {}, {}".format(arg1, arg2, arg3))
        # Run program and emit a signal
        if arg1 == "":
            self.runResult.emit("Please choose files for chemistries.")
            return
        if arg2 == "":
            self.runResult.emit("Please choose a main file.")
            return
        try:
            arg3 = float(arg3)
        except ValueError:
            self.runResult.emit("Please enter the secondary dendrite arm spacing (SDAS).")
            return

        # Remove the "file:///" portion of the folder
        arg1 = arg1[8:]
        arg2 = arg2[arg2.rfind("/") + 1:]

        lines, solidus = hta.runMain(arg1, arg2, arg3)

        self.runResult.emit("Outputs have been created.\nThere were {} lines and the solidus was {}.".format(lines, solidus))

def runGui():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    gui = Gui()
    # And register it in the context of QML
    engine.rootContext().setContextProperty("gui", gui)
    # Load the qml file into the engine
    engine.load("main.qml")

    engine.quit.connect(app.quit)
    sys.exit(app.exec_())

