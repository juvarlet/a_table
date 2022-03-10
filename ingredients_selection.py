import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtGui import QBrush, QFont, QPixmap, QIcon, QPainter, QFontMetrics, QPen


import os, sys
import custom_widgets as cw
from ingredient import Ingredient
from ingredient_item import IngredientItem
from recipe import Recipe

from stylesheet_update import COLORS


UI_FILE = cw.dirname('UI') + 'ingredients_selection.ui'

class IngredientsSelection(QWidget):
    
    def __init__(self, ingredient_list, recipe=None, title='', parent=None):
        super(IngredientsSelection, self).__init__(parent)
        
        self.ingredient_list = ingredient_list
        self.recipe = recipe
        self.title = title
        self.loadUI()
        self.saveComponents()
        self.initial_state()
        self.connect_actions()
        self.update_modif()
            
    def loadUI(self):
        self.pW = cw.loadUI(self, UI_FILE)
    
    def saveComponents(self):
        self.dirname = cw.dirname('UI/images')
        self.frame_selection: QFrame
        self.frame_selection = self.pW.frame_selection
        self.frame_action: QFrame
        self.frame_action = self.pW.frame_action
        self.lW_ingredients: QListWidget
        self.lW_ingredients = self.pW.lW_ingredients
        self.pB_ok: QPushButton
        self.pB_ok = self.pW.pB_ok
        self.pB_cancel: QPushButton
        self.pB_cancel = self.pW.pB_cancel
        self.lW_selection: QListWidget
        self.lW_selection = self.pW.lW_selection
        self.label_title: QLabel
        self.label_title = self.pW.label_title
    
    def initial_state(self):
        self.lW_ingredients.addItems(sorted([ing.name for ing in self.ingredient_list], key=str.lower))
        if self.recipe:
            self.frame_selection.setVisible(True)
            populate_ing_list(self.recipe, self.lW_selection)
            self.label_title.setText(self.recipe.name)
        else:
            self.frame_selection.setVisible(False)
        
    def connect_actions(self):
        pass

    def update_modif(self):
        pass

#generic version to adapt to any listwidget
def add_new_ingredient_to_list(ingredient:Ingredient, listWidget:QListWidget):

    def on_btn_confirm_changes_clicked_(ing_item_id, listWidget=listWidget):
        ing_item:IngredientItem
        # ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(self.lw_ingredients.count()-1)).findChild(IngredientItem)
        ing_item = listWidget.itemWidget(listWidget.item(listWidget.count()-1))
        if ing_item.getUID() == ing_item_id:
            add_new_ingredient_to_list(Ingredient(), listWidget)

    def rm_ing_item_from_list_(ing_item_id, listWidget=listWidget):
        for i in range(0, listWidget.count()):
            ing_item:IngredientItem
            # ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(i)).findChild(IngredientItem)
            ing_item = listWidget.itemWidget(listWidget.item(i))
            if ing_item_id == ing_item.getUID():
                listWidget.takeItem(i)
                break

    #TODO : handle the case were the ingredient is already in the list
    ing_item = IngredientItem(ingredient)
    ing_item.on_btn_confirm_changes_clicked.connect(on_btn_confirm_changes_clicked_)
    ing_item.on_btn_rm_item_clicked.connect(rm_ing_item_from_list_)
    if ingredient.name == "" and ingredient.unit == "" and ingredient.qty == -1:
        ing_item.selectWidgetMode(IngredientItem.WIDGET_EDIT_ING_MODE)

    list_widget_item = QListWidgetItem()
    list_widget_item.setSizeHint(QSize(0,30))
    listWidget.addItem(list_widget_item)
    listWidget.setItemWidget(list_widget_item,ing_item)

def populate_ing_list(recipe:Recipe, listWidget:QListWidget): #OK but can be improved
    if listWidget.count : #vider la liste si elle n'est pas deja vide
        listWidget.clear()
    if recipe.ing_list is None:
        return
    mand_ing_list, opt_ing_list = recipe.get_mandatory_and_optional_ing_lists()
    for ingredient in mand_ing_list + opt_ing_list:
        add_new_ingredient_to_list(ingredient, listWidget)
    
    add_new_ingredient_to_list(Ingredient(), listWidget) # Add extra line for new ing input


if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_gui = IngredientsSelection([])
    test_gui.show()
    sys.exit(app.exec_())
    