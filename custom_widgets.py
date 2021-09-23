import PySide2
from PySide2.QtWidgets import*
# QApplication, QWidget, QPushButton, QTableWidget, QSpinBox
from PySide2.QtGui import QBrush, QDoubleValidator, QEnterEvent, QFont, QMouseEvent, QPainterPath, QPixmap, QIcon, QColor, QPainter
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import*
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import os
import menu
import recipe_db

class TableWidgetCustom(QTableWidget): #Custom TableWidget to adjust item position
    def __init__(self, parent=None):
        super(TableWidgetCustom, self).__init__(parent)
        self.setStyleSheet(parent.styleSheet())
    
    def viewOptions(self) -> PySide2.QtWidgets.QStyleOptionViewItem:
        option = QTableWidget.viewOptions(self)
        option.decorationAlignment = Qt.AlignHCenter | Qt.AlignCenter
        option.decorationPosition = QStyleOptionViewItem.Top
        # return super().viewOptions()
        return option

class SpinBoxCustom(QSpinBox): #Custom SpinBox to force +- only, ignoring keyboard input
    def __init__(self, parent=None):
        super(SpinBoxCustom, self).__init__(parent)
        self.setStyleSheet(parent.styleSheet())
    
    def keyPressEvent(self, event: PySide2.QtGui.QKeyEvent) -> None:
        return event.ignore()
        # return super().keyPressEvent(event)
    
class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        pass


def getFormAncestor(widget):
    ancestor = widget
    while ancestor is not None and not ancestor.objectName() == 'Form':
        ancestor = ancestor.parent()
    # print(self.label_title.text(), ancestor.objectName())
    return ancestor

def load_pic(widget, picture_path):#Display image on widget from image path
    picture = QPixmap(picture_path)
    widget.setPixmap(picture)


def display_image(recipe_object, dirname, widget, icon = True):#Scale and display image on Widget from recipe object
    if icon:
        if recipe_object is None:#special case for header icon
            image_path = dirname
            icon = QIcon()
            qpix = QPixmap(image_path)
            icon.addPixmap(qpix, mode = QIcon.Selected, state = QIcon.On)
            widget.setSizeHint(QSize(60, 60))
            widget.setIcon(icon)

        elif recipe_object.image != '' and recipe_object.image != '/images/':
            image_path = dirname + recipe_object.image + '_icon.jpg'
            # icon = QIcon()
            qpix = QPixmap(image_path)

            qpix_to_widget(qpix, widget)

    else:
        if recipe_object.image != '' and recipe_object.image != '/images/':
            image_path = dirname + recipe_object.image + '.jpg'
            qpix = QPixmap(image_path)


            if qpix.width() > qpix.height():
                # qpix_scaled = qpix.scaled(400, 300)
                qpix_scaled = qpix.scaled(270, 200)
            else:
                # qpix_scaled = qpix.scaled(300, 400)
                qpix_scaled = qpix.scaled(200, 270)

            # print('-%s-' % recipe_object.image)
            qpix_to_widget(qpix_scaled, widget, icon=False)
            
        else:
            image_path = dirname + "/images/placeholder_dish_icon.jpg"
            qpix = QPixmap(image_path)
            if qpix.width() > qpix.height():
                qpix_scaled = qpix.scaled(270, 200)
            else:
                qpix_scaled = qpix.scaled(200, 270)
            qpix_to_widget(qpix_scaled, widget, icon=False)

def display_new_image(image_path, widget, icon = False):#Scale and display image on Widget from Image path
    qpix = QPixmap(image_path)

    if qpix.width() > qpix.height():
        # qpix_scaled = qpix.scaled(400, 300)
        qpix_scaled = qpix.scaled(270, 200)
    else:
        # qpix_scaled = qpix.scaled(300, 400)
        qpix_scaled = qpix.scaled(200, 270)
        
    qpix_to_widget(qpix_scaled, widget, icon)

def qpix_to_widget(qpix, widget, icon = True):#set Image of a Widget rounded from QPixmap object
    x_size, y_size = qpix.width(), qpix.height()
    rounded = QPixmap(x_size, y_size)
    rounded.fill(Qt.transparent)
    path = QPainterPath()
    path.addRoundedRect(rounded.rect(), 25, 25, mode=Qt.RelativeSize)
    painter = QPainter()
    painter.begin(rounded)
    painter.setClipPath(path)
    painter.fillRect(rounded.rect(), Qt.transparent)
    x = int((qpix.width() - x_size)/2)
    y = int((qpix.height() - y_size)/2)
    painter.drawPixmap(x, y, qpix.width(), qpix.height(), qpix)
    painter.end()
    if icon:
        try:
            widget.setIcon(QIcon(rounded))
        except:#case label with icon
            widget.setPixmap(rounded)
    else:
        widget.setPixmap(rounded)

def style_factory(widget : QWidget, init_colors, colors):
    init_stylesheet = widget.styleSheet()
    stylesheet = init_stylesheet
    #replace init stylesheet
    for color in colors:
        old_hex = init_colors[color][0]
        new_hex = colors[color][0]
        stylesheet = stylesheet.replace(old_hex, new_hex)
    widget.setStyleSheet(stylesheet)
    return widget
    # return colors
        