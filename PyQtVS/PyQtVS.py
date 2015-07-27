from PyQt5 import QtCore, QtWidgets
import MainWindow
import Thread


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.setWindowTitle("Test PyQt Application")
    window.show()

    sys.exit(app.exec_())

