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
    
    on_reset = Signal()
    on_delete = Signal()
    
    def __init__(self, ingredient: Ingredient, checked = False, parent=None):
        super(LineIngredient, self).__init__(parent)

        self.ingredient = ingredient
        self.checked = checked
        self.loadUI()
        self.saveComponents()
        
        self.initial_state()
        self.connect_actions()
        self.update_modif()
    
    def loadUI(self):
        self.pW = cw.loadUI(self, UI_FILE)
    
    def saveComponents(self):
        self.dirname = cw.dirname('UI/images')
        
        self.label_name: QLabel
        self.label_name = self.pW.label_name
        self.label_unit: QLabel
        self.label_unit = self.pW.label_unit
        self.cB_done: QCheckBox
        self.cB_done = self.pW.cB_done
        self.sB_qty: QDoubleSpinBox
        self.sB_qty = self.pW.sB_qty
        self.pB_delete: QPushButton
        self.pB_delete = self.pW.pB_delete
        self.pB_reset: QPushButton
        self.pB_reset = self.pW.pB_reset
        
    def initial_state(self):
        cw.pb_hover_stylesheet(self.pB_delete, 'icon_bin', 'icon_bin_')
        cw.pb_hover_stylesheet(self.pB_reset, 'icon_reset_LD', 'icon_reset_LD_')
        # self.pB_delete.setIcon(QIcon(self.dirname + '/icon_bin.png'))
        # self.pB_reset.setIcon(QIcon(self.dirname + '/icon_reset_LD.png'))
        self.label_name.setText(self.ingredient.name)
        self.label_unit.setText(self.ingredient.qty_unit)
        self.sB_qty.setValue(self.ingredient.qty)
        self.cB_done.setChecked(self.checked)
        
    def connect_actions(self):
        pass
    
    def update_modif(self):
        # self.sB_qty.valueChanged.connect(self.on_value_changed)
        pass

    def on_value_changed(self, new_value):
        print(str(new_value))
        self.sB_qty.setDecimals(not new_value.is_integer())