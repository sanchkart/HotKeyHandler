from PyQt5 import QtCore
import win32con, ctypes, logging, sys
from ctypes import wintypes

byref = ctypes.byref
user32 = ctypes.windll.user32
msg = wintypes.MSG()


class HotKeyThread(QtCore.QThread):
    showMessage = QtCore.pyqtSignal(str, str)

    def __init__(self, keysVector, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.__logger = logging.getLogger("HotKeyThread")
        self.__logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)
        self.__count = 0
        self.__keysVector = keysVector
        self.__names = {}

    def clean(self):
        while self.__count > 0:
            self.__logger.info(user32.UnregisterHotKey(None, self.__count))
            self.__count -= 1

    def run(self):
        self.clean()

        for oneHotKey in self.__keysVector:
            self.__count += 1
            self.__names[self.__count] = self.__keysVector[oneHotKey].name
            self.__logger.info(self.__keysVector[oneHotKey].key[0])
            flag = True
            if len(self.__keysVector[oneHotKey].key[0]) == 2:
                flag = user32.RegisterHotKey(None, self.__count, self.__keysVector[oneHotKey].key[0][0] |
                                             self.__keysVector[oneHotKey].key[0][1],
                                             self.__keysVector[oneHotKey].key[1])
            else:
                flag = user32.RegisterHotKey(None, self.__count, self.__keysVector[oneHotKey].key[0][0],
                                             self.__keysVector[oneHotKey].key[1])

            if flag:
                self.__logger.info('Key number %s create' % self.__count)
            else:
                self.__logger.info('Key number %s no create' % self.__count)

        try:
            while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY and self.__keysVector[
                    self.__names[msg.wParam]].checkAble.isChecked():
                    self.showMessage.emit("Key pressed.", "HotKey %s clicked." % self.__names[msg.wParam])
                    self.__logger.info(self.__names[msg.wParam])
        except:
            print('END')
