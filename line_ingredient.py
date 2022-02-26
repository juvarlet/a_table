from unicodedata import name
import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon, QColor
from PySide2.QtWebEngineWidgets import QWebEngineView

import os
import sys
import custom_widgets as cw
from ingredient import Ingredient

UI_FILE = cw.dirname('UI') + 'line_ingredient.ui'

class LineIngredient(QWidget):
    
    on_reset = Signal(Ingredient, bool)
    on_delete = Signal(Ingredient)
    on_search = Signal(Ingredient)
    
    def __init__(self, ingredient: Ingredient, checked=False, user_input=False, parent=None):
        super(LineIngredient, self).__init__(parent)

        self.ingredient = ingredient
        self.checked = checked
        self.user_input = user_input
        self.selected = False
        self.loadUI()
        self.saveComponents()
        
        self.initial_state()
        self.connect_actions()
        self.update_modif()
    
    def loadUI(self):
        self.pW = cw.loadUI(self, UI_FILE)
    
    def saveComponents(self):
        self.dirname = cw.dirname('UI/images')
        
        self.lE_name: QLineEdit
        self.lE_name = self.pW.lE_name
        self.lE_unit: QLineEdit
        self.lE_unit = self.pW.lE_unit
        self.cB_done: QCheckBox
        self.cB_done = self.pW.cB_done
        self.sB_qty: QDoubleSpinBox
        self.sB_qty = self.pW.sB_qty
        self.pB_delete: QPushButton
        self.pB_delete = self.pW.pB_delete
        self.pB_reset: QPushButton
        self.pB_reset = self.pW.pB_reset
        self.pB_search: QPushButton
        self.pB_search = self.pW.pB_search
        self.frame: QFrame
        self.frame = self.pW.frame
        
    def initial_state(self):
        self.setMouseTracking(True)
        
        cw.pb_hover_stylesheet(self.pB_delete, 'icon_bin', 'icon_bin_')
        cw.pb_hover_stylesheet(self.pB_reset, 'icon_reset_LD', 'icon_reset_LD_')
        cw.pb_hover_stylesheet(self.pB_search, 'icon_search', 'icon_search_')
        # self.pB_delete.setIcon(QIcon(self.dirname + '/icon_bin.png'))
        # self.pB_reset.setIcon(QIcon(self.dirname + '/icon_reset_LD.png'))
        self.lE_name.setText(self.ingredient.name)
        self.lE_unit.setText(self.ingredient.unit)
        self.sB_qty.setValue(self.ingredient.qty)
        self.cB_done.setChecked(self.checked)
        self.pB_reset.hide()
        self.pB_search.setVisible(not self.user_input)
        
    def connect_actions(self):
        self.pB_reset.clicked.connect(self.reset)
        self.pB_delete.clicked.connect(self.delete)
        self.pB_search.clicked.connect(self.search)
    
    def update_modif(self):
        # self.sB_qty.valueChanged.connect(self.on_value_changed)
        self.cB_done.stateChanged.connect(self.check_style)
        self.lE_name.textChanged.connect(self.on_modif)
        self.lE_unit.textChanged.connect(self.on_modif)
        self.sB_qty.valueChanged.connect(self.on_modif)

    def enterEvent(self, event: PySide2.QtCore.QEvent) -> None:
        self.frame.setStyleSheet('''
                           QFrame#frame{
                               background-color: #ffe0ad;
                               border-width:2px;
                               border-radius:5px;
                               border-color: #ffe0ad;
                           }
                           
                           ''')
        return super().enterEvent(event)

    def leaveEvent(self, event: PySide2.QtCore.QEvent) -> None:
        self.frame.setStyleSheet('''
                           QFrame#frame{
                               background-color: transparent;
                               border-width:2px;
                               border-radius:5px;
                               border-color: transparent;
                           }
                           
                           ''')
        return super().leaveEvent(event)
    
    def on_value_changed(self, new_value):
        print(str(new_value))
        self.sB_qty.setDecimals(not new_value.is_integer())
    
    def check_style(self):
        self.on_modif()
        self.checked = self.cB_done.isChecked()
        if self.cB_done.isChecked():
            self.sB_qty.setEnabled(False)
            self.lE_name.setStyleSheet('''
                            QLineEdit#lE_name{
                                color:#ffc05c;
                            }
                            ''')
            self.lE_unit.setStyleSheet('''
                            QLineEdit#lE_unit{
                                color:#ffc05c;
                            }
                            ''')
            self.sB_qty.setStyleSheet('''
                            QDoubleSpinBox#sB_qty{
                                font: bold 18px;
                                background-color: #ffe0ad;
                                border-width: 0px;
                                color:#ffc05c;
                            }
                            QDoubleSpinBox#sB_qty::up-button{
                                border:none;
                            }
                            ''')
        else:
            self.sB_qty.setEnabled(True)
            self.lE_name.setStyleSheet('''
                            QLineEdit#lE_name{
                                color:#1a5d75;
                            }
                            ''')
            self.lE_unit.setStyleSheet('''
                            QLineEdit#lE_unit{
                                color:#1a5d75;
                            }
                            ''')
            self.sB_qty.setStyleSheet('''
                            QDoubleSpinBox#sB_qty{
                                font: bold 18px;
                                background-color: #ffe0ad;
                                border-width: 0px;
                                color:#1a5d75;
                            }
                            QDoubleSpinBox#sB_qty::up-button{
                                border:none;
                            }
                            ''')
    
    def on_modif(self):
        isModified = self.lE_name.text() != self.ingredient.name
        isModified += self.lE_unit.text() != self.ingredient.unit
        isModified += self.sB_qty.value() != self.ingredient.qty
        isModified += self.cB_done.isChecked() != self.checked
        self.pB_reset.setVisible(isModified and not self.user_input)
        self.on_reset.emit(self.ingredient, isModified)
    
    def reset(self):
        self.lE_name.setText(self.ingredient.name)
        self.lE_unit.setText(self.ingredient.unit)
        self.sB_qty.setValue(self.ingredient.qty)
        self.cB_done.setChecked(self.checked)
        self.pB_search.setChecked(False)
        self.on_modif()
    
    def delete(self):
        self.on_delete.emit(self.ingredient)
    
    def search(self):
        self.selected = self.pB_search.isChecked()
        self.on_search.emit(self.ingredient)
    
    def select(self, boolean):
        self.pB_search.setChecked(boolean)
        self.search()

    def toIngredient(self):
        #create new ingredient based on current texts
        name = self.lE_name.text()
        qty = self.sB_qty.value()
        unit = self.lE_unit.text()
        return Ingredient(name, qty, unit)