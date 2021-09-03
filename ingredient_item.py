import os
from ingredient import Ingredient
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from uid_widget import UIDWidget

class IngredientItem(UIDWidget):
    def __init__(self, ingredient:Ingredient, lw_ingredients=None, parent=None):
        super(IngredientItem, self).__init__(parent)

        self.parent_widget = self.parentWidget()
        self.lw_ingredients = lw_ingredients

        self.lbl_ing_name:QLabel
        self.lbl_ing_name = self.parent_widget.lbl_ing_name
        if ingredient.is_optional:
            self.lbl_ing_name.setText("(%s)" % ingredient.name)
        else:
            self.lbl_ing_name.setText(ingredient.name)

        self.sb_ing_qty : QSpinBox
        self.sb_ing_qty = self.parent_widget.sb_ing_qty
        self.sb_ing_qty.setValue(float(ingredient.qty))

        self.le_ing_qty_unit:QLineEdit
        self.le_ing_qty_unit = self.parent_widget.le_ing_qty_unit
        self.le_ing_qty_unit.setText(ingredient.qty_unit)

        #TODO : IMPROVE THE WAY YOU AUTOCOMPLETE UNITES
        ing_possible_units = ["c.a.s", "g", "Kg", "cl", "c.a.c"]
        completer = QCompleter(ing_possible_units)
        self.le_ing_qty_unit.setCompleter(completer)

        self.btn_remove_ing : QPushButton
        self.btn_remove_ing = self.parent_widget.btn_remove_ing
        self.btn_remove_ing.setIcon(QtGui.QIcon(os.path.dirname(__file__) + '/UI/images/icon_bin_2.png'))
        self.btn_remove_ing.clicked.connect(self.removeItemFromList)

    def removeItemFromList(self):
         for i in range(0, self.lw_ingredients.count()):
            widget:UIDWidget
            widget = self.lw_ingredients.itemWidget(self.lw_ingredients.item(i)).findChild(IngredientItem)
            if self.getUID() == widget.getUID():
                self.lw_ingredients.takeItem(i)
                break