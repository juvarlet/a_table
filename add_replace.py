import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon

import os, sys

CARD_UI_FILE = os.path.dirname(__file__) + '/UI/add_replace.ui'

LINE_UI_FILE = os.path.dirname(__file__) + '/UI/line_label_button.ui'

class AddReplace(QWidget):
    def __init__(self, recipes, name, parent=None):
        super(AddReplace, self).__init__(parent)

        self.loadUI()
        self.recipes = recipes
        self.name = name
        self.line_widgets = []
        self.saveComponents()
        self.initial_state()
        self.connect_actions()
        

    def loadUI(self):
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        loader = QUiLoader()
        widget = loader.load(CARD_UI_FILE)
        vlayout.addWidget(widget)
        self.setLayout(vlayout)
        self.pW = widget
        
    def saveComponents(self):
        # self.dirname = os.path.dirname(__file__)
        self.dirname = os.path.dirname(os.path.abspath(__file__))

        self.lW: QListWidget
        self.lW = self.pW.lW
        self.pB_add: QPushButton
        self.pB_add = self.pW.pB_add
        self.pB_replace: QPushButton
        self.pB_replace = self.pW.pB_replace

    def initial_state(self):
        for recipe in self.recipes:
            self.add_recipe(str(recipe))

        self.pB_add.setIcon(QIcon(self.dirname + '/UI/images/icon_add_recipe_LD.png'))
        self.pB_add.setToolTip("Ajouter '%s'" % self.name)
        self.pB_replace.setIcon(QIcon(self.dirname + '/UI/images/icon_reset_all_LD.png'))
        self.pB_replace.setToolTip("Remplacer tout par '%s'" % self.name)
        
    def connect_actions(self):
        self.pB_add.clicked.connect(self.on_add_recipe)
        self.pB_replace.clicked.connect(self.on_replace_all)
    
    def on_add_recipe(self):
        self.add_recipe(self.name)
    
    def on_replace_all(self):
        self.lW.clear()
        self.line_widgets = []
        self.on_add_recipe()
    
    def create_list_widget(self, name):
        loader = QUiLoader()
        widget = loader.load(LINE_UI_FILE)
        widget.label.setText(name)
        widget.pB_reset.setIcon(QIcon(self.dirname + '/UI/images/icon_reset_LD.png'))
        widget.pB_reset.setToolTip("Remplacer par '%s'" % self.name)
        widget.pB_reset.clicked.connect(lambda: widget.label.setText(self.name))
        self.line_widgets.append(widget)
        return widget
    
    def add_line(self, line_widget):
        qlwi = QListWidgetItem()
        qlwi.setSizeHint(QSize(35,35))
        self.lW.addItem(qlwi)
        self.lW.setItemWidget(qlwi, line_widget)
    
    def add_recipe(self, name):
        widget = self.create_list_widget(name)
        self.add_line(widget)

    def get_recipes(self):

        return [self.lW.itemWidget(
            self.lW.item(i)).label.text() 
                for i in range(self.lW.count()
                               )]

    def update_recipes(self, stack):
        self.recipes = stack
        for i, line_widget in enumerate(self.line_widgets):
            if i < len(self.recipes):
                line_widget.label.setText(str(self.recipes[i]))
            else:#if recipe has been removed
                self.line_widgets = self.line_widgets[:-1]
                self.lW.takeItem(self.lW.count()-1)
                
        
        for i, recipe in enumerate(self.recipes):#if recipe has been added
            if i >= len(self.line_widgets):
                self.add_recipe(recipe)