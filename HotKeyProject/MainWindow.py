from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
import win32con, Windows, Thread


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__map = dict()
        self.__rootLayout = QtWidgets.QVBoxLayout(self)
        self.__form = QtWidgets.QFormLayout(self)
        self.__vectorBase = {"One-Click": [[[win32con.MOD_SHIFT], 49], 'Shift+1'],
                             "Create Note": [[[win32con.MOD_CONTROL], 50], 'Ctrl+2'],
                             "Paste Back": [[[win32con.MOD_CONTROL, win32con.MOD_SHIFT], 51], 'Ctrl+Shift+3'],
                             "Save File": [[[win32con.MOD_ALT], 52], 'Alt+4']
                             }
        self.__btn = QtWidgets.QPushButton(self)
        self.__btn.setText("Add Element")
        view = Windows.HotKeyObjectView("Enter name here")
        self.__btn.clicked.connect(lambda: self.onAddButton(view))

        for category in self.__vectorBase:
            self.onOkAddButton(Windows.HotKeyObjectView(category,
                                                        self.__vectorBase[category][0],
                                                        self.__vectorBase[category][1])
                               )
        self.__keyThread = Thread.HotKeyThread(self.__map)
        self.__keyThread.showMessage.connect(self.messageShow)
        self.__keyThread.start()
        self.__rootLayout.addLayout(self.__form)
        self.__rootLayout.addWidget(self.__btn)
        self.setLayout(self.__rootLayout)

    def onOkAddButton(self, key):
        self.__map[key.name] = key
        key.showMessage.connect(self.messageShow)
        key.resetParentTread.connect(self.threadReset)
        self.__form.addRow(QtWidgets.QLabel(self.__map[key.name].name))
        self.__form.addRow(self.__map[key.name])

    def onAddButton(self, hotKey):
        self.__addWindow = Windows.ChangeOrAddHotKeyWindow(hotKey)
        self.__addWindow.show()
        self.__addWindow.resetParentTread.connect(self.threadReset)
        self.__addWindow.onOkAddButtonNew.connect(self.onOkAddButton)

    def threadReset(self):
        self.__keyThread.terminate()
        self.__keyThread.start()

    def messageShow(self, title, text):
        QMessageBox(QMessageBox.Information, title, text, QMessageBox.Ok, self).show()
