import PySide2
from PySide2.QtWidgets import*
# QApplication, QWidget, QPushButton, QTableWidget, QSpinBox
from PySide2.QtGui import QBrush, QMovie, QDoubleValidator, QEnterEvent, QFont, QMouseEvent, QPainterPath, QPalette, QPixmap, QIcon, QColor, QPainter, QPen, QFontMetrics
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import*
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import os
import menu
import recipe_db
from stylesheet_update import COLORS
import time

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

class MyStyle(QProxyStyle):#to be able to set value of slider immediately at mouse pos
    
    def styleHint(self, hint: PySide2.QtWidgets.QStyle.StyleHint, option=0, widget=0, returnData=0) -> int:
        if hint == QStyle.SH_Slider_AbsoluteSetButtons:
            return (Qt.LeftButton | Qt.MidButton | Qt.RightButton)
        
        return super().styleHint(hint, option=option, widget=widget, returnData=returnData)

class SliderWithValue(QSlider):

    def __init__(self, parent=None):
        super(SliderWithValue, self).__init__(parent)
        self.setStyle(MyStyle())
        # self.setStyleSheet(self.stylesheet)

    def paintEvent(self, event):
        QSlider.paintEvent(self, event)

        painter = QPainter(self)
        qpen = QPen(QColor(COLORS['#color1_bright#']))
        painter.setPen(qpen)

        font_metrics = QFontMetrics(self.font())
        font_width = font_metrics.boundingRect(str(self.value())).width()
        
        rect = self.geometry()
        min_pos =  rect.width() - font_width - self.width() + 25
        max_pos = rect.width() - font_width - 47
        slider_pos = min_pos + (max_pos - min_pos) / (self.maximum()-1) * (self.value()-1)
        
        horizontal_x_pos = slider_pos
        horizontal_y_pos = rect.height() * 0.75

        text = '%s jour' % str(self.value()) + 's'*(self.value()>1)
        painter.drawText(QPoint(horizontal_x_pos, horizontal_y_pos), text)

        painter.drawRect(rect)



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

def changeFont(lineEdit, change=True):
    stylesheet_init = 'QLineEdit,QSpinBox{color:%s;}' % COLORS['#color1_dark#']
    stylesheet_change = 'QLineEdit,QSpinBox{color:%s;}' % COLORS['#color3_bright#']
    if change:
        lineEdit.setStyleSheet(stylesheet_change)
    else:
        lineEdit.setStyleSheet(stylesheet_init)
        
def animate_button(pB, custom = False, options = {}):
    animation = QPropertyAnimation(pB, b"iconSize")
    if custom:
        duration = options['duration']
        animation.setDuration(duration)
        for k, size in options['keys'].items():
            animation.setKeyValueAt(k, QSize(size, size))
    else:
        animation.setDuration(160)
        animation.setKeyValueAt(0, QSize(27,27))
        animation.setKeyValueAt(0.5, QSize(20,20))
        animation.setKeyValueAt(1, QSize(27,27))
    animation.setEasingCurve(QEasingCurve.Linear)

    return animation
    # self.animation.start()

def decoratortimer(decimal):
    def decoratorfunction(f):
        def wrap(*args, **kwargs):
            time1 = time.monotonic()
            result = f(*args, **kwargs)
            time2 = time.monotonic()
            print('{:s} function took {:.{}f} ms'.format(f.__name__, ((time2-time1)*1000.0), decimal ))
            return result
        return wrap
    return decoratorfunction

def is_filter_in_recipe_name(filter, recipe, cB = None):
    if type(cB) is QCheckBox:
        if cB.isChecked():
            return filter in recipe.name.lower()
        return False
    return filter in recipe.name.lower()

def is_filter_in_ing_list(filter,recipe, cB = None):
    if recipe.ingredients_list_qty is not None:
        if type(cB) is QCheckBox:
            if cB.isChecked(): 
                for ingredient in list(map(str.lower, recipe.ingredients_list_qty)):
                    if filter in ingredient:
                        return True
            return False
        for ingredient in list(map(str.lower, recipe.ingredients_list_qty)):
            if filter in ingredient:
                return True
    return False

def is_filter_in_preparation(filter, recipe, cB = None):
    if recipe.preparation is not None:
        if type(cB) is QCheckBox:
            if cB.isChecked():
                return filter in recipe.preparation.lower()
            return False
        return filter in recipe.preparation.lower()
    return False


def dynamic_filter(text, lW, recipe_db, tagFunc = None):
    with_filters = text.split(',')
    recipeCount = 0

    for recipeIndex in range(lW.count()):
        recipeListItem = lW.item(recipeIndex)
        recipe = recipe_db.get_recipe_object(recipeListItem.text())
        show_recipe_flag = True
        
        for filter in with_filters:
            filter = filter.strip()
            isCriteriaMet = is_filter_in_recipe_name(filter, recipe)
            isCriteriaMet = isCriteriaMet or is_filter_in_ing_list(filter, recipe)
            isCriteriaMet = isCriteriaMet or is_filter_in_preparation(filter, recipe)
            
            show_recipe_flag = show_recipe_flag and isCriteriaMet

        if tagFunc is not None:
            show_recipe_flag = show_recipe_flag and tagFunc(recipe)

        lW.setItemHidden(recipeListItem, not show_recipe_flag)
        if show_recipe_flag:
            recipeCount += 1

def gif_to_button(gif_path, pB):
    movie = QMovie()
    movie.setFileName(gif_path)
    movie.frameChanged.connect(lambda: pB.setIcon(movie.currentPixmap()))
    movie.start()
    return movie