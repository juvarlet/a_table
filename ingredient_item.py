import os
from ingredient import Ingredient
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from uid_widget import UIDWidget

# UI_FILE = os.path.dirname(__file__) + '/UI/ingredient_item.ui'
UI_FILE = os.path.dirname(os.path.abspath(__file__)) + '/UI/ingredient_item.ui'

class IngredientItem(UIDWidget):
    WIDGET_EDIT_ING_MODE = "0000"
    WIDGET_SH0W_ING_MODE = "0001"

    on_btn_confirm_changes_clicked = Signal(str)
    on_btn_rm_item_clicked = Signal(str)

    # def __init__(self, ingredient:Ingredient, lw_ingredients=None, parent=None):
    def __init__(self, ingredient:Ingredient, parent=None):
        super(IngredientItem, self).__init__(parent)

        self.loadUI()
        # self.lw_ingredients = lw_ingredients
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
    
    def loadUI(self):
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        widget = QUiLoader().load(UI_FILE)
        vlayout.addWidget(widget)
        self.setLayout(vlayout)
        self.parent_widget = widget
    
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
        ing_name = self.lbl_ing_name.text()
        if ing_name[0] == '(' and ing_name[-1] == ')' :
            self.btn_ing_is_optional.setChecked(True)
            self.le_ing_name.setText(ing_name[1:-1])
        else:
            self.btn_ing_is_optional.setChecked(False)
            self.le_ing_name.setText(self.lbl_ing_name.text())
        self.sb_ing_qty.setValue(float(self.lbl_ing_qty.text()))
        self.le_ing_qty_unit.setText(self.lbl_ing_qty_unit.text())

    def cancelChanges(self):
        if not self.isCurrentIngredientEmpty():
            self.selectWidgetMode()
        #else:
        #   display warning message ?

    def confirmChanges(self):
        if not self.isNewIngredientEmpty():
            self.selectWidgetMode()
            if self.btn_ing_is_optional.isChecked():
                self.lbl_ing_name.setText('(' + self.le_ing_name.text() + ')')
            else :    
                self.lbl_ing_name.setText(self.le_ing_name.text())
            self.lbl_ing_qty.setText(str(self.sb_ing_qty.value()))
            self.lbl_ing_qty_unit.setText(self.le_ing_qty_unit.text())

            self.on_btn_confirm_changes_clicked.emit(self.getUID())
        #else:
        #   display warning message ?
    
    def removeItemFromList(self):
        self.on_btn_rm_item_clicked.emit(self.getUID())

    def isCurrentIngredientEmpty(self):
        if self.lbl_ing_name.text() == '' or self.lbl_ing_qty.text() == '0':
            return True
        return False

    def isNewIngredientEmpty(self):
        if self.le_ing_name.text() == '' or self.sb_ing_qty.value() == 0:
            return True
        return False