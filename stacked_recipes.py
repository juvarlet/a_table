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
import time

UI_FILE = cw.dirname(ui_file = True) + '/UI/stacked_recipes_.ui'

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
        # QCoreApplication.processEvents()
        # self.initial_state()
        self.init1()
        self.init2()
        # self.init3()
        # self.init4()
        # QCoreApplication.processEvents()
        self.connect_actions()
        # self.recipe_card_worker = RecipeCard()
        # self.recipe_card_worker.on_init.connect(self.initial_state)
        # self.recipe_card_worker.on_connect.connect(self.connect_actions)
        # self.recipe_card_worker.start()
        # QCoreApplication.processEvents()
        self.setObjectName('stack')
        
        self.initIsComplete = False
        
    def loadUI(self):
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        widget = QUiLoader().load(UI_FILE)
        vlayout.addWidget(widget)
        self.setLayout(vlayout)
        self.pW = widget
        
    def saveComponents(self):
        self.dirname = cw.dirname()
        
        self.stackedWidget: QStackedWidget
        self.stackedWidget = self.pW.stackedWidget

        self.label_image: QLabel
        self.label_image = self.pW.label_image

        self.frame_buttons: QFrame
        self.frame_buttons = self.pW.frame_buttons
        self.frame_buttons_2: QFrame
        self.frame_buttons_2 = self.pW.frame_buttons_2
        self.frame: QFrame
        self.frame = self.pW.frame
        self.frame_4: QFrame
        self.frame_4 = self.pW.frame_4

        self.pB_add: QPushButton
        self.pB_add = self.pW.pB_add
        # self.pB_add = QPushButton()
        self.pB_delete: QPushButton
        self.pB_delete = self.pW.pB_delete
        self.pB_edit: QPushButton
        self.pB_edit = self.pW.pB_edit

        self.pB_list: QPushButton
        self.pB_list = self.pW.pB_list
        self.pB_next: QPushButton
        self.pB_next = self.pW.pB_next
        self.label_title: QLabel
        self.label_title = self.pW.label_title

        self.pB_add_2: QPushButton
        self.pB_add_2 = self.pW.pB_add_2
        self.pB_delete_2: QPushButton
        self.pB_delete_2 = self.pW.pB_delete_2
        self.pB_edit_2: QPushButton
        self.pB_edit_2 = self.pW.pB_edit_2
        self.pB_stack: QPushButton
        self.pB_stack = self.pW.pB_stack

        self.list_stack: QListWidget
        self.list_stack = self.pW.list_stack

        self.pB_ok: QPushButton
        self.pB_ok = self.pW.pB_ok
        self.pB_cancel: QPushButton
        self.pB_cancel = self.pW.pB_cancel

        self.lE_search: QLineEdit
        self.lE_search = self.pW.lE_search

        self.list_stack_2: QListWidget
        self.list_stack_2 = self.pW.list_stack_2

        self.frame_card: QFrame
        self.frame_card = self.pW.frame_card
        self.frame_card_2: QFrame
        self.frame_card_2 = self.pW.frame_card_2
        self.frame_card_3: QFrame
        self.frame_card_3 = self.pW.frame_card_3
        
        self.hL: QHBoxLayout
        self.hL = self.pW.hL
    
    # @cw.decoratortimer(1)
    def initial_state(self):
        self.colors = COLORS
        self.frame_buttons.setVisible(False)
        self.pB_list.setVisible(False)
        # self.comboBox.setVisible(False)
        self.current_index = len(self.recipe_list) - 1
        self.layout_widgets = []
        
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.frame_card.installEventFilter(self)
        self.frame_card_2.installEventFilter(self)
        self.frame_card_3.installEventFilter(self)
        for child in self.frame_card.children() + self.frame_card_2.children() + self.frame_card_3.children():
            if child.isWidgetType():
                # print('installed')
                child.installEventFilter(self)
                
        self.update_recipes()      
        self.show_hide_buttons()
        self.update_index()
        self.update_list()
        
        self.pB_add.setIcon(QIcon(self.dirname + '/UI/images/icon_add_recipe.png'))
        self.pB_add_2.setIcon(QIcon(self.dirname + '/UI/images/icon_add_recipe.png'))
        self.pB_delete.setIcon(QIcon(self.dirname + '/UI/images/icon_bin.png'))
        self.pB_delete_2.setIcon(QIcon(self.dirname + '/UI/images/icon_bin.png'))
        self.pB_next.setIcon(QIcon(self.dirname + '/UI/images/icon_right_arrow.png'))
        self.pB_edit.setIcon(QIcon(self.dirname + '/UI/images/icon_edit_2.png'))
        self.pB_edit_2.setIcon(QIcon(self.dirname + '/UI/images/icon_edit_2.png'))
        self.pB_stack.setIcon(QIcon(self.dirname + '/UI/images/icon_stack.png'))
        self.pB_ok.setIcon(QIcon(self.dirname + '/UI/images/icon_ok.png'))
        self.pB_cancel.setIcon(QIcon(self.dirname + '/UI/images/icon_cancel.png'))
        self.pB_list.setIcon(QIcon(self.dirname + '/UI/images/icon_list_view.png'))
        
        self.add_button_menu()
    
    # @cw.decoratortimer(1)
    def init1(self):
        self.colors = COLORS
        self.frame_buttons.setVisible(False)
        self.pB_list.setVisible(False)
        # self.comboBox.setVisible(False)
        self.current_index = len(self.recipe_list) - 1
        self.layout_widgets = []
        
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.frame_card.installEventFilter(self)
        self.frame_card_2.installEventFilter(self)
        self.frame_card_3.installEventFilter(self)
        for child in self.frame_card.children() + self.frame_card_2.children() + self.frame_card_3.children():
            if child.isWidgetType():
                # print('installed')
                child.installEventFilter(self)
    
    # @cw.decoratortimer(1)
    def init2(self):
        self.update_recipes()      
        self.show_hide_buttons()
        self.update_index()
        self.update_list()
    
    # @cw.decoratortimer(1)
    def init3(self):
        self.pB_add.setIcon(QIcon(self.dirname + '/UI/images/icon_add_recipe.png'))
        self.pB_add_2.setIcon(QIcon(self.dirname + '/UI/images/icon_add_recipe.png'))
        self.pB_delete.setIcon(QIcon(self.dirname + '/UI/images/icon_bin.png'))
        self.pB_delete_2.setIcon(QIcon(self.dirname + '/UI/images/icon_bin.png'))
        self.pB_next.setIcon(QIcon(self.dirname + '/UI/images/icon_right_arrow.png'))
        self.pB_edit.setIcon(QIcon(self.dirname + '/UI/images/icon_edit_2.png'))
        self.pB_edit_2.setIcon(QIcon(self.dirname + '/UI/images/icon_edit_2.png'))
        self.pB_stack.setIcon(QIcon(self.dirname + '/UI/images/icon_stack.png'))
        self.pB_ok.setIcon(QIcon(self.dirname + '/UI/images/icon_ok.png'))
        self.pB_cancel.setIcon(QIcon(self.dirname + '/UI/images/icon_cancel.png'))
        self.pB_list.setIcon(QIcon(self.dirname + '/UI/images/icon_list_view.png'))
    
    # @cw.decoratortimer(1)
    def init4(self):
        self.add_button_menu()
        self.connect_action_menu()
    
    def add_button_menu(self):
        self.pB_add_menu = QMenu(self)
        self.pB_add_menu.setStyleSheet('QWidget{color:%s;selection-color:%s;}' % 
                                       (self.colors['#color1_dark#'], self.colors['#color3_dark#']))
        # self.pB_add_menu.setStyleSheet('QMenu{background-color:transparent;}')

        self.actionWidget = QWidgetAction(self.pB_add_menu)
        ui_actions = cw.dirname(ui_file = True) + '/UI/add_menu.ui'
        self.widget_menu = QUiLoader().load(ui_actions)
        self.widget_menu.pB_choice_recipe.setIcon(QIcon(self.dirname + '/UI/images/icon_choice_recipe.png'))
        self.widget_menu.pB_choice_dessert.setIcon(QIcon(self.dirname + '/UI/images/icon_choice_dessert.png'))
        self.widget_menu.pB_random_recipe.setIcon(QIcon(self.dirname + '/UI/images/icon_random_recipe.png'))
        self.widget_menu.pB_random_dessert.setIcon(QIcon(self.dirname + '/UI/images/icon_random_dessert.png'))
        self.actionWidget.setDefaultWidget(self.widget_menu)
        self.pB_add_menu.addAction(self.actionWidget)
                
        self.pB_add.setMenu(self.pB_add_menu)
        self.pB_add_2.setMenu(self.pB_add_menu)
    
    def connect_actions(self):
        self.pB_delete.clicked.connect(self.on_delete)
        self.pB_delete_2.clicked.connect(self.on_delete)
        self.pB_next.clicked.connect(self.on_right)
        self.pB_edit.clicked.connect(self.on_edit_recipe)
        self.pB_edit_2.clicked.connect(self.on_edit_recipe)
        self.pB_list.clicked.connect(self.on_list_view)
        self.pB_stack.clicked.connect(self.on_stack_view)
        self.list_stack.itemSelectionChanged.connect(self.on_recipe_selection)
        self.list_stack_2.itemSelectionChanged.connect(self.on_recipe_selection_2)
        self.lE_search.textChanged.connect(self.dynamic_filter)
        self.pB_ok.clicked.connect(self.on_ok)
        self.pB_cancel.clicked.connect(self.on_cancel)
        
    def connect_action_menu(self):
        self.widget_menu.pB_random_recipe.clicked.connect(self.on_add_random_recipe)
        self.widget_menu.pB_choice_recipe.clicked.connect(self.on_add_choice_recipe)
        self.widget_menu.pB_random_dessert.clicked.connect(self.on_add_random_dessert)
        self.widget_menu.pB_choice_dessert.clicked.connect(self.on_add_choice_dessert)
        
        self.widget_menu.pB_random_recipe.clicked.connect(self.pB_add_menu.close)
        self.widget_menu.pB_choice_recipe.clicked.connect(self.pB_add_menu.close)
        self.widget_menu.pB_random_dessert.clicked.connect(self.pB_add_menu.close)
        self.widget_menu.pB_choice_dessert.clicked.connect(self.pB_add_menu.close)
        
    def finish_init(self):
        if not self.initIsComplete:
            self.init3()
            self.init4()
            self.initIsComplete = True
            self.update_recipes()
            
    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent) -> bool:
        
        if event.type() == QEvent.Enter:
            self.on_enter_recipe_stack.emit(self.id)

        return super().eventFilter(watched, event)
    
    def update_recipes(self, index = -1):
        recipe = self.recipe_list[index]
        if type(recipe) is str:
            recipe = self.recipe_db.get_recipe_object(recipe)

        image_path = self.dirname + recipe.image + '_icon.jpg'
        qpix = QPixmap(image_path)
        if recipe.image != '' and recipe.image != '/images/':
            if qpix.height() < qpix.width():
                p1 = qpix.scaledToHeight(self.height()*1, Qt.SmoothTransformation)
            else:
                p1 = qpix.scaledToWidth(self.width()*1, Qt.SmoothTransformation)
            self.label_image.setPixmap(p1)
        else:
            self.label_image.setPixmap(qpix)
        self.label_title.setText(recipe.name)
    
    def update_list(self):
        self.list_stack.clear()
        # self.list_stack_2.clear()
        self.list_stack.addItems([
            recipe.name 
            if type(recipe) is not str 
            else self.recipe_db.get_recipe_object(recipe) 
            for recipe in self.recipe_list])
        # self.list_stack_2.addItems([recipe.name for recipe in self.recipe_list])
        
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
        self.update_list()
        row, column = id_to_row_column(self.id)
        self.on_update_current_menu.emit(self.recipe_list, row, column)
        self.on_recipe_selection()
        # print(self.parentWidget().underMouse())
    
    def on_add_choice_recipe(self):
        self.on_add_random_recipe()
        self.from_page = self.stackedWidget.currentIndex()
        if self.from_page == 0:
            self.pB_edit.click()
        elif self.from_page == 1:
            self.list_stack.item(self.list_stack.count()-1).setSelected(True)
            self.pB_edit_2.click()
            
    
    def on_add_random_dessert(self):
        simple_menu = menu.Menu(number_of_days=1)
        simple_menu.generate_dessert_full_menu(self.recipe_db, 1)
        dessert_recipe = simple_menu.desserts[0]
        self.on_add_random_recipe(recipe = dessert_recipe)
    
    def on_add_choice_dessert(self):
        self.on_add_random_dessert()
        self.pB_edit.click()
    
    def on_delete(self):
        self.recipe_list.remove(self.get_current_recipe())
        self.current_index = self.current_index % len(self.recipe_list)
        self.update_recipes(index = self.current_index)
        self.update_index()
        self.update_list()
        self.show_hide_buttons()
        row, column = id_to_row_column(self.id)
        self.on_update_current_menu.emit(self.recipe_list, row, column)
        if self.current_index == len(self.recipe_list):
            self.current_index -= 1
        self.on_recipe_selection()
        
    def on_right(self):
        self.a1 = cw.animate_button(self.pB_next)
        self.a1.start()
        self.current_index = (self.current_index + 1) % len(self.recipe_list)
        self.update_recipes(index = self.current_index)
        self.update_index()
    
    def on_recipe_selection(self):
        # print(self.list_stack.currentItem().text())
        isItemSelected = self.list_stack.currentItem() is not None
        self.pB_edit_2.setVisible(isItemSelected)
        self.pB_delete_2.setVisible(isItemSelected and len(self.recipe_list) > 1)
        if isItemSelected:
            self.current_index = self.list_stack.currentRow()
        
    def on_recipe_selection_2(self):
        isItemSelected = self.list_stack_2.currentItem() is not None
        isItemSelectedVisible = isItemSelected and not self.list_stack_2.currentItem().isHidden()
        self.pB_ok.setVisible(isItemSelectedVisible)
        
    def dynamic_filter(self):
        cw.dynamic_filter(self.lE_search.text(), self.list_stack_2, self.recipe_db)
        self.on_recipe_selection_2()
        
    def on_edit_recipe(self):
        self.from_page = self.stackedWidget.currentIndex()
        if self.from_page == 0:
            recipe_name = self.label_title.text()
        elif self.from_page == 1:
            # recipe_name = self.list_stack.currentItem().text()
            recipe_name = self.list_stack.selectedItems()[0].text()
        self.stackedWidget.setCurrentIndex(2)
        self.lE_search.setFocus(Qt.OtherFocusReason)
        
        self.list_stack_2.clear()
        full_recipe_list = sorted(recipe_db.get_recipe_names(self.recipe_db.recipe_list), key=str.lower)
        self.list_stack_2.addItems(full_recipe_list)
        
        lwi = self.list_stack_2.findItems(recipe_name, Qt.MatchExactly)[0]
        self.list_stack_2.scrollToItem(lwi)
        self.list_stack_2.setCurrentItem(lwi)
        lwi.setSelected(True)
        
        self.on_lock_for_edition.emit(self.id, True)
        
        # self.comboBox.setVisible(self.pB_edit.isChecked())
        # self.pB_add.setVisible(not self.pB_edit.isChecked())
        # self.pB_delete.setVisible(not self.pB_edit.isChecked())
        # self.pB_next.setVisible(not self.pB_edit.isChecked())
        # self.label_title.setVisible(not self.pB_edit.isChecked())
        # self.label_image.setVisible(not self.pB_edit.isChecked())
        
        # if self.pB_edit.isChecked():
        #     self.comboBox.clear()
        #     selected_recipe = self.label_title.text()
        #     selected_recipe_object = self.recipe_db.get_recipe_object(selected_recipe)
        #     if selected_recipe_object.isTagged('dessert'):
        #         menu_list = recipe_db.get_recipe_sublist(self.recipe_db.recipe_list, tagsIn = ['dessert'])
        #     else:
        #         menu_list = recipe_db.get_recipe_sublist(self.recipe_db.recipe_list, tagsOut = ['dessert', 'tips'])
        #     recipe_list = sorted(recipe_db.get_recipe_names(menu_list), 
        #                             key= str.lower)
        #     self.comboBox.addItems(recipe_list)
            
        #     self.comboBox.setCurrentText(selected_recipe)
            
        #     self.pB_edit.setIcon(QIcon(self.dirname + '/UI/images/icon_ok.png'))
        
        #     self.on_lock_for_edition.emit(self.id, True)
        # else:
        #     text = self.comboBox.currentText()
        #     # print(recipe_db.get_recipe_names(self.recipe_db.recipe_list))
        #     # print(self.comboBox.currentText())
        #     recipe_object = self.recipe_db.get_recipe_object(text)
        #     self.recipe_list[self.current_index] = recipe_object
        #     # print(text, recipe_object.name, self.current_index)
        #     self.update_recipes(index = self.current_index)
            
        #     self.show_hide_buttons()
            
        #     self.pB_edit.setIcon(QIcon(self.dirname + '/UI/images/icon_edit_2.png'))
        
            
        #     self.on_lock_for_edition.emit(self.id, False)
        #     row, column = id_to_row_column(self.id)
        #     self.on_update_current_menu.emit(self.recipe_list, row, column)
    
    def on_ok(self):
        text = self.list_stack_2.currentItem().text()
        recipe_object = self.recipe_db.get_recipe_object(text)
        if self.from_page == 1:
            self.current_index = self.list_stack.currentRow()
        self.recipe_list[self.current_index] = recipe_object
        self.update_recipes(index = self.current_index)
        self.update_list()
        self.show_hide_buttons()
        self.on_lock_for_edition.emit(self.id, False)
        row, column = id_to_row_column(self.id)
        self.on_update_current_menu.emit(self.recipe_list, row, column)
        self.stackedWidget.setCurrentIndex(self.from_page)
        self.on_recipe_selection()
    
    def on_cancel(self):
        self.stackedWidget.setCurrentIndex(self.from_page)
        self.on_lock_for_edition.emit(self.id, False)
        self.on_recipe_selection()
        
    def show_hide_buttons(self):
        self.pB_next.setVisible(len(self.recipe_list) > 1)
        self.pB_delete.setVisible(len(self.recipe_list) > 1)
        self.pB_delete_2.setVisible(len(self.recipe_list) > 1)
    
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
                label_num.setStyleSheet('QLabel{background:transparent;}')
                cw.load_pic(label_num, self.dirname + '/UI/images/icon_circle.png')
                self.hL.addWidget(label_num)
                self.layout_widgets.append(label_num)
            label_pos = QLabel('')
            label_pos.setStyleSheet('QLabel{background:transparent;}')
            cw.load_pic(label_pos, self.dirname + '/UI/images/icon_circle_full.png')
            self.hL.insertWidget(index - 1, label_pos)
            self.layout_widgets.append(label_pos)
    
    def get_current_recipe(self):
        return self.recipe_list[self.current_index]

    def on_list_view(self):
        # self.animate_button(self.pB_list)
        # self.stackedWidget.slideToNextWidget()
        self.stackedWidget.setCurrentIndex(1)
        self.on_recipe_selection()
    
    def on_stack_view(self):
        # self.animate_button(self.pB_stack)
        self.update_index()
        self.update_recipes(self.current_index)
        self.stackedWidget.setCurrentIndex(0)

    def on_enter_exit_stack(self, isHovered):
        self.frame_buttons.setVisible(isHovered)
        self.pB_list.setVisible(isHovered)
        self.pB_next.setVisible(isHovered and len(self.recipe_list) > 1)
        self.pB_stack.setVisible(isHovered)
        self.frame_buttons_2.setVisible(isHovered)
        self.frame_4.setVisible(isHovered)
        
        # if not self.initIsComplete:
        #     self.init3()
        #     self.init4()
        #     self.initIsComplete = True
    

        
class RecipeCard(QThread):#QThread
    
    on_init = Signal(StackedRecipes)
    on_connect = Signal(StackedRecipes)
    on_stop = Signal()
    
    def __init__(self, stacked_recipes_list):
        QThread.__init__(self)
        self.stacked_recipe_list = stacked_recipes_list
    
    def run(self):
        for stacked_recipe in self.stacked_recipe_list:
            self.on_init.emit(stacked_recipe)
            self.on_connect.emit(stacked_recipe)
        self.on_stop.emit()
        

        
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