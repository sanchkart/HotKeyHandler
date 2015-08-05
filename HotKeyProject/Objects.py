from PyQt5 import QtWidgets
import win32con

keys = {
    16: ["Shift", win32con.MOD_SHIFT],
    17: ["Ctrl", win32con.MOD_CONTROL],
    18: ["Alt", win32con.MOD_ALT],
    91: ["Win", win32con.MOD_WIN]
}


class HotKeyHandler(QtWidgets.QTextEdit):
    def __init__(self, title, parent=None):
        super(HotKeyHandler, self).__init__(parent)
        self.__str = ''
        self.setText(title)
        self.key = []
        self.__flag = False
        self.hotKeyComplete = False

    def keyPressEvent(self, e):
        if self.__flag:
            self.__str = ''
            self.key = []
            self.__flag = False
            self.hotKeyComplete = False

        control = EventControl(e, self.key, self.__str, self.hotKeyComplete)

        self.key = control.arrayKey
        self.__str = control.str
        self.__flag = control.flag
        self.hotKeyComplete = control.keyComplete
        self.setText(self.__str)


class HotKeyChange(QtWidgets.QLineEdit):
    def __init__(self, title, parent=None):
        super(HotKeyChange, self).__init__(parent)
        self.__str = ''
        self.setText(title)
        self.key = []
        self.__flag = False
        self.hotKeyComplete = False

    def keyPressEvent(self, e):
        if self.__flag:
            self.__str = ''
            self.key = []
            self.__flag = False
            self.hotKeyComplete = False

        control = EventControl(e, self.key, self.__str, self.hotKeyComplete)

        self.key = control.arrayKey
        self.__str = control.str
        self.__flag = control.flag
        self.hotKeyComplete = control.keyComplete
        self.setText(self.__str)


class EventControl():
    def __init__(self, key, arrayKey, str, keyComplete):
        self.arrayKey = arrayKey
        self.str = str
        self.flag = False
        self.keyComplete = keyComplete
        self.__accept = 1

        if keys.get(key.nativeVirtualKey()):
            self.__accept = self.arrayKey.count(keys.get(key.nativeVirtualKey())[1])
        else:
            self.__accept = self.arrayKey.count(key.nativeVirtualKey())

        if self.__accept == 0:
            if len(self.arrayKey) == 0 and not keys.get(key.nativeVirtualKey()):
                return
            if len(self.arrayKey) == 2 and keys.get(key.nativeVirtualKey()):
                return

            if keys.get(key.nativeVirtualKey()):
                self.arrayKey.append(keys.get(key.nativeVirtualKey())[1])
            else:
                self.arrayKey.append(key.nativeVirtualKey())

            if len(self.arrayKey) > 2:
                self.flag = True

            if not keys.get(key.nativeVirtualKey()) and len(key.text()) == 0:
                return

            stringAdd = ''
            if keys.get(key.nativeVirtualKey()):
                stringAdd = keys.get(key.nativeVirtualKey())[0]
            if len(stringAdd) == 0:
                stringAdd = key.text()
                self.keyComplete = True
                self.flag = True
            if self.str == '':
                self.str = stringAdd
            else:
                self.str = "%s+%s" % (self.str, stringAdd)
