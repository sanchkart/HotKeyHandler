from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
import Objects

class HotKeyObjectView(QtWidgets.QHBoxLayout):
    def __init__(self,parent,name,num):
        super(HotKeyObjectView,self).__init__(parent)
        self._object = Objects.HotKeyObject(name,num)
        self._name = name
        self._hotKeyComboString=''

        for key in num:
            if(len(self._hotKeyComboString)>0):
                self._hotKeyComboString=self._hotKeyComboString+"+"+str(key)
            else:
                self._hotKeyComboString=self._hotKeyComboString+str(key)

        self._textEdit = QtWidgets.QLineEdit(self._hotKeyComboString)
        self._textEdit.setReadOnly(True)
        self._textEdit.setDisabled(True)

        self._btnChange = QtWidgets.QPushButton("Change")
        self._btnChange.clicked.connect(lambda: parent.onAddButton(self))

        self._checkAble = QtWidgets.QCheckBox("Enabled")
        self._checkAble.toggled.connect(self.switchHotKey)
        self._checkAble.toggled.connect(lambda: parent.onSwitchKey(self))

        self.addWidget(self._textEdit)
        self.addWidget(self._btnChange)
        self.addWidget(self._checkAble)


    def switchHotKey(self):
        self._textEdit.setDisabled(not self._checkAble.isChecked())


class ChangeOrAddHotKeyWindow(QtWidgets.QWidget):
    okAddSignal = QtCore.pyqtSignal([str,HotKeyObjectView], name="okAddSignal")
    def __init__(self,category="Enter name here", parent=None):
        super(ChangeOrAddHotKeyWindow, self).__init__(parent)
        self.setWindowTitle("Enter name of field")

        self._chooselayout = QtWidgets.QFormLayout(self)

        self._infoNameSelectButton="Enter name here"
        self._infoSelectButton="Just click here and press your hotkey for capturing"

        self._textEditName = QtWidgets.QLineEdit(self._infoNameSelectButton,self)
        self._textEditName.setText(category)

        self._textView = Objects.HotKeyHandler(self._infoSelectButton)

        self._btnOk = QtWidgets.QPushButton("Add or change",self)
        self._btnOk.clicked.connect(self.onOkButtonClicked)

        self._btnClear = QtWidgets.QPushButton("Clear")
        self._btnClear.clicked.connect(self.clear)

        self._chooselayout.addRow(self._textEditName)
        self._chooselayout.addRow(self._textView)
        self._chooselayout.addRow(self._btnOk)
        self._chooselayout.addRow(self._btnClear)

        self.setLayout(self._chooselayout)

    def onOkButtonClicked(self):
        if self._infoSelectButton == self._textView.toPlainText() or self._infoNameSelectButton == self._textEditName.text():
            QMessageBox(QMessageBox.Warning,"Error.","Please, enter data HotKey.",QMessageBox.Ok,self).show()
        else:
            object = HotKeyObjectView(self,self._textEditName.text,self._textView.key)
            self.okAddSignal.emit(self._textEditName.text(), object)
            self.close()

    def clear(self):
       self._textView.setText(self._infoSelectButton)
       self._textView.str=''
       self._textView.key=[]

