import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon, QColor

import os
import sys
import custom_widgets as cw
import pyautogui
from stylesheet_update import COLORS

UI_FILE = cw.dirname('UI') + 'history.ui'

class History(QWidget):
    
    on_switch_to_recipe = Signal(str)
    # on_reset = Signal()
    on_confirm = Signal()
    
    def __init__(self, history = [], new_history = [], parent=None):
        super(History, self).__init__(parent)

        self.history = history
        self.recipeMultiSelection = []
        self.colors = COLORS
        self.dirname = cw.dirname('UI/images')
        self.loadUI()
        self.saveComponents()
        
        self.initial_state()
        self.connect_actions()
        
        self.selectWidgetMode(new_history)
    
    def loadUI(self):
        self.pW = cw.loadUI(self, UI_FILE)
    
    def saveComponents(self):
        self.tW_history: QTableWidget
        self.tW_history = self.pW.tW_history
        self.frame_confirm: QFrame
        self.frame_confirm = self.pW.frame_confirm
        self.pB_ok: QPushButton
        self.pB_ok = self.pW.pB_ok
        self.pB_cancel: QPushButton
        self.pB_cancel = self.pW.pB_cancel
        self.label_confirm: QLabel
        self.label_confirm = self.pW.label_confirm
        self.label_warning: QLabel
        self.label_warning = self.pW.label_warning
        self.label_deco_1: QLabel
        self.label_deco_1 = self.pW.label_deco_1
        self.label_deco_2: QLabel
        self.label_deco_2 = self.pW.label_deco_2
        self.label_deco_3: QLabel
        self.label_deco_3 = self.pW.label_deco_3
        self.label_deco_4: QLabel
        self.label_deco_4 = self.pW.label_deco_4
        self.label_deco_5: QLabel
        self.label_deco_5 = self.pW.label_deco_5
        self.label_deco_6: QLabel
        self.label_deco_6 = self.pW.label_deco_6
        self.label_deco_7: QLabel
        self.label_deco_7 = self.pW.label_deco_7
        self.label_deco_8: QLabel
        self.label_deco_8 = self.pW.label_deco_8
        self.label_deco_9: QLabel
        self.label_deco_9 = self.pW.label_deco_9
        self.label_deco_10: QLabel
        self.label_deco_10 = self.pW.label_deco_10
        self.label_deco_11: QLabel
        self.label_deco_11 = self.pW.label_deco_11
        self.label_deco_12: QLabel
        self.label_deco_12 = self.pW.label_deco_12
        self.label_deco_13: QLabel
        self.label_deco_13 = self.pW.label_deco_13
        self.label_deco_14: QLabel
        self.label_deco_14 = self.pW.label_deco_14
        self.label_deco_15: QLabel
        self.label_deco_15 = self.pW.label_deco_15
        self.label_deco_16: QLabel
        self.label_deco_16 = self.pW.label_deco_16
    
    def initial_state(self):
        self.setWindowTitle('Historique')
        self.setWindowIcon(QIcon(self.dirname + 'icon_plate_3colors.png'))
        self.setWindowModality(Qt.WindowModal)
        
        self.tW_history.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_history.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_history.setColumnCount(2)
        self.tW_history.setContextMenuPolicy(Qt.CustomContextMenu)
        
        labels = [self.label_deco_1,self.label_deco_2,self.label_deco_3,self.label_deco_4,
                  self.label_deco_5,self.label_deco_6,self.label_deco_7,self.label_deco_8,
                  self.label_deco_9,self.label_deco_10,self.label_deco_11,self.label_deco_12,
                  self.label_deco_13,self.label_deco_14,self.label_deco_15,self.label_deco_16]
        
        for i, label in enumerate(labels):
            cw.load_pic(label, self.dirname + 'icon_deco_%s.png' % (i+1))
        
        cw.load_pic(self.label_warning, self.dirname + 'icon_fork_X_3colors_t_LD.png')
        self.pB_cancel.setIcon(QIcon(self.dirname + 'icon_cancel.png'))
        self.pB_ok.setIcon(QIcon(self.dirname + 'icon_ok.png'))
        
        self.reset_history()
    
    def connect_actions(self):
        self.pB_ok.clicked.connect(self.on_confirm_history_update)
        self.pB_cancel.clicked.connect(self.on_cancel_history_update)
        self.tW_history.cellDoubleClicked.connect(self.on_history_recipe_selection)
        self.tW_history.customContextMenuRequested.connect(self.on_history_right_click)
        
    def selectWidgetMode(self, new_history=[]):
        if len(new_history) > 0:
            self.frame_confirm.show()
            #populate table with new history entries
            self.pB_ok.click() #auto-save, no confirmation
        else:
            self.frame_confirm.hide()
            self.reset_history()
    
    def on_confirm_history_update(self):
        print('confirm')
        
        #update rows where recipe has been replaced
        for i in range(self.tW_history.rowCount()):
            qtwi_lunch = self.tW_history.item(i, 0)
            qtwi_dinner = self.tW_history.item(i, 1)
            r,g,b = tuple(int(self.colors['#color2#'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            if qtwi_lunch.textColor().getRgb() == (r,g,b,255):
                # print(i,qtwi_lunch.textColor().getRgb())
                #take new entry
                lunch_recipe_name = qtwi_lunch.text().split(' -> ')[-1]
                dinner_recipe_name = qtwi_dinner.text().split(' -> ')[-1]
                qtwi_lunch.setText(lunch_recipe_name)
                qtwi_dinner.setText(dinner_recipe_name)
                #reset color
                qtwi_lunch.setTextColor(QColor(self.colors['#color1_dark#']))
                qtwi_dinner.setTextColor(QColor(self.colors['#color1_dark#']))
        
        #backup file
        self.on_confirm.emit()
        self.selectWidgetMode()
        # self.reset_history()
        
    
    def on_cancel_history_update(self):
        print('cancel')
        self.selectWidgetMode()
        # self.reset_history()
        # self.on_reset.emit()
    
    def on_history_recipe_selection(self, row, column):
        if self.frame_confirm.isHidden():#no effect when waiting for user confirmation
            recipes = self.tW_history.item(row, column).text().split(' | ')

            if len(recipes) == 1:
                recipe_name = recipes[0]
                self.switch_to_recipe(recipe_name)
            else:
                #display context menu with choices
                self.recipeMultiSelection = recipes
                pyautogui.click(button='right')
    
    def switch_to_recipe(self, recipe_name):
        self.on_switch_to_recipe.emit(recipe_name)
    
    def on_history_right_click(self, pos):
        if self.recipeMultiSelection != []:
            globalPos = self.tW_history.mapToGlobal(pos)
            
            right_click_menu = QMenu(self)
            right_click_menu.setToolTipsVisible(True)
            right_click_menu.setStyleSheet('QWidget{color:%s;selection-color:%s;}' % 
                                        (self.colors['#color1_dark#'], self.colors['#color3_dark#']))
            
            mapper = QSignalMapper(self)
            
            for recipe_name in self.recipeMultiSelection:
                action = QAction(right_click_menu)
                action.setText(recipe_name)
                mapper.setMapping(action, recipe_name)
                action.triggered.connect(mapper.map)
                right_click_menu.addAction(action)
            
            self.recipeMultiSelection = []
            
            mapper.mappedString.connect(self.switch_to_recipe)
            right_click_menu.exec_(globalPos)
    
    def on_save_menu(self, new_history):
        self.reset_history()
        #get current header labels
        verticalHeader_labels = [self.tW_history.verticalHeaderItem(r).text() 
                                 for r in range(self.tW_history.rowCount())]
        
        
        for history in new_history:
            date_text, lunch_recipe_name, dinner_recipe_name, index = history
            
            if index != -1:
                if date_text in verticalHeader_labels:
                    qtwi_lunch = self.tW_history.item(index, 0)
                    qtwi_dinner = self.tW_history.item(index, 1)
                    qtwi_lunch.setText(qtwi_lunch.text() + ' -> %s' % lunch_recipe_name)
                    qtwi_dinner.setText(qtwi_dinner.text() + ' -> %s' % dinner_recipe_name)
                else:
                    verticalHeader_labels.insert(index, date_text)
                    self.tW_history.insertRow(index)
                    qtwi_lunch = QTableWidgetItem(lunch_recipe_name)
                    qtwi_dinner = QTableWidgetItem(dinner_recipe_name)
                    self.tW_history.setItem(index, 0, qtwi_lunch)
                    self.tW_history.setItem(index, 1, qtwi_dinner)

                
            else:
                self.tW_history.insertRow(self.tW_history.rowCount())
                qtwi_lunch = QTableWidgetItem(lunch_recipe_name)
                qtwi_dinner = QTableWidgetItem(dinner_recipe_name)
                self.tW_history.setItem(self.tW_history.rowCount()-1, 0, qtwi_lunch)
                self.tW_history.setItem(self.tW_history.rowCount()-1, 1, qtwi_dinner)
                verticalHeader_labels.append(date_text)


            qtwi_lunch.setTextColor(QColor(self.colors['#color2#']))
            qtwi_dinner.setTextColor(QColor(self.colors['#color2#']))
        
        self.tW_history.setVerticalHeaderLabels(verticalHeader_labels)
        self.tW_history.scrollToItem(self.tW_history.item(self.tW_history.rowCount()-1, 0), QAbstractItemView.PositionAtTop)
        # self.selectWidgetMode(new_history)
    
    def reset_history(self):
        self.tW_history.clear()
        self.tW_history.setHorizontalHeaderLabels(['Midi', 'Soir'])
        self.tW_history.setRowCount(len(self.history))
        self.tW_history.setVerticalHeaderLabels([h[0] for h in self.history])
        # self.tW_history.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.tW_history.resizeColumnsToContents()
        for i, day in enumerate(self.history):
            date, lunch, dinner = day
            self.tW_history.setItem(i, 0, QTableWidgetItem(lunch))
            self.tW_history.setItem(i, 1, QTableWidgetItem(dinner))

        self.tW_history.scrollToBottom()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    myGUI = History()
    myGUI.show()
    
    sys.exit(app.exec_())