import PySide2
from PySide2.QtWidgets import*
# QApplication, QWidget, QPushButton, QTableWidget, QSpinBox
from PySide2.QtGui import QBrush, QDoubleValidator, QFont, QPainterPath, QPixmap, QIcon, QColor, QPainter
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import*
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import os
import menu
import recipe_db

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
    
class StackedRecipes(QWidget):
    def __init__(self, recipe_list, recipe_db = None, parent=None):
        super(StackedRecipes, self).__init__(parent)
        
        self.recipe_list = recipe_list
        self.recipe_db = recipe_db
        self.initial_state()
        self.connect_actions()
    
    def initial_state(self):
        self.pW = self.parentWidget()
        self.dirname = os.path.dirname(__file__)
        self.pB_add: QPushButton
        self.pB_add = self.pW.pB_add
        self.pB_delete: QPushButton
        self.pB_delete = self.pW.pB_delete
        self.pB_next: QPushButton
        self.pB_next = self.pW.pB_next
        self.label_image: QLabel
        self.label_image = self.pW.label_image
        self.label_title: QLabel
        self.label_title = self.pW.label_title
        self.frame_card: QFrame
        self.frame_card = self.pW.frame_card
        self.hL: QHBoxLayout
        self.hL = self.pW.hL
        
        self.current_index = len(self.recipe_list) - 1
        self.layout_widgets = []
        
        self.update_recipes()        
        self.show_hide_buttons()
        self.update_index()
        
        self.pB_add.setIcon(QIcon(self.dirname + '/UI/images/icon_new_recipe.png'))
        self.pB_delete.setIcon(QIcon(self.dirname + '/UI/images/icon_bin.png'))
        self.pB_next.setIcon(QIcon(self.dirname + '/UI/images/icon_right_arrow.png'))
        
    def connect_actions(self):
        self.pB_add.clicked.connect(self.on_add)
        self.pB_delete.clicked.connect(self.on_delete)
        self.pB_next.clicked.connect(self.on_right)
    
    def update_recipes(self, index = -1):
        recipe = self.recipe_list[index]

        image_path = self.dirname + recipe.image + '_icon.jpg'
        qpix = QPixmap(image_path)
        if recipe.image != '' and recipe.image != '/images/':
            p1 = qpix.scaledToHeight(self.parentWidget().height()*0.8, Qt.SmoothTransformation)
            self.label_image.setPixmap(p1)
        else:
            self.label_image.setPixmap(qpix)
        self.label_title.setText(recipe.name)
    
    def on_add(self, recipe = None, dinner = 0):
        #dinner = 0;1 => lunch;dinner
        if recipe is None:
            simple_menu = menu.Menu(number_of_days=1)
            simple_menu.generate_smart_menu_v2(self.recipe_db)
            recipe = simple_menu.table[dinner]
            while recipe.name in recipe_db.get_recipe_names(self.recipe_list):
                simple_menu.generate_smart_menu_v2(self.recipe_db)
                recipe = simple_menu.table[dinner]
        self.recipe_list.append(recipe)
        
        self.show_hide_buttons()
        
        #display latest recipe added
        self.current_index = -1
        self.update_recipes()
        self.update_index()
        
    def on_delete(self):
        self.recipe_list.remove(self.recipe_list[self.current_index])
        self.current_index = self.current_index % len(self.recipe_list)
        self.update_recipes(index = self.current_index)
        self.update_index()
        self.show_hide_buttons()
        
    def on_right(self):
        self.current_index = (self.current_index + 1) % len(self.recipe_list)
        self.update_recipes(index = self.current_index)
        self.update_index()
        
    def show_hide_buttons(self):
        self.pB_next.setVisible(len(self.recipe_list) > 1)
        self.pB_delete.setVisible(len(self.recipe_list) > 1)
    
    def update_index(self):#to display the current index with dots icon
        for widget in self.layout_widgets:
            widget.setParent(None)
            self.hL.removeWidget(widget)
        self.layout_widgets = []
        
        if self.current_index == -1:
            index = len(self.recipe_list)
        else:
            index = self.current_index + 1
        length = len(self.recipe_list)

        if length > 1:
            for i in range(length - 1):
                label_num = QLabel('')
                load_pic(label_num, self.dirname + '/UI/images/icon_circle.png')
                self.hL.addWidget(label_num)
                self.layout_widgets.append(label_num)
            label_pos = QLabel('')
            load_pic(label_pos, self.dirname + '/UI/images/icon_circle_full.png')
            self.hL.insertWidget(index - 1, label_pos)
            self.layout_widgets.append(label_pos)
            
        
def create_stack(recipe, recipe_db):
    dirname = os.path.dirname(__file__)
    myStack = dirname + '/UI/stacked_recipes.ui'
    w = QUiLoader().load(myStack)
    mySW = StackedRecipes(recipe_list = [recipe], recipe_db = recipe_db, parent = w)
    # w.show()
    return mySW

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
            widget.setPixmap(QPixmap())

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

        
        