from PyQt5 import QtWidgets

keys = {
    "42": "shift"
    ,"29": "ctrl"
    ,"56": "alt"
    ,"347":"win"
    ,"328":"up"
    ,"336":"down"
    ,"331":"left"
    ,"333":"right"
    ,"329":"pgup"
    ,"337":"pgdown"
    ,"327":"home"
    ,"335":"end"
    ,"338":"insert"
    ,"28":"enter"
    ,"15":"tab"
    ,"57":"space"
    ,"14":"backspace"
    ,"339":"del"
    ,"1":"escape"
    ,"59": "f1"
    ,"60":"f2"
    ,"61":"f3"
    ,"62":"f4"
    ,"63":"f5"
    ,"64":"f6"
    ,"65":"f7"
    ,"66":"f8"
    ,"67":"f9"
    ,"68":"f10"
    ,"87":"f11"
    ,"88":"f12"
    ,"82":"numpad0"
    ,"79":"numpad1"
    ,"80":"numpad2"
    ,"81":"numpad3"
    ,"75":"numpad4"
    ,"76":"numpad5"
    ,"77":"numpad6"
    ,"71":"numpad7"
    ,"72":"numpad8"
    ,"73":"numpad9"
}

class HotKeyHandler(QtWidgets.QTextEdit):
    def __init__(self,title,parent=None):
        super(HotKeyHandler, self).__init__(parent)
        self.str=''
        self.setText(title)
        self.key=[]
        self.flagOne=False
        self.flagTwo=False
    def keyPressEvent(self,event):
        if self.key.count(event.nativeScanCode()) == 0:
            if len(self.key) == 0 and not keys.get(str(event.nativeScanCode())):
                return 
            if event.text() !='' or keys.get(str(event.nativeScanCode())):
                self.key.append(event.nativeScanCode())
            self.stringAdd=''
            if keys.get(str(event.nativeScanCode())):
                self.stringAdd=keys.get(str(event.nativeScanCode()))
            if len(self.stringAdd) == 0 and event.text() !='':
                self.stringAdd=event.text()
            if self.str == '':
                self.str=self.stringAdd
            else:
                self.str=self.str+"+"+self.stringAdd
        self.setText(self.str)
        print(self.key)


class HotKeyObject():
    def __init__(self,name ="",number=[1]):
        self._name = name
        self._keyValue = number
        self._checkFlag = False
          

