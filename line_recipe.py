import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon
import custom_widgets as cw
from right_click_menu import RightClickMenu
from stylesheet_update import COLORS
import os, sys

UI_FILE = os.path.dirname(__file__) + '/UI/line_recipe.ui'

class LineRecipe(QWidget):
    def __init__(self, recipe, menu, parent=None):
        super(LineRecipe, self).__init__(parent)

        self.loadUI()
        self.recipe = recipe
        self.menu = menu
        self.saveComponents()
        self.initial_state()
        # self.connect_actions()
    
    def loadUI(self):
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        loader = QUiLoader()
        widget = loader.load(UI_FILE)
        vlayout.addWidget(widget)
        self.setLayout(vlayout)
        self.pW = widget
    
    def saveComponents(self):
        self.dirname = os.path.dirname(__file__)

        self.label_name: QLabel
        self.label_name = self.pW.label_name
        self.label_dessert: QLabel
        self.label_dessert = self.pW.label_dessert
        self.label_double: QLabel
        self.label_double = self.pW.label_double
        self.label_kids: QLabel
        self.label_kids = self.pW.label_kids
        self.label_lunchdinner: QLabel
        self.label_lunchdinner = self.pW.label_lunchdinner
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
        
    def initial_state(self):
        self.setMouseTracking(True)
        
        self.label_name.setText(self.recipe.name)
        tags = [self.label_vegan, 
                self.label_kids, 
                self.label_double, 
                self.label_summer, 
                self.label_winter, 
                self.label_dessert, 
                self.label_tips]
        tags_names = ['vegan', 'kids', 'double', 'ete', 'hiver', 'dessert', 'tips']
        for tag, tag_name in zip(tags, tags_names):
            tag.setVisible(self.recipe.isTagged(tag_name))
            cw.load_pic(tag, self.dirname + '/UI/images/tag_%s_SLD.png' % tag_name)
        if self.recipe.isTagged('midi'):
            self.label_lunchdinner.setVisible(True)
            cw.load_pic(self.label_lunchdinner, self.dirname + '/UI/images/tag_lunch_SLD.png')
        elif self.recipe.isTagged('soir'):
            self.label_lunchdinner.setVisible(True)
            cw.load_pic(self.label_lunchdinner, self.dirname + '/UI/images/tag_dinner_SLD.png')
        else:
            self.label_lunchdinner.setVisible(False)
        self.pB_add.setIcon(QIcon(self.dirname + '/UI/images/icon_add_recipe.png'))
        self.pB_add.setVisible(False)
        
    def connect_actions(self):#TODO only on pb_add visible
        self.pB_add.clicked.connect(self.on_add)

    def enterEvent(self, event: PySide2.QtCore.QEvent) -> None:
        self.label_name.setStyleSheet('QLabel{color:%s;}' % COLORS['#color3_dark#'])
        self.pB_add.setVisible(True)
        self.connect_actions()
        return super().enterEvent(event)
    
    def leaveEvent(self, event: PySide2.QtCore.QEvent) -> None:
        self.label_name.setStyleSheet('QLabel{color:%s;}' % COLORS['#color1_dark#'])
        self.pB_add.setVisible(False)
        return super().leaveEvent(event)

    def on_add(self):
        self.pushMenu = QMenu(self.pB_add)
        self.pushAction = QWidgetAction(self.pushMenu)
        rcm = RightClickMenu(self.menu, self.recipe.name)
        self.pushAction.setDefaultWidget(rcm)
        self.pushMenu.addAction(self.pushAction)
        self.pB_add.setMenu(self.pushMenu)