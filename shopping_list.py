import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon, QColor
from PySide2.QtWebEngineWidgets import QWebEngineView

import os
import sys
import custom_widgets as cw

from line_ingredient import LineIngredient
from ingredient import Ingredient


UI_FILE = cw.dirname('UI') + 'shopping_list.ui'



class ShoppingList(QWidget):
    def __init__(self, ingredient_list=None, parent=None):
        super(ShoppingList, self).__init__(parent)

        self.ingredient_list = ingredient_list
        
        self.loadUI()
        self.saveComponents()
        
        self.initial_state()
        self.connect_actions()
        self.update_modif()
    
    def loadUI(self):
        self.pW = cw.loadUI(self, UI_FILE)
    
    def saveComponents(self):
        self.dirname = cw.dirname('UI/images')
        
        self.label_icon: QLabel
        self.label_icon = self.pW.label_icon
        self.lW_shopping: QListWidget
        self.lW_shopping = self.pW.lW_shopping
        self.tW_link_menus: QTableWidget
        self.tW_link_menus = self.pW.tW_link_menus
        self.pB_print: QPushButton
        self.pB_print = self.pW.pB_print
        self.pB_reset: QPushButton
        self.pB_reset = self.pW.pB_reset
        self.pB_send: QPushButton
        self.pB_send = self.pW.pB_send
        self.pB_sort: QPushButton
        self.pB_sort = self.pW.pB_sort
        
    def initial_state(self):
        cw.pb_hover_stylesheet(self.pB_send, 'icon_send', 'icon_send_')
        cw.pb_hover_stylesheet(self.pB_print, 'icon_print', 'icon_print_')
        cw.pb_hover_stylesheet(self.pB_reset, 'icon_reset_LD', 'icon_reset_LD_')
        cw.pb_hover_stylesheet(self.pB_sort, 'icon_filter_LD', 'icon_filter_LD_')
        cw.load_pic(self.label_icon, self.dirname + 'icon_list.png')
        # self.pB_sort.setIcon(QIcon(self.dirname + '/icon_filter_LD.png'))
        
        self.add_ingredient(Ingredient('example'))
        self.add_ingredient(Ingredient('example2', 10, 'kg'))
        
        if self.ingredient_list:
            self.add_ingredients(self.ingredient_list)
        
    def connect_actions(self):
        pass
    
    def update_modif(self):
        pass

    def add_ingredient(self, ingredient: Ingredient, checked = False):
        self.lW_shopping.addItem(ingredient.name)
        line_item = self.lW_shopping.item(self.lW_shopping.count()-1)
        line_item.setSizeHint(QSize(0,35))
        line_widget = LineIngredient(ingredient, checked)
        self.lW_shopping.setItemWidget(line_item, line_widget)
    
    def add_ingredients(self, ingredient_list):
        #ingredient_list = [(ingredient, checked),()...]
        for ingredient, checked in ingredient_list:
            self.add_ingredient(ingredient, checked)