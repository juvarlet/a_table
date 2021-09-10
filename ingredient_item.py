import os
from ingredient import Ingredient
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from uid_widget import UIDWidget

class IngredientItem(UIDWidget):
    WIDGET_EDIT_ING_MODE = "0000"
    WIDGET_SH0W_ING_MODE = "0001"

    def __init__(self, ingredient:Ingredient, lw_ingredients=None, parent=None):
        super(IngredientItem, self).__init__(parent)

        self.parent_widget = self.parentWidget()
        self.lw_ingredients = lw_ingredients
        self.saveComponents()
        self.selectWidgetMode()

        if ingredient.is_optional:
            self.lbl_ing_name.setText("(%s)" % ingredient.name)
        else:
            self.lbl_ing_name.setText(ingredient.name)
        self.lbl_ing_qty.setText(str(ingredient.qty))
        self.lbl_ing_qty_unit.setText(ingredient.qty_unit)

        #TODO : IMPROVE THE WAY YOU AUTOCOMPLETE UNITES
        ing_possible_units = ["", "c.a.s", "g", "Kg", "cl", "c.a.c"]
        completer = QCompleter(ing_possible_units)
        self.le_ing_qty_unit.setCompleter(completer)

        self.btn_remove_ing.clicked.connect(self.removeItemFromList)
        self.btn_edit_ing.clicked.connect(self.showEditWidget)
        self.btn_cancel_changes.clicked.connect(self.cancelChanges)
        self.btn_confirm_changes.clicked.connect(self.confirmChanges)

    def saveComponents(self):
        self.widget_show_ing:QWidget
        self.widget_show_ing = self.parent_widget.widget_show_ing
        self.widget_edit_ing:QWidget
        self.widget_edit_ing = self.parent_widget.widget_edit_ing
        self.lbl_ing_name:QLabel
        self.lbl_ing_name = self.parent_widget.lbl_ing_name
        self.lbl_ing_qty:QLabel
        self.lbl_ing_qty = self.parent_widget.lbl_ing_qty
        self.lbl_ing_qty_unit:QLabel
        self.lbl_ing_qty_unit = self.parent_widget.lbl_ing_qty_unit
        self.le_ing_name:QLineEdit
        self.le_ing_name = self.parent_widget.le_ing_name
        self.sb_ing_qty : QSpinBox
        self.sb_ing_qty = self.parent_widget.sb_ing_qty
        self.le_ing_qty_unit:QLineEdit
        self.le_ing_qty_unit = self.parent_widget.le_ing_qty_unit
        self.btn_remove_ing : QPushButton
        self.btn_remove_ing = self.parent_widget.btn_remove_ing
        self.btn_remove_ing.setIcon(QtGui.QIcon(os.path.dirname(__file__) + '/UI/images/icon_bin_2.png'))
        self.btn_edit_ing:QPushButton
        self.btn_edit_ing = self.parent_widget.btn_edit_ing
        self.btn_edit_ing.setIcon(QtGui.QIcon(os.path.dirname(__file__) + '/UI/images/icon_edit_2.png'))
        self.btn_cancel_changes:QPushButton
        self.btn_cancel_changes = self.parent_widget.btn_cancel_changes
        self.btn_cancel_changes.setIcon(QtGui.QIcon(os.path.dirname(__file__) + '/UI/images/icon_cancel.png'))
        self.btn_confirm_changes:QPushButton
        self.btn_confirm_changes = self.parent_widget.btn_confirm_changes
        self.btn_confirm_changes.setIcon(QtGui.QIcon(os.path.dirname(__file__) + '/UI/images/icon_ok.png'))
        self.btn_ing_is_optional:QPushButton
        self.btn_ing_is_optional = self.parent_widget.btn_ing_is_optional

    def selectWidgetMode(self, widget_code=WIDGET_SH0W_ING_MODE):
        if widget_code == self.WIDGET_SH0W_ING_MODE:
            self.widget_show_ing.show()
            self.widget_edit_ing.hide()
        elif widget_code == self.WIDGET_EDIT_ING_MODE:
            self.widget_show_ing.hide()
            self.widget_edit_ing.show()
        else:
            print("IngredientItem > selectWidgetToShow : There something wrong here !!!")


    def showEditWidget(self):
        self.selectWidgetMode(self.WIDGET_EDIT_ING_MODE)
        self.le_ing_name.setText(self.lbl_ing_name.text())
        self.sb_ing_qty.setValue(float(self.lbl_ing_qty.text()))
        self.le_ing_qty_unit.setText(self.lbl_ing_qty_unit.text())

    def cancelChanges(self):
        self.selectWidgetMode()

    def confirmChanges(self):
        self.selectWidgetMode()
        self.lbl_ing_name.setText(self.le_ing_name.text())
        self.lbl_ing_qty.setText(str(self.sb_ing_qty.value()))
        self.lbl_ing_qty_unit.setText(self.le_ing_qty_unit.text())

    def removeItemFromList(self):
         for i in range(0, self.lw_ingredients.count()):
            widget:UIDWidget
            widget = self.lw_ingredients.itemWidget(self.lw_ingredients.item(i)).findChild(IngredientItem)
            if self.getUID() == widget.getUID():
                self.lw_ingredients.takeItem(i)
                break