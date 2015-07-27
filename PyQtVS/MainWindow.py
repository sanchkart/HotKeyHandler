from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

import Windows , Objects, Thread
from collections import defaultdict
import win32con

class MainWindow(QtWidgets.QWidget):

    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)

        self._map = dict()

        self._newKey =''

        self._arrayKeyEvent=[]

        self._rootLayout = QtWidgets.QVBoxLayout(self)
        self._form = QtWidgets.QFormLayout(self)
        self._vectorBase = {"One-Click":[29,2],"Create Note":[29,3],"Paste Back":[29,4],"Save File":[29,5]}
        self._vector=[]

        for category in self._vectorBase:
            object = Windows.HotKeyObjectView(self,category,self._vectorBase[category])
            self.onOkAddButton(category,object)
            
        self._btn = QtWidgets.QPushButton()
        self._btn.setText("Add Element")
        object = Windows.HotKeyObjectView(self, "NewElement", [29,1])
        self._btn.clicked.connect(lambda: self.onAddButton(object))

        self._rootLayout.addLayout(self._form)
        self._rootLayout.addWidget(self._btn)
        self.setLayout(self._rootLayout)

        """self._shorcutThread = Thread.ShortcutThread()
        self._shorcutThread.start()"""



    def onOkAddButton(self,category,numberKey):
        if(self._map.get(category) == None):
            self._vector.append(str(category))

            self._newKey = numberKey
            self._newKey._textEdit.setText(numberKey._textEdit.text())

            self._map[category]= numberKey._object

            self._lbl = QtWidgets.QLabel(category)
            self._form.addRow(self._lbl)
            self._form.addRow(numberKey)
        else:
            self._comboString=''

            for key in numberKey._object._keyValue:
                if(len(self._comboString)>0):
                    self._comboString=self._comboString+"+"+str(key)
                else:
                    self._comboString=self._comboString+str(key)
            self._newKey._textEdit.setText(self._comboString)
            self._map[category]._keyValue=numberKey._object._keyValue


    def onAddButton(self,hotKey):
        print('work')
        self._newKey = hotKey
        self._addWindow = Windows.ChangeOrAddHotKeyWindow(hotKey._name)
        self._addWindow.okAddSignal[str,Windows.HotKeyObjectView].connect(self.onOkAddButton)
        self._addWindow.show()

    def keyPressEvent(self,event):
        print(event.nativeScanCode())
        if self._arrayKeyEvent.count(event.nativeScanCode()) == 0:
            self._arrayKeyEvent.append(event.nativeScanCode())

    def keyReleaseEvent(self,event):
        for keyName in self._vectorBase:
            if self._map[keyName]._keyValue == self._arrayKeyEvent and self._map[keyName]._checkFlag:
                QMessageBox(QMessageBox.Information,"HotKey Pressed","HotKey "+keyName+" pressed.",QMessageBox.Ok,self).show()
        self._arrayKeyEvent.clear()


    def onSwitchKey(self,info):
        self._map[info._name]._checkFlag=info._checkAble.isChecked()


   
