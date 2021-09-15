from PySide2.QtWidgets import*
import string
import uuid

class UIDWidget(QWidget):
    def __init__(self,parent=None):
        super(UIDWidget,self).__init__(parent)
        self.uid = str(uuid.uuid4())

    def getUID(self) -> string:
        return self.uid