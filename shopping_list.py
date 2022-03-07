from recipe import Recipe
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
import keep_api

UI_FILE = cw.dirname('UI') + 'shopping_list.ui'

class ShoppingList(QWidget):
    
    on_gkeep = Signal()
    
    def __init__(self, parent=None):
        super(ShoppingList, self).__init__(parent)

        self.cards = {}
        self.resets = {'deletion':False}
        self.current_menu = None
        
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
        self.pB_add: QPushButton
        self.pB_add = self.pW.pB_add
        self.pB_keep: QPushButton
        self.pB_keep = self.pW.pB_keep
        
    def initial_state(self):
        cw.pb_hover_stylesheet(self.pB_send, 'icon_send', 'icon_send_')
        cw.pb_hover_stylesheet(self.pB_print, 'icon_print', 'icon_print_')
        cw.pb_hover_stylesheet(self.pB_reset, 'icon_reset_LD', 'icon_reset_LD_')
        cw.pb_hover_stylesheet(self.pB_add, 'icon_ingredient', 'icon_ingredient_')
        cw.pb_hover_stylesheet(self.pB_keep, 'icon_keep', 'icon_keep_')
        
        self.tW_link_menus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_link_menus.verticalHeader().setDefaultSectionSize(200)
        self.tW_link_menus.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tW_link_menus.setIconSize(QSize(100, 200))
        self.tW_link_menus.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.tW_link_menus.setRowHeight(0,200)
        
        self.on_reset_update()
        
    def connect_actions(self):
        self.pB_reset.clicked.connect(self.reset_all)
        self.pB_add.clicked.connect(self.on_add_empty_ingredient)
        self.pB_keep.clicked.connect(self.execute_gkeep_process)
    
    def update_modif(self):
        pass

    def add_ingredient(self, ingredient: Ingredient, checked=False, user_input=False):
        self.lW_shopping.addItem(ingredient.name)
        
        line_item = self.lW_shopping.item(self.lW_shopping.count()-1)
        line_item.setSizeHint(QSize(0,35))
        
        line_widget = LineIngredient(ingredient, checked, user_input)
        line_widget.on_delete.connect(self.delete_line)
        line_widget.on_reset.connect(self.update_reset)
        line_widget.on_search.connect(self.update_cards_status)
        self.lW_shopping.setItemWidget(line_item, line_widget)
        
        self.resets[ingredient.name] = False
    
    def on_add_empty_ingredient(self):
        ingredient = Ingredient()
        self.add_ingredient(ingredient, checked=False, user_input=True)
        self.lW_shopping.scrollToBottom()
    
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
            card.on_list_ingredients.connect(self.on_select_ingredients)
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

    def update(self, menu: Menu=None):
        self.clear()
        if menu: #new current menu assigned to this object
            self.current_menu = menu
        elif self.current_menu: #using previous menu assigned
            menu = self.current_menu
        else:
            return
        recipe_list = menu.get_recipe_list(no_double=True)
        self.populate_menu_list(recipe_list)
        shopping_list = menu.get_shopping_list().items()
        self.populate_ingredient_list(shopping_list)
        self.on_reset_update()
    
    def delete_line(self, ingredient: Ingredient):
        item = self.lW_shopping.findItems(ingredient.name, Qt.MatchExactly)[0]
        row = self.lW_shopping.row(item)
        self.lW_shopping.takeItem(row)
        
        self.resets.pop(ingredient.name)
        self.resets['deletion'] = True
        self.on_reset_update()
    
    def update_reset(self, ingredient: Ingredient, visible: bool):
        self.resets[ingredient.name] = visible
        self.on_reset_update()
        
    def on_reset_update(self):
        self.pB_reset.setVisible(sum(self.resets.values()))
    
    def reset_all(self):
        self.resets = {'deletion':False}
        self.update()
    
    def update_cards_status(self, ingredient: Ingredient):
        for card in self.cards.values():
            if card.recipe.hasIngredient(ingredient.name):
                highlight = bool(sum([line.selected for line in self.get_linked_LineIngredients(card)]))
                card.apply_status(highlight)
    
    def get_line_widget(self, ingredient: Ingredient) -> LineIngredient:
        qlwi_list = [self.lW_shopping.item(r) for r in range(self.lW_shopping.count())]
        for qlwi in qlwi_list:
            if qlwi.text() == ingredient.name:
                return self.lW_shopping.itemWidget(qlwi)
        
        return None
    
    def get_all_line_widgets(self):
        return [self.lW_shopping.itemWidget(qlwi) 
                for qlwi in [self.lW_shopping.item(r) 
                             for r in range(self.lW_shopping.count())
                             ]
                ]
    
    def get_linked_LineIngredients(self, card: CardRecipe):
        return [self.get_line_widget(ingredient) for ingredient in card.recipe.ing_list]
    
    def on_select_ingredients(self, card: CardRecipe, boolean):
        for line in self.get_linked_LineIngredients(card):
            if line:#in case ingredient has been deleted
                line.select(boolean)
    
    def execute_gkeep_process(self):
        self.on_gkeep.emit()
    
