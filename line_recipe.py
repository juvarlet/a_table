import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon
import custom_widgets as cw
from right_click_menu import RightClickMenu
from menu import Menu
from stylesheet_update import COLORS
import os, sys

UI_FILE = os.path.dirname(__file__) + '/UI/line_recipe.ui'

class LineRecipe(QWidget):
    
    on_menu_request = Signal(int)
    
    # def __init__(self, recipe, menu, parent=None):
    def __init__(self, recipe, index, parent=None):
        super(LineRecipe, self).__init__(parent)

        self.loadUI()
        self.recipe = recipe
        self.index = index
        # self.menu = menu
        self.saveComponents()
        self.initial_state()
        self.connect_actions()
    
    def loadUI(self):
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        loader = QUiLoader()
        widget = loader.load(UI_FILE)
        vlayout.addWidget(widget)
        self.setLayout(vlayout)
        self.pW = widget
    
    def saveComponents(self):
        # self.dirname = os.path.dirname(__file__)
        self.dirname = os.path.dirname(os.path.abspath(__file__))

        self.label_name: QLabel
        self.label_name = self.pW.label_name
        self.label_dessert: QLabel
        self.label_dessert = self.pW.label_dessert
        self.label_double: QLabel
        self.label_double = self.pW.label_double
        self.label_kids: QLabel
        self.label_kids = self.pW.label_kids
        self.label_lunch: QLabel
        self.label_lunch = self.pW.label_lunch
        self.label_dinner: QLabel
        self.label_dinner = self.pW.label_dinner
        self.label_summer: QLabel
        self.label_summer = self.pW.label_summer
        self.label_tips: QLabel
        self.label_tips = self.pW.label_tips
        self.label_vegan: QLabel
        self.label_vegan = self.pW.label_vegan
        self.label_winter: QLabel
        self.label_winter = self.pW.label_winter
        self.pB_add: QPushButton
        self.pB_add = self.pW.pB_add
    
    # @cw.decoratortimer(1)
    def initial_state(self):
        # self.initial_1()
        # self.initial_2()
        # self.initial_3()


        self.setMouseTracking(True)
        
        self.label_name.setText(self.recipe.name)
        tags = [self.label_vegan, 
                self.label_kids, 
                self.label_double, 
                self.label_lunch, 
                self.label_dinner, 
                self.label_summer, 
                self.label_winter, 
                self.label_dessert, 
                self.label_tips]
        tags_names = ['vegan', 'kids', 'double', 'midi', 'soir', 'ete', 'hiver', 'dessert', 'tips']
        for tag, tag_name in zip(tags, tags_names):
            tag.setVisible(self.recipe.isTagged(tag_name))
            cw.load_pic(tag, self.dirname + '/UI/images/tag_%s_SLD.png' % tag_name)

        self.pB_add.setIcon(QIcon(self.dirname + '/UI/images/icon_add_recipe_LD.png'))
        self.pB_add.setVisible(False)
        
        self.pushMenu = QMenu(self.pB_add)
        self.pushAction = QWidgetAction(self.pushMenu)
        self.rcm = RightClickMenu(Menu(), self.recipe.name)
        self.pushAction.setDefaultWidget(self.rcm)
        self.pushMenu.addAction(self.pushAction)
        self.pB_add.setMenu(self.pushMenu)
    
    # @cw.decoratortimer(1)
    def initial_1(self):
        self.setMouseTracking(True)
        
        self.label_name.setText(self.recipe.name)
        tags = [self.label_vegan, 
                self.label_kids, 
                self.label_double, 
                self.label_lunch, 
                self.label_dinner, 
                self.label_summer, 
                self.label_winter, 
                self.label_dessert, 
                self.label_tips]
        tags_names = ['vegan', 'kids', 'double', 'midi', 'soir', 'ete', 'hiver', 'dessert', 'tips']
        for tag, tag_name in zip(tags, tags_names):
            tag.setVisible(self.recipe.isTagged(tag_name))
            if self.recipe.isTagged(tag_name):
                cw.load_pic(tag, self.dirname + '/UI/images/tag_%s_SLD.png' % tag_name)

    # @cw.decoratortimer(1)
    def initial_2(self):
        self.pB_add.setIcon(QIcon(self.dirname + '/UI/images/icon_add_recipe_LD.png'))
        self.pB_add.setVisible(False)

    @cw.decoratortimer(1)
    def initial_3(self):
        self.pushMenu = QMenu(self.pB_add)
        self.pushAction = QWidgetAction(self.pushMenu)
        self.rcm = RightClickMenu(Menu(), self.recipe.name)
        self.pushAction.setDefaultWidget(self.rcm)
        self.pushMenu.addAction(self.pushAction)
        self.pB_add.setMenu(self.pushMenu)
    

    def connect_actions(self):#TODO only on pb_add visible
        # print('action connected')
        
        self.pushMenu.aboutToShow.connect(self.on_add)
        
    def enterEvent(self, event: PySide2.QtCore.QEvent) -> None:
        self.label_name.setStyleSheet('QLabel{color:%s;}' % COLORS['#color3_dark#'])
        self.pB_add.setVisible(True)
        # self.connect_actions()
        return super().enterEvent(event)
    
    def leaveEvent(self, event: PySide2.QtCore.QEvent) -> None:
        self.label_name.setStyleSheet('QLabel{color:%s;}' % COLORS['#color1_dark#'])
        self.pB_add.setVisible(False)
        return super().leaveEvent(event)

    def on_add(self):
        # print('signal emitted')
        # self.initial_3()
        self.on_menu_request.emit(self.index)
    
    def on_update(self, menu):
        # print('update menu')
        self.rcm.on_new_menu(menu)
        #update with currentmenu
        #select corresponding line
        
        # self.pushMenu = QMenu(self.pB_add)
        # self.pushAction = QWidgetAction(self.pushMenu)
        # rcm = RightClickMenu(self.menu, self.recipe.name)
        # self.pushAction.setDefaultWidget(rcm)
        # self.pushMenu.addAction(self.pushAction)
        # self.pB_add.setMenu(self.pushMenu)