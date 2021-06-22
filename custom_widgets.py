import PySide2
from PySide2.QtWidgets import*
# QApplication, QWidget, QPushButton, QTableWidget, QSpinBox
from PySide2.QtGui import QBrush, QDoubleValidator, QPainterPath, QPixmap, QIcon, QColor, QPainter
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import*
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

class TableWidgetCustom(QTableWidget): #Custom TableWidget to adjust item position
    def __init__(self, parent=None):
        super(TableWidgetCustom, self).__init__(parent)
    
    def viewOptions(self) -> PySide2.QtWidgets.QStyleOptionViewItem:
        option = QTableWidget.viewOptions(self)
        option.decorationAlignment = Qt.AlignHCenter | Qt.AlignCenter
        option.decorationPosition = QStyleOptionViewItem.Top
        # return super().viewOptions()
        return option

class SpinBoxCustom(QSpinBox): #Custom SpinBox to force +- only, ignoring keyboard input
    def __init__(self, parent=None):
        super(SpinBoxCustom, self).__init__(parent)
    
    def keyPressEvent(self, event: PySide2.QtGui.QKeyEvent) -> None:
        return event.ignore()
        # return super().keyPressEvent(event)
    
class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        pass