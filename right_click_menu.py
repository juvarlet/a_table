import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon

import os, sys
from add_replace import AddReplace
import custom_widgets as cw
from recipe import Recipe

UI_FILE = os.path.dirname(__file__) + '/UI/right_click_menu.ui'

class RightClickMenu(QWidget):
    
    on_close = Signal()
    on_update = Signal()
    
    def __init__(self, menu, name, parent=None):
        super(RightClickMenu, self).__init__(parent)
        
        self.loadUI()
        self.table = menu.table
        self.headers = [m[0] for m in menu.full_menu()]
        self.name = name
        self.card_widgets = []
        
        self.minw = int(self.screen().size().width()*0.55)
        minh = int(self.screen().size().height()*0.4)
        
        # self.dimensions = {'min' : QSize(220, 45), 
        #                    'max' : QSize(500, 390)}
        self.dimensions = QSize(self.minw + 57, minh)        
        self.saveComponents()
        self.initial_state()
        self.connect_actions()

    def loadUI(self):
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        loader = QUiLoader()
        widget = loader.load(UI_FILE)
        vlayout.addWidget(widget)
        self.setLayout(vlayout)
        self.pW = widget
        
    def saveComponents(self):
        # self.dirname = os.path.dirname(__file__)
        self.dirname = os.path.dirname(os.path.abspath(__file__))

        self.frame_actions: QFrame
        self.frame_actions = self.pW.frame_actions
        self.frame_table: QFrame
        self.frame_table = self.pW.frame_table
        self.frame_valid: QFrame
        self.frame_valid = self.pW.frame_valid
        self.frame_title: QFrame
        self.frame_title = self.pW.frame_title
        self.pB_ok: QPushButton
        self.pB_ok = self.pW.pB_ok
        self.pB_cancel: QPushButton
        self.pB_cancel = self.pW.pB_cancel
        self.pB_reset: QPushButton
        self.pB_reset = self.pW.pB_reset
        self.tW_menus: QTableWidget
        self.tW_menus = self.pW.tW_menus
        self.label_lunch: QLabel
        self.label_lunch = self.pW.label_lunch
        self.label_dinner: QLabel
        self.label_dinner = self.pW.label_dinner
        self.label_carte: QLabel
        self.label_carte = self.pW.label_carte
    
    def initial_state(self):
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.adjustSize()

        
        self.tW_menus.setRowCount(2)
        self.tW_menus.setColumnCount(len(self.table)/2)
        # minw = len(self.table)/2 * 150
        
        
        # self.dimensions['max'] = QSize(minw+57, self.dimensions['max'].height())
        # self.dimensions['max'] = QSize(minw+57, minh)
        
        self.tW_menus.setMinimumWidth(self.minw)
        self.tW_menus.setHorizontalHeaderLabels(self.headers)
        self.tW_menus.verticalHeader().hide()

        self.tW_menus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_menus.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, stack in enumerate(self.table):
            if type(stack) is Recipe:
                card_widget = AddReplace([stack], self.name)
            elif type(stack) is list:
                card_widget = AddReplace(stack, self.name)
            self.card_widgets.append(card_widget)
            # widget.show()
            qtwi = QTableWidgetItem('')
            self.tW_menus.setItem(i%2, int(i/2), qtwi)
            self.tW_menus.setCellWidget(i%2, int(i/2), card_widget)
        
        # self.tW_menus.cellWidget(0,0).show()
        self.pB_ok.setIcon(QIcon(self.dirname + '/UI/images/icon_check_LD.png'))
        self.pB_cancel.setIcon(QIcon(self.dirname + '/UI/images/icon_cancel_LD.png'))
        self.pB_reset.setIcon(QIcon(self.dirname + '/UI/images/icon_back_LD.png'))
        cw.load_pic(self.label_lunch, self.dirname + '/UI/images/tag_midi_SLD.png')
        cw.load_pic(self.label_dinner, self.dirname + '/UI/images/tag_soir_SLD.png')
        cw.load_pic(self.label_carte, self.dirname + '/UI/images/icon_menu_SLD.png')
                
    def connect_actions(self):
        self.pB_cancel.clicked.connect(self.on_cancel)
        self.pB_ok.clicked.connect(self.on_validate)
        self.pB_reset.clicked.connect(self.update_qtable)

    def on_cancel(self):
        self.update_qtable()
        self.on_close.emit()

    def on_validate(self):
        new_table = []
        for c in range(self.tW_menus.columnCount()):
            for r in range(self.tW_menus.rowCount()):
                recipes = self.tW_menus.cellWidget(r, c).get_recipes()
                new_table.append(recipes)
        self.table = new_table

        for i, stack in enumerate(self.table):
            if type(stack) is Recipe:
                stack = [stack]
            recipes_str = ' | '.join([str(r) for r in stack])
            print('%i-%s' % (i, recipes_str))
        # self.update_qtable()
        self.on_update.emit()


    def update_qtable(self):
        for i, stack in enumerate(self.table):
            if type(stack) is Recipe:
                self.card_widgets[i].update_recipes([stack])
            elif type(stack) is list:
                self.card_widgets[i].update_recipes(stack)
    
    def on_new_menu(self, menu):
        self.card_widgets = []
        self.table = menu.table
        self.headers = [m[0] for m in menu.full_menu()]
        self.tW_menus.setColumnCount(len(self.table)/2)
        self.tW_menus.setHorizontalHeaderLabels(self.headers)
        for i, stack in enumerate(self.table):
            if type(stack) is Recipe:
                card_widget = AddReplace([stack], self.name)
            elif type(stack) is list:
                card_widget = AddReplace(stack, self.name)
            self.card_widgets.append(card_widget)
            qtwi = QTableWidgetItem('')
            self.tW_menus.setItem(i%2, int(i/2), qtwi)
            self.tW_menus.setCellWidget(i%2, int(i/2), card_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    table = [['r1'],
            ['r2'],
            ['r3'],
            ['r4'],
            ['r5','r51','r52'],
            ['r6'],
            ['r7'],
            ['r8'],
            ['r9'],
            ['r10','r101'],
            ['r11'],
            ['r12'],
            ['r13'],
            ['r14']]
    myGUI = RightClickMenu(table, 'recette1')
    myGUI.show()
    # myGUI.window().setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    # myGUI.window().adjustSize()
    sys.exit(app.exec_())