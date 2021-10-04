import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon


import os
import custom_widgets as cw
import menu
import recipe_db
from stylesheet_update import COLORS

UI_FILE = os.path.dirname(__file__) + '/UI/stacked_recipes.ui'

class StackedRecipes(QWidget):
    
    on_enter_recipe_stack = Signal(str)
    on_lock_for_edition = Signal([str,bool])
    on_update_current_menu = Signal([list, int, int])
    
    def __init__(self, recipe_list, recipe_db = None, id = '000', parent=None):
        super(StackedRecipes, self).__init__(parent)
        
        self.loadUI()
        self.recipe_list = recipe_list
        self.recipe_db = recipe_db
        self.id = id
        self.saveComponents()
        self.initial_state()
        self.connect_actions()
        self.setObjectName('stack')
        
    def loadUI(self):
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        widget = QUiLoader().load(UI_FILE)
        vlayout.addWidget(widget)
        self.setLayout(vlayout)
        self.pW = widget
        
    def saveComponents(self):
        self.dirname = os.path.dirname(__file__)
        self.pB_add: QPushButton
        self.pB_add = self.pW.pB_add
        self.pB_delete: QPushButton
        self.pB_delete = self.pW.pB_delete
        self.pB_next: QPushButton
        self.pB_next = self.pW.pB_next
        self.pB_edit: QPushButton
        self.pB_edit = self.pW.pB_edit
        self.label_image: QLabel
        self.label_image = self.pW.label_image
        self.label_title: QLabel
        self.label_title = self.pW.label_title
        self.frame_card: QFrame
        self.frame_card = self.pW.frame_card
        self.frame_buttons: QFrame
        self.frame_buttons = self.pW.frame_buttons
        self.hL: QHBoxLayout
        self.hL = self.pW.hL
        self.comboBox: QComboBox
        self.comboBox = self.pW.comboBox
    
    def initial_state(self):
        self.colors = COLORS
        
        self.frame_buttons.setVisible(False)
        self.comboBox.setVisible(False)
        self.current_index = len(self.recipe_list) - 1
        self.layout_widgets = []
        
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.frame_card.installEventFilter(self)
        for child in self.frame_card.children():
            if child.isWidgetType():
                # print('installed')
                child.installEventFilter(self)
        
        self.update_recipes()        
        self.show_hide_buttons()
        self.update_index()
        
        self.pB_add.setIcon(QIcon(self.dirname + '/UI/images/icon_add_recipe.png'))
        self.pB_delete.setIcon(QIcon(self.dirname + '/UI/images/icon_bin.png'))
        self.pB_next.setIcon(QIcon(self.dirname + '/UI/images/icon_right_arrow.png'))
        self.pB_edit.setIcon(QIcon(self.dirname + '/UI/images/icon_edit_2.png'))
        
        self.add_button_menu()
    
    def add_button_menu(self):
        self.pB_add_menu = QMenu(self)
        self.pB_add_menu.setStyleSheet('QWidget{color:%s;selection-color:%s;}' % 
                                       (self.colors['#color1_dark#'], self.colors['#color3_dark#']))
        
        self.actionRandomRecipe = QAction(self)
        self.actionRandomRecipe.setText('Plat au hasard')
        self.actionRandomRecipe.setIcon(QIcon(self.dirname + '/UI/images/icon_random_recipe.png'))
        self.actionChoiceRecipe = QAction(self)
        self.actionChoiceRecipe.setText('Plat au choix')
        self.actionChoiceRecipe.setIcon(QIcon(self.dirname + '/UI/images/icon_choice_recipe.png'))
        
        self.actionRandomDessert = QAction(self)
        self.actionRandomDessert.setText('Dessert au hasard')
        self.actionRandomDessert.setIcon(QIcon(self.dirname + '/UI/images/icon_random_dessert.png'))
        self.actionChoiceDessert = QAction(self)
        self.actionChoiceDessert.setText('Dessert au choix')
        self.actionChoiceDessert.setIcon(QIcon(self.dirname + '/UI/images/icon_choice_dessert.png'))
        
        self.pB_add_menu.addAction(self.actionRandomRecipe)
        self.pB_add_menu.addAction(self.actionChoiceRecipe)
        self.pB_add_menu.addAction(self.actionRandomDessert)
        self.pB_add_menu.addAction(self.actionChoiceDessert)
        
        self.pB_add.setMenu(self.pB_add_menu)
        
    def connect_actions(self):
        self.actionRandomRecipe.triggered.connect(self.on_add_random_recipe)
        self.actionChoiceRecipe.triggered.connect(self.on_add_choice_recipe)
        self.actionRandomDessert.triggered.connect(self.on_add_random_dessert)
        self.actionChoiceDessert.triggered.connect(self.on_add_choice_dessert)
        self.pB_delete.clicked.connect(self.on_delete)
        self.pB_next.clicked.connect(self.on_right)
        self.pB_edit.clicked.connect(self.on_edit_recipe)
    
    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent) -> bool:
        
        if event.type() == QEvent.Enter:
            self.on_enter_recipe_stack.emit(self.id)

        return super().eventFilter(watched, event)
    
    def update_recipes(self, index = -1):
        recipe = self.recipe_list[index]

        image_path = self.dirname + recipe.image + '_icon.jpg'
        qpix = QPixmap(image_path)
        if recipe.image != '' and recipe.image != '/images/':
            p1 = qpix.scaledToHeight(self.height()*0.8, Qt.SmoothTransformation)
            self.label_image.setPixmap(p1)
        else:
            self.label_image.setPixmap(qpix)
        self.label_title.setText(recipe.name)
    
    def on_add_random_recipe(self, recipe = None, dinner = 0):
        #dinner = 0;1 => lunch;dinner
        if recipe is None:
            simple_menu = menu.Menu(number_of_days=1)
            simple_menu.generate_smart_menu_v2(self.recipe_db)
            recipe = simple_menu.table[dinner]
            while recipe.name in recipe_db.get_recipe_names(self.recipe_list):
                simple_menu.generate_smart_menu_v2(self.recipe_db)
                recipe = simple_menu.table[dinner]
        self.recipe_list.append(recipe)
        
        self.show_hide_buttons()
        
        #display latest recipe added
        self.current_index = -1
        self.update_recipes()
        self.update_index()
        row, column = id_to_row_column(self.id)
        self.on_update_current_menu.emit(self.recipe_list, row, column)
        
        # print(self.parentWidget().underMouse())
    
    def on_add_choice_recipe(self):
        self.on_add_random_recipe()
        self.pB_edit.click()
    
    def on_add_random_dessert(self):
        simple_menu = menu.Menu(number_of_days=1)
        simple_menu.generate_dessert_full_menu(self.recipe_db, 1)
        dessert_recipe = simple_menu.desserts[0]
        self.on_add_random_recipe(recipe = dessert_recipe)
    
    def on_add_choice_dessert(self):
        self.on_add_random_dessert()
        self.pB_edit.click()
    
    def on_delete(self):
        self.recipe_list.remove(self.recipe_list[self.current_index])
        self.current_index = self.current_index % len(self.recipe_list)
        self.update_recipes(index = self.current_index)
        self.update_index()
        self.show_hide_buttons()
        row, column = id_to_row_column(self.id)
        self.on_update_current_menu.emit(self.recipe_list, row, column)
        
    def on_right(self):
        self.current_index = (self.current_index + 1) % len(self.recipe_list)
        self.update_recipes(index = self.current_index)
        self.update_index()
    
    def on_edit_recipe(self):
        # print('edit')
        
        self.comboBox.setVisible(self.pB_edit.isChecked())
        self.pB_add.setVisible(not self.pB_edit.isChecked())
        self.pB_delete.setVisible(not self.pB_edit.isChecked())
        self.pB_next.setVisible(not self.pB_edit.isChecked())
        self.label_title.setVisible(not self.pB_edit.isChecked())
        self.label_image.setVisible(not self.pB_edit.isChecked())
        
        if self.pB_edit.isChecked():
            self.comboBox.clear()
            selected_recipe = self.label_title.text()
            selected_recipe_object = self.recipe_db.get_recipe_object(selected_recipe)
            if selected_recipe_object.isTagged('dessert'):
                menu_list = recipe_db.get_recipe_sublist(self.recipe_db.recipe_list, tagsIn = ['dessert'])
            else:
                menu_list = recipe_db.get_recipe_sublist(self.recipe_db.recipe_list, tagsOut = ['dessert', 'tips'])
            recipe_list = sorted(recipe_db.get_recipe_names(menu_list), 
                                    key= str.lower)
            self.comboBox.addItems(recipe_list)
            
            self.comboBox.setCurrentText(selected_recipe)
            
            self.pB_edit.setIcon(QIcon(self.dirname + '/UI/images/icon_ok.png'))
        
            self.on_lock_for_edition.emit(self.id, True)
        else:
            text = self.comboBox.currentText()
            # print(recipe_db.get_recipe_names(self.recipe_db.recipe_list))
            # print(self.comboBox.currentText())
            recipe_object = self.recipe_db.get_recipe_object(text)
            self.recipe_list[self.current_index] = recipe_object
            # print(text, recipe_object.name, self.current_index)
            self.update_recipes(index = self.current_index)
            
            self.show_hide_buttons()
            
            self.pB_edit.setIcon(QIcon(self.dirname + '/UI/images/icon_edit_2.png'))
        
            
            self.on_lock_for_edition.emit(self.id, False)
            row, column = id_to_row_column(self.id)
            self.on_update_current_menu.emit(self.recipe_list, row, column)
            
        
    def show_hide_buttons(self):
        self.pB_next.setVisible(len(self.recipe_list) > 1)
        self.pB_delete.setVisible(len(self.recipe_list) > 1)
    
    def update_index(self):#to display the current index with dots icon
        for widget in self.layout_widgets:
            widget.setParent(None)
            self.hL.removeWidget(widget)
        self.layout_widgets = []
        
        if self.current_index == -1:
            index = len(self.recipe_list)
        else:
            index = self.current_index + 1
        length = len(self.recipe_list)

        if length > 1:
            for i in range(length - 1):
                label_num = QLabel('')
                cw.load_pic(label_num, self.dirname + '/UI/images/icon_circle.png')
                self.hL.addWidget(label_num)
                self.layout_widgets.append(label_num)
            label_pos = QLabel('')
            cw.load_pic(label_pos, self.dirname + '/UI/images/icon_circle_full.png')
            self.hL.insertWidget(index - 1, label_pos)
            self.layout_widgets.append(label_pos)
    
    def get_current_recipe(self):
        return self.recipe_list[self.current_index]


def id_to_row_column(id):
    if id[0] == '+':
        row = 0
    elif id[0] == '-':
        row = 1
    elif id[0] == '*':
        row = 2
    col = int(id[1:]) - 1
    return row, col

def row_column_to_id(row, column):
    id = '0' + str(column + 1)
    id = id[-2:]
    
    if row == 0:
        id = '+' + id
    elif row == 1:
        id = '-' + id
    elif row == 2:
        id = '*' + id
    
    return id