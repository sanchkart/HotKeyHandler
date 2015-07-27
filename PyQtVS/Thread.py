from PyQt5 import QtCore, QtWidgets
import ctypes
import win32con
from ctypes import wintypes
 
user32 = ctypes.windll.user32
byref = ctypes.byref
 


class threadHotKey(QtCore.QThread):
    def  __init__(self,collection, parent=None):
        QtCore.QThread.__init__(self,parent)
        print("Thread create")
        self.user32 = ctypes.windll.user32
        self.byref = ctypes.byref
    def run(self):
        print("Thread run")
        "for key in collection:"
        self.user32.RegisterHotKey(None,1,win32con.MOD_CONTROL,0x42)
        self.msg = wintypes.MSG()

    def register(self, window):
        if ctypes.windll.user32.RegisterHotKey(window.hWindow
                , self.keyId
                , self.modifiers
                , self.virtualkeys):
            return True

        else:
            return False

    def unregister(self):
        ctypes.windll.user32.UnregisterHotKey(self, self.keyId)




class ShortcutThread(QtCore.QThread):
 
    oneClick = QtCore.pyqtSignal()
    pasteBack = QtCore.pyqtSignal()
    createNote = QtCore.pyqtSignal()
 
    def __init__(self, config, parent=None):
        super(ShortcutThread, self).__init__(parent)
        self._config = config
 
    def run(self):
        shKey = int(self._config.getValue('hotkeyCharID', 49))
        user32.RegisterHotKey(None, 1, win32con.MOD_CONTROL, shKey)
 
        from pe.config import config
 
        if config.isFull:
            noteKey = int(self._config.getValue('hotkeyNoteCharID', 50))
            user32.RegisterHotKey(None, 3, win32con.MOD_CONTROL, noteKey)
 
        pbKey = int(self._config.getValue('hotkeyPBCharID', 51))
        user32.RegisterHotKey(None, 2, win32con.MOD_CONTROL, pbKey)
 
        msg = wintypes.MSG()
        while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
 
            shStatus = int(self._config.getValue('hotkeyStatus', 1))
            pbStatus = int(self._config.getValue('hotkeyPBStatus', 1))
            noteStatus = int(self._config.getValue('hotkeyNoteStatus', 1))
 
            if msg.message == win32con.WM_HOTKEY:
                if msg.wParam == 1 and shStatus > 0:
                    self.oneClick.emit()
                elif msg.wParam == 2 and pbStatus > 0:
                    self.pasteBack.emit()
                elif msg.wParam == 3 and noteStatus > 0 and config.isFull:
                    self.createNote.emit()
                user32.TranslateMessage (byref (msg))
                user32.DispatchMessageA (byref (msg))
 
class ShortcutHandler(object):
    def __init__(self, ocCallback, pbCallback, noteCallback, config, parent=None):
        self._config = config
        self._shThread = None
        self._ocCallback = ocCallback
        self._pbCallback = pbCallback
        self._noteCallback = noteCallback
        self._parent = parent
 
    def stop(self):
        user32.UnregisterHotKey(None, 1)
        if self._shThread:
            self._shThread.terminate()
            self._shThread = None
 
    def run(self):
        if self._shThread:
            self.stop()
        QtWidgets.QApplication.processEvents()
        self._shThread = ShortcutThread(self._config, self._parent)
        self._shThread.oneClick.connect(self._ocCallback)
        self._shThread.pasteBack.connect(self._pbCallback)
        self._shThread.createNote.connect(self._noteCallback)
        self._shThread.start()