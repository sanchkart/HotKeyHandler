from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
import Objects


class HotKeyObjectView(QtWidgets.QHBoxLayout):
    showMessage = QtCore.pyqtSignal(str, str)
    resetParentTread = QtCore.pyqtSignal()

    def __init__(self, name, keys=[], keyString='', parent=None):
        super(HotKeyObjectView, self).__init__(parent)
        self.name = name
        self.key = keys
        self.__textEdit = Objects.HotKeyChange(keyString)
        self.__textEdit.setReadOnly(True)
        self.__textEdit.setDisabled(True)
        self.__btnChange = QtWidgets.QPushButton("Change")
        self.__btnChange.clicked.connect(lambda: self.changeHotKey())
        self.checkAble = QtWidgets.QCheckBox("Enabled")
        self.checkAble.toggled.connect(self.switchHotKey)
        self.addWidget(self.__textEdit)
        self.addWidget(self.__btnChange)
        self.addWidget(self.checkAble)

    def switchHotKey(self):
        self.__textEdit.setDisabled(not self.checkAble.isChecked())

    def changeHotKey(self):
        if self.__textEdit.hotKeyComplete and self.key != self.__textEdit.key:
            if len(self.__textEdit.key) == 2:
                self.__textEdit.key = [[self.__textEdit.key[0]], self.__textEdit.key[1]]
            else:
                self.__textEdit.key = [[self.__textEdit.key[0], self.__textEdit.key[1]], self.__textEdit.key[2]]
            self.key = self.__textEdit.key
            self.resetParentTread.emit()
            self.showMessage.emit("The Key to change.", "HotKey %s change." % self.name)
        else:
            self.showMessage.emit("The Key is not change.", "HotKey %s is not change." % self.name)


class ChangeOrAddHotKeyWindow(QtWidgets.QWidget):
    resetParentTread = QtCore.pyqtSignal()
    onOkAddButtonNew = QtCore.pyqtSignal(HotKeyObjectView)

    def __init__(self, elem, parent=None):
        super(ChangeOrAddHotKeyWindow, self).__init__(parent)
        self.__refactorKey = elem
        self.setWindowTitle("Enter name of field")
        self.__chooselayout = QtWidgets.QFormLayout(self)
        self.__infoSelectButton = "Just click here and press your hotkey for capturing"
        self.__textEditName = QtWidgets.QLineEdit(elem.name, self)
        self.__textView = Objects.HotKeyHandler(self.__infoSelectButton)
        self.__textView.setReadOnly(True)
        self.__btnOk = QtWidgets.QPushButton("Add or change", self)
        self.__btnOk.clicked.connect(self.onOkButtonClicked)
        self.__chooselayout.addRow(self.__textEditName)
        self.__chooselayout.addRow(self.__textView)
        self.__chooselayout.addRow(self.__btnOk)
        self.setLayout(self.__chooselayout)

    def onOkButtonClicked(self):
        if self.__infoSelectButton == self.__textView.toPlainText() or self.__textEditName.text() == "Enter name here" or not self.__textView.hotKeyComplete:
            QMessageBox(QMessageBox.Warning, "Error.", "Please, enter data HotKey.", QMessageBox.Ok, self).show()
        else:
            if len(self.__textView.key) == 2:
                self.__textView.key = [[self.__textView.key[0]], self.__textView.key[1]]
            else:
                self.__textView.key = [[self.__textView.key[0], self.__textView.key[1]], self.__textView.key[2]]
            if self.__refactorKey.name == "Enter name here":
                self.onOkAddButtonNew.emit(HotKeyObjectView(self.__textEditName.text(),
                                                            self.__textView.key,
                                                            self.__textView.toPlainText())
                                           )
            self.resetParentTread.emit()

            self.close()
