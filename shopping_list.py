import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon, QColor

import os
import sys
import math
import custom_widgets as cw

from line_ingredient import LineIngredient
from ingredient import Ingredient
from card_recipe import CardRecipe
from menu import Menu

UI_FILE = cw.dirname('UI') + 'shopping_list.ui'



class ShoppingList(QWidget):
    def __init__(self, ingredient_list=None, parent=None):
        super(ShoppingList, self).__init__(parent)

        self.ingredient_list = ingredient_list
        self.cards = {}
        
        self.loadUI()
        self.saveComponents()
        
        self.initial_state()
        self.connect_actions()
        self.update_modif()
    
    def loadUI(self):
        self.pW = cw.loadUI(self, UI_FILE)
    
    def saveComponents(self):
        self.dirname = cw.dirname('UI/images')
        
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
        # self.pB_sort.setIcon(QIcon(self.dirname + '/icon_filter_LD.png'))
        
        self.add_ingredient(Ingredient('example'))
        self.add_ingredient(Ingredient('example2', 10, 'kg'))
        
        if self.ingredient_list:
            self.add_ingredients(self.ingredient_list)
        
        self.tW_link_menus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_link_menus.verticalHeader().setDefaultSectionSize(200)
        self.tW_link_menus.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tW_link_menus.setIconSize(QSize(100, 200))
        self.tW_link_menus.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.tW_link_menus.setRowHeight(0,200)
        
    def connect_actions(self):
        pass
    
    def update_modif(self):
        pass

    def add_ingredient(self, ingredient: Ingredient, checked = False):
        self.lW_shopping.addItem(ingredient.name)
        line_item = self.lW_shopping.item(self.lW_shopping.count()-1)
        line_item.setSizeHint(QSize(0,35))
        line_widget = LineIngredient(ingredient, checked)
        line_widget.on_delete.connect(self.delete_line)
        self.lW_shopping.setItemWidget(line_item, line_widget)
    
    def add_ingredients(self, ingredient_list):
        #ingredient_list = [(ingredient, checked),()...]
        for ingredient, checked in ingredient_list:
            self.add_ingredient(ingredient, checked)
    
    def add_missing_information(self, recipe_name):
        self.cards[recipe_name].no_ingredient()
    
    def clear(self):
        self.lW_shopping.clear()
        self.tW_link_menus.clear()
        self.tW_link_menus.setRowCount(0)
    
    def populate_menu_list(self, recipe_list):
        columnCount = 4
        #reset table
        self.tW_link_menus.setColumnCount(0)
        self.tW_link_menus.setColumnCount(columnCount)
        self.tW_link_menus.setRowCount(0)
        self.tW_link_menus.setRowCount(math.ceil(len(recipe_list)/columnCount))
        
        #populate table with menus
        for i, recipe in enumerate(recipe_list):
            card = CardRecipe(recipe)
            qtwi = QTableWidgetItem(recipe.name)
            self.tW_link_menus.setItem(int(i/columnCount), i%columnCount, qtwi)
            self.tW_link_menus.setCellWidget(int(i/columnCount), i%columnCount, card)
            self.cards[recipe.name] = card
    
    def populate_ingredient_list(self, shopping_list):
        for ingredient_name, value in shopping_list:
            if ingredient_name != 'missing information':
                self.add_ingredient(value)
            else:
                for recipe_name in value:
                    self.add_missing_information(recipe_name)

    def update(self, menu: Menu):
        self.clear()
        recipe_list = menu.get_recipe_list(no_double=True)
        self.populate_menu_list(recipe_list)
        shopping_list = menu.get_shopping_list().items()
        self.populate_ingredient_list(shopping_list)
    
    def delete_line(self, ingredient: Ingredient):
        item = self.lW_shopping.findItems(ingredient.name, Qt.MatchExactly)[0]
        self.lW_shopping.takeItem(item)
        
        
        