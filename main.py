import os
from os.path import basename
from recipe import Recipe
import sys
import recipe_db
import menu
import mailbox_google as mail
import printer
from datetime import date, timedelta
from pyperclip import copy
from shutil import copy2

import PySide2
from PySide2.QtWidgets import*
# QApplication, QWidget, QPushButton, QTableWidget, QSpinBox
from PySide2.QtGui import QBrush, QDoubleValidator, QPainterPath, QPixmap, QIcon, QColor, QPainter
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import*
# QDate

#COLOR THEME
RED = '#d72631' #215,38,49
LIGHT_GREEN = '#a2d5c6' #162,213,198
FADED_LIGHT_GREEN = '#b7cab9' #183,202,185
GREEN = '#077b8a' #7,123,138
VIOLET = '#5c3c92' #92,60,146
BEIGE = '#ccc1ae' #204,193,174

#TAGS
'''
dessert
ete/hiver
midi/soir
kids
double
vegan
tips
'''

#@table_@dmin
#notification.a.table@gmail.com
#Maitre D'hotel

class MainGUI(QWidget):
    def __init__(self, parent=None, recipe_db = None):
        super(MainGUI, self).__init__(parent)
        self.initial_state(recipe_db)
        self.connect_actions()
        self.update_modif()

        #generate default menu at startup
        self.pB_new_menu.click()
        
    def initial_state(self, my_recipe_db):
        #variables
        self.pW = self.parentWidget()
        self.recipe_db: recipe_db.RecipeDB
        self.recipe_db = my_recipe_db
        self.current_menu = menu.Menu()
        self.dessert_list = []
        self.dirname = os.path.dirname(__file__)
        self.just_dropped = False
        self.cell_signal_count = 0
        self.from_cell = ()
        self.to_cell = ()
        self.html_source_file_shopping = self.dirname + '/shopping_core.html'
        self.default_email = ''
        self.recipe_image_path = ''
        self.myThreads = []

        #-- ui widgets --
        self.tW: QTabWidget
        self.tW = self.pW.tabWidget
        #-tab menu
        self.tab_menus: QWidget
        self.tab_menus = self.pW.tab_menus
        self.tB: QToolBox
        self.tB = self.pW.toolBox
        self.label_date: QLabel
        self.label_date = self.pW.label_date
        self.label_dessert: QLabel
        self.label_dessert = self.pW.label_dessert
        self.cB_restes: QCheckBox
        self.cB_restes = self.pW.cB_restes_2
        self.dateEdit: QDateEdit
        self.dateEdit = self.pW.dateEdit_2
        self.sB_desserts: QSpinBox
        self.sB_desserts = self.pW.sB_desserts_2
        self.sB_days: QSpinBox
        self.sB_days = self.pW.sB_days_2
        self.p_carte: QWidget
        self.p_carte = self.pW.page_carte
        self.pB_save: QPushButton
        self.pB_save = self.pW.pB_save
        self.pB_new_menu: QPushButton
        self.pB_new_menu = self.pW.pB_new_menu_2
        self.pB_modif: QPushButton
        self.pB_modif = self.pW.pB_modif
        self.tW_menu: QTableWidget
        self.tW_menu = self.pW.tW_menu
        self.score_vegan: QLabel
        self.score_vegan = self.pW.label_s_vegan
        self.score_kids: QLabel
        self.score_kids = self.pW.label_s_kids
        self.score_double: QLabel
        self.score_double = self.pW.label_s_double
        self.score_summer: QLabel
        self.score_summer = self.pW.label_s_ete
        self.score_winter: QLabel
        self.score_winter = self.pW.label_s_hiver
        #--page shopping
        self.p_list: QWidget
        self.p_list = self.pW.page_liste
        self.lW_shopping: QListWidget
        self.lW_shopping = self.pW.lW_courses
        self.lW_menu: QListWidget
        self.lW_menu = self.pW.lW_menu
        self.frame_shopping: QFrame
        self.frame_shopping = self.pW.frame_shopping
        self.label_top: QLabel
        self.label_top = self.pW.label_top
        self.label_icon_carte: QLabel
        self.label_icon_carte = self.pW.label_icon_carte
        self.frame_bottom: QFrame
        self.frame_bottom = self.pW.frame_bottom
        self.label_cocktail: QLabel
        self.label_cocktail = self.pW.label_cocktail
        self.pB_print: QPushButton
        self.pB_print = self.pW.pB_print
        self.pB_send: QPushButton
        self.pB_send = self.pW.pB_send
        self.pB_copy: QPushButton
        self.pB_copy = self.pW.pB_copy
        #-tab recettes
        self.tab_recipe: QWidget
        self.tab_recipe = self.pW.tab_recettes
        self.label_recipe_title: QLabel
        self.label_recipe_title = self.pW.label_titre
        self.label_recipe_image: QLabel
        self.label_recipe_image = self.pW.label_image
        self.pB_back: QPushButton
        self.pB_back = self.pW.pB_back
        self.pB_print_2: QPushButton
        self.pB_print_2 = self.pW.pB_print_2
        self.pB_send_2: QPushButton
        self.pB_send_2 = self.pW.pB_send_2
        self.pB_modif_2: QPushButton
        self.pB_modif_2 = self.pW.pB_modif_2
        self.pB_new_recipe: QPushButton
        self.pB_new_recipe = self.pW.pB_new_recipe
        self.pB_delete: QPushButton
        self.pB_delete = self.pW.pB_delete
        self.label_newedit: QLabel
        self.label_newedit = self.pW.label_newedit
        self.pB_photo: QPushButton
        self.pB_photo = self.pW.pB_photo
        self.tE_ingredients: QTextEdit
        self.tE_ingredients = self.pW.tE_ingredients
        self.tE_recipe: QTextEdit
        self.tE_recipe = self.pW.tE_recette
        self.lW_recipe: QListWidget
        self.lW_recipe = self.pW.lW_recettes
        self.cB_search: QCheckBox
        self.cB_search = self.pW.cB_recherche
        self.frame_search: QFrame
        self.frame_search = self.pW.frame_recherche
        self.frame_new_recipe: QFrame
        self.frame_new_recipe = self.pW.frame_new_recipe
        self.frame_edit_recipe: QFrame
        self.frame_edit_recipe = self.pW.frame_edit_recipe
        self.lE_title: QLineEdit
        self.lE_title = self.pW.lE_titre
        self.label_image_2: QLabel
        self.label_image_2 = self.pW.label_image_2
        self.tW_ingredients: QTableWidget
        self.tW_ingredients = self.pW.tW_ingredients
        self.cB_ingredient: QComboBox
        self.cB_ingredient = self.pW.cB_ingredient
        self.lE_qty: QLineEdit
        self.lE_qty = self.pW.lE_qty
        self.cB_unit: QComboBox
        self.cB_unit = self.pW.cB_unit
        self.pB_add: QPushButton
        self.pB_add = self.pW.pB_add
        self.pB_option: QPushButton
        self.pB_option = self.pW.pB_option
        self.sB_time: QSpinBox
        self.sB_time = self.pW.sB_time
        self.tB_preparation: QTextBrowser
        self.tB_preparation = self.pW.tB_preparation
        self.cB_tagdouble: QCheckBox
        self.cB_tagdouble = self.pW.cB_tagdouble
        self.cB_tagdessert: QCheckBox
        self.cB_tagdessert = self.pW.cB_tagdessert
        self.cB_tagdinner: QCheckBox
        self.cB_tagdinner = self.pW.cB_tagdinner
        self.cB_tagkids: QCheckBox
        self.cB_tagkids = self.pW.cB_tagkids
        self.cB_taglunch: QCheckBox
        self.cB_taglunch = self.pW.cB_taglunch
        self.cB_tagsummer: QCheckBox
        self.cB_tagsummer = self.pW.cB_tagsummer
        self.cB_tagtips: QCheckBox
        self.cB_tagtips = self.pW.cB_tagtips
        self.cB_tagvegan: QCheckBox
        self.cB_tagvegan = self.pW.cB_tagvegan
        self.cB_tagwinter: QCheckBox
        self.cB_tagwinter = self.pW.cB_tagwinter
        self.lE_with: QLineEdit
        self.lE_with = self.pW.lE_with
        self.lE_without: QLineEdit
        self.lE_without = self.pW.lE_without
        self.pB_filter: QPushButton
        self.pB_filter = self.pW.pB_filter
        self.frame_tags: QFrame
        self.frame_tags = self.pW.frame_tags
        self.tag_vegan: QLabel
        self.tag_vegan = self.pW.label_vegan
        self.tag_kids: QLabel
        self.tag_kids = self.pW.label_kids
        self.tag_double: QLabel
        self.tag_double = self.pW.label_double
        self.tag_summer: QLabel
        self.tag_summer = self.pW.label_summer
        self.tag_winter: QLabel
        self.tag_winter = self.pW.label_winter
        self.tag_dessert: QLabel
        self.tag_dessert = self.pW.label_dessert_2
        self.tag_lunchdinner: QLabel
        self.tag_lunchdinner = self.pW.label_lunchdinner
        self.tag_tips: QLabel
        self.tag_tips = self.pW.label_tips
        self.pB_ok_2: QPushButton
        self.pB_ok_2 = self.pW.pB_ok_2
        self.pB_cancel_2: QPushButton
        self.pB_cancel_2 = self.pW.pB_cancel_2
        #-tab historique
        self.tab_history: QWidget
        self.tab_history = self.pW.tab_historique
        self.tW_history: QTableWidget
        self.tW_history = self.pW.tW_historique
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

        #default state
        self.window().setWindowState(Qt.WindowMaximized)
        #-replace qtablewidget tW_menu by custom class
        new_tW_menu = TableWidgetCustom(self.pW)
        new_tW_menu.setRowCount(3)
        new_tW_menu.setVerticalHeaderLabels([' Midi ', ' Soir ', ' Desserts '])
        new_tW_menu.hideRow(2)
        
        new_tW_menu.setMouseTracking(True)
        new_tW_menu.setEditTriggers(self.tW_menu.editTriggers())
        new_tW_menu.setDragEnabled(True)
        new_tW_menu.setDragDropOverwriteMode(False)
        new_tW_menu.setDragDropMode(self.tW_menu.dragDropMode())
        #new_tW_menu.setAlternatingRowColors(True)
        new_tW_menu.setSelectionMode(self.tW_menu.selectionMode())
        new_tW_menu.setTextElideMode(self.tW_menu.textElideMode())
        new_tW_menu.setFont(self.tW_menu.font())
        self.pW.gridLayout_10.replaceWidget(self.tW_menu, new_tW_menu)
        self.tW_menu = new_tW_menu
        self.pW.tW_menu.setParent(None)

        self.dateEdit.setDate(QDate().currentDate().addDays(1))
        self.tW_menu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_menu.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_menu.setIconSize(QSize(160, 160))
        self.tW_menu.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tW_menu.viewport().installEventFilter(self)

        self.pB_modif.setEnabled(False)
        self.pB_save.setEnabled(False)

        # self.tW_shopping.setVisible(False)
        recipe_list = sorted(recipe_db.get_recipe_names(self.recipe_db.recipe_list), key=str.lower)
        self.lW_recipe.addItems(recipe_list)
        self.pB_back.hide()      

        self.frame_search.hide()
        self.frame_edit_recipe.hide()
        
        self.tW_ingredients.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_ingredients.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.lE_qty.setValidator(QDoubleValidator(0, 1000, 2))

        self.tW_history.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_history.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_history.setColumnCount(2)
        
        self.reset_history()
        
        #images
        self.window().setWindowIcon(QIcon(self.dirname + '/UI/images/donut.png'))

        load_pic(self.label_date, self.dirname + '/UI/images/icon_date_3colors_t_LD.png')
        load_pic(self.label_dessert, self.dirname + '/UI/images/icon_cupcake_t.png')
        # load_pic(self.label_dessert_2, self.dirname + '/UI/images/tag_dessert_color_LD.png')
        self.tW.setTabIcon(0,QIcon(self.dirname + '/UI/images/icon_chef_3colors.png'))
        self.tW.setTabIcon(1,QIcon(self.dirname + '/UI/images/icon_recipe_3colors.png'))
        self.tW.setTabIcon(2,QIcon(self.dirname + '/UI/images/icon_plate_3colors.png'))
        self.tB.setItemIcon(0, QIcon(self.dirname + '/UI/images/icon_menu_3colors.png'))
        self.tB.setItemIcon(1, QIcon(self.dirname + '/UI/images/icon_shopping_cart.png'))
        self.pB_new_menu.setIcon(QIcon(self.dirname + '/UI/images/icon_cover_3colors_new.png'))
        self.pB_modif.setIcon(QIcon(self.dirname + '/UI/images/icon_edit.png'))
        self.pB_save.setIcon(QIcon(self.dirname + '/UI/images/icon_plate_3colors.png'))
        load_pic(self.tag_vegan, self.dirname + '/UI/images/tag_vegan_black_LD.png')
        load_pic(self.tag_kids, self.dirname + '/UI/images/tag_kids_black_LD.png')
        load_pic(self.tag_double, self.dirname + '/UI/images/tag_double_black_LD.png')
        load_pic(self.tag_summer, self.dirname + '/UI/images/tag_ete_black_LD.png')
        load_pic(self.tag_winter, self.dirname + '/UI/images/tag_hiver_black_LD.png')
        load_pic(self.tag_dessert, self.dirname + '/UI/images/tag_dessert_black_LD.png')
        load_pic(self.tag_tips, self.dirname + '/UI/images/tag_tips_black_LD.png')
        load_pic(self.tag_lunchdinner, self.dirname + '/UI/images/tag_lunch_black_LD.png')
        self.pB_back.setIcon(QIcon(self.dirname + '/UI/images/icon_back.png'))
        self.pB_print_2.setIcon(QIcon(self.dirname + '/UI/images/icon_print.png'))
        self.pB_send_2.setIcon(QIcon(self.dirname + '/UI/images/icon_send.png'))

        load_pic(self.score_vegan, self.dirname + '/UI/images/score_vegan_0.png')
        load_pic(self.score_kids, self.dirname + '/UI/images/score_kids_0.png')
        load_pic(self.score_double, self.dirname + '/UI/images/score_double_0.png')
        load_pic(self.score_summer, self.dirname + '/UI/images/score_ete_0.png')
        load_pic(self.score_winter, self.dirname + '/UI/images/score_hiver_0.png')
        
        load_pic(self.label_top, self.dirname + '/UI/images/icon_list.png')
        load_pic(self.label_icon_carte, self.dirname + '/UI/images/icon_menu_3colors_LD.png')
        load_pic(self.label_cocktail, self.dirname + '/UI/images/table_cocktails.png')
        self.pB_print.setIcon(QIcon(self.dirname + '/UI/images/icon_print.png'))
        self.pB_send.setIcon(QIcon(self.dirname + '/UI/images/icon_send.png'))
        self.pB_copy.setIcon(QIcon(self.dirname + '/UI/images/icon_copy.png'))

        labels = [self.label_deco_1,self.label_deco_2,self.label_deco_3,self.label_deco_4,
                  self.label_deco_5,self.label_deco_6,self.label_deco_7,self.label_deco_8,
                  self.label_deco_9,self.label_deco_10,self.label_deco_11,self.label_deco_12,
                  self.label_deco_13,self.label_deco_14,self.label_deco_15,self.label_deco_16]
        
        for i, label in enumerate(labels):
            load_pic(label, self.dirname + '/UI/images/icon_deco_%s.png' % (i+1))
        
        load_pic(self.label_warning, self.dirname + '/UI/images/icon_fork_X_3colors_t_LD.png')
        self.pB_cancel.setIcon(QIcon(self.dirname + '/UI/images/icon_cancel.png'))
        self.pB_ok.setIcon(QIcon(self.dirname + '/UI/images/icon_ok.png'))
        self.pB_cancel_2.setIcon(QIcon(self.dirname + '/UI/images/icon_cancel.png'))
        self.pB_ok_2.setIcon(QIcon(self.dirname + '/UI/images/icon_ok.png'))
        self.pB_modif_2.setIcon(QIcon(self.dirname + '/UI/images/icon_edit.png'))
        self.pB_new_recipe.setIcon(QIcon(self.dirname + '/UI/images/icon_new_recipe.png'))
        self.pB_delete.setIcon(QIcon(self.dirname + '/UI/images/icon_bin.png'))
        self.pB_photo.setIcon(QIcon(self.dirname + '/UI/images/icon_photo.png'))

    def main(self):
        self.pW.show()

    def connect_actions(self):
        self.pB_new_menu.clicked.connect(self.on_new_menu)
        self.tW_menu.cellDoubleClicked.connect(self.on_card_recipe_selection)
        self.tW_history.cellDoubleClicked.connect(self.on_history_recipe_selection)
        self.pB_modif.clicked.connect(self.on_card_modif)
        self.pB_filter.clicked.connect(self.on_filter_selection)
        self.pB_save.clicked.connect(self.on_save_menu)
        self.pB_ok.clicked.connect(self.on_confirm_history_update)
        self.pB_cancel.clicked.connect(self.on_cancel_history_update)
        self.tE_ingredients.anchorClicked.connect(self.on_recipe_link)
        self.pB_back.clicked.connect(self.on_previous_recipe)
        self.pB_copy.clicked.connect(self.on_copy_shopping_list)
        self.pB_send.clicked.connect(self.on_send_shopping_list)
        self.pB_print.clicked.connect(self.on_print_shopping_list)
        self.pB_send_2.clicked.connect(self.on_send_recipe)
        self.pB_print_2.clicked.connect(self.on_print_recipe)
        self.pB_new_recipe.clicked.connect(self.on_new_recipe)
        self.pB_modif_2.clicked.connect(self.on_edit_recipe)
        self.pB_delete.clicked.connect(self.on_delete_recipe)
        self.pB_ok_2.clicked.connect(self.on_confirm_recipe)
        self.pB_cancel_2.clicked.connect(self.on_cancel_recipe)
        self.pB_add.clicked.connect(self.on_add_ingredient)
        self.pB_photo.clicked.connect(self.on_add_photo)
        
    def update_modif(self):
        self.dateEdit.dateChanged.connect(self.dummy_function)
        self.tW_menu.cellChanged.connect(self.on_drag_drop_event)
        self.lW_recipe.itemSelectionChanged.connect(self.on_recipe_selection)
        self.sB_desserts.valueChanged.connect(self.on_dessert_selection)
        self.lW_shopping.itemSelectionChanged.connect(self.on_ingredient_selection)
        self.tW.currentChanged.connect(self.on_tab_changed)
        
        self.selectable_tags = [self.cB_tagdinner, self.cB_tagdessert, self.cB_tagdouble, self.cB_tagkids,
                                self.cB_taglunch, self.cB_tagwinter, self.cB_tagsummer, self.cB_tagvegan, self.cB_tagtips]
        for tag in self.selectable_tags:
            tag.toggled.connect(lambda _, cB=tag: self.on_tag_selected(cB))
        
    def dummy_function(self, row, column):
        print('dummy function triggered %s %s' % (row, column))
    
    def print_thread_function(self, data):
        # print(data)
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle('Information')
        error_dialog.setWindowModality(Qt.WindowModal)
        error_dialog.setText(data)
        error_dialog.setIcon(QMessageBox.Information)
        # error_dialog.setDetailedText(text)
        error_dialog.exec_()
    
    def on_new_menu(self):
        self.new_menu()
        self.populate_tW_menu(self.current_menu)
        self.on_dessert_selection(self.sB_desserts.value()) #includes dessert, menu_list, shopping list
        self.compute_score()
        self.pB_modif.setEnabled(True)
        self.pB_save.setEnabled(True)

        #TODO
        #clean code
        #exe package for windows on VM
        #bug dessert changed update shopping list
    
    def new_menu(self):
        current_QDate = self.dateEdit.date()
        y = current_QDate.year()
        m = current_QDate.month()
        d = current_QDate.day()
        self.current_menu.start_day = date(y, m, d)
        self.current_menu.number_of_days = self.sB_days.value()

        # self.current_menu.generate_random_menu(self.recipe_db)
        options = []
        if self.cB_restes.isChecked():
            options = ['leftovers']
        self.current_menu.generate_smart_menu_v2(self.recipe_db, options = options)
        self.current_menu.use_double()

    def populate_tW_menu(self, menu):
        #reset tW_Menu
        self.tW_menu.setColumnCount(0)
        #update tW_menu with days
        self.tW_menu.setColumnCount(self.sB_days.value())
        table_menu = menu.full_menu()
        self.tW_menu.setHorizontalHeaderLabels([m[0] for m in table_menu])

        #update tW_menu with menus
        recipe_list_lunch = [m[1] for m in table_menu]
        recipe_list_dinner = [m[2] for m in table_menu]
        for i, recipes_of_day in enumerate(zip(recipe_list_lunch, recipe_list_dinner)):
            recipe_lunch, recipe_dinner = recipes_of_day
            text_lunch, text_dinner = (recipe_lunch.name, recipe_dinner.name)
            # print((text_lunch, self.recipe_db.background_score(recipe_lunch, self.current_menu.start_day)))
            qtwi_lunch, qtwi_dinner = (QTableWidgetItem(text_lunch), QTableWidgetItem(text_dinner))
            qtwi_lunch.setTextAlignment(Qt.AlignCenter)
            qtwi_dinner.setTextAlignment(Qt.AlignCenter)

            self.tW_menu.setItem(0, i, qtwi_lunch)
            self.tW_menu.setItem(1, i, qtwi_dinner)

            display_image(recipe_lunch, self.dirname, qtwi_lunch, icon = True)
            display_image(recipe_dinner, self.dirname, qtwi_dinner, icon = True)
    
    def on_drag_drop_event(self, row, column):
        
        if self.just_dropped and self.cell_signal_count == 1:
            self.from_cell = (row, column)
            self.cell_signal_count += 1
            #copy again in case of bad drop


        elif self.just_dropped and self.cell_signal_count == 2:
            #reinit event detection
            self.just_dropped = False
            self.cell_signal_count = 0

            self.to_cell = (row, column)

            #take text and image from original to_cell
            original_to_cell_recipe = self.current_menu.full_menu()[column][row + 1]
            text = original_to_cell_recipe.name
            qtwi = QTableWidgetItem(text)
            qtwi.setTextAlignment(Qt.AlignCenter)
            #and insert in from_cell (now empty after drop)
            from_row, from_column = self.from_cell
            self.tW_menu.setItem(from_row, from_column, qtwi)

            display_image(original_to_cell_recipe, self.dirname, qtwi, icon = True)

            #update menu object
            #take from recipe
            from_recipe = self.current_menu.table[from_row + from_column*2]
            #take to recipe
            to_row, to_column = self.to_cell
            to_recipe = self.current_menu.table[to_row + to_column*2]
            #switch
            self.current_menu.table[to_row + to_column*2] = from_recipe
            self.current_menu.table[from_row + from_column*2] = to_recipe

            self.tW_menu.item(to_row, to_column).setSelected(True)
            self.tW_menu.item(from_row, from_column).setSelected(False)
                
            #**Improvement: make sur drop was not forgotten (dropped between 2 cells)
            
                #menu.table to tW_menu
                #   rc
                # 0 00
                # 1 10
                # 2 01
                # 3 11
                # 4 02
                # 5 12
                # 6 03
                # 7 13

    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent) -> bool:

        # if watched == self.tW_menu.viewport() and event.type() == QDropEvent:
        if event.type() == QEvent.Drop:
            #start special process
            self.just_dropped = True
            self.cell_signal_count += 1
        return super().eventFilter(watched, event)

    def populate_tW_dessert(self, dessert_list = []):
        if dessert_list == []:
            self.dessert_list = self.current_menu.generate_dessert_full_menu(self.recipe_db, self.sB_desserts.value())
        else:
            self.dessert_list = dessert_list
        for i, dessert in enumerate(self.dessert_list):
            text = dessert.name
            qtwi_dessert = QTableWidgetItem(text)
            qtwi_dessert.setTextAlignment(Qt.AlignCenter)

            # self.tW_dessert.setItem(0, i, qtwi_dessert)
            self.tW_menu.setItem(2, i, qtwi_dessert)

            display_image(dessert, self.dirname, qtwi_dessert, icon = True)
        
        for x in range(self.sB_desserts.value(), self.tW_menu.columnCount()):
            self.tW_menu.setItem(2, x, QTableWidgetItem())
            self.tW_menu.item(2, x).setBackground(QColor(204,193,174))
    
    def populate_shopping_list(self):
        #reset list
        self.lW_shopping.clear()
        # print(self.current_menu.get_shopping_list())
        options = []
        missing = []
        for ingredient, qty_unit in self.current_menu.get_shopping_list().items():
            if ingredient != 'missing information':
                string = ''
                string_option = ''
                qty, unit = qty_unit
                if ingredient != '':
                    if ingredient[0] == '[' and ingredient[-1] == ']':
                        string_option += '- %s : %s' % (ingredient, qty)
                        if unit != '()':
                            string_option += unit
                        options.append(string_option)
                    else:
                        string += '- %s : %s' % (ingredient, qty)
                        if unit != '()':
                            string += unit
                        self.lW_shopping.addItem(string)
            else:
                missing.append(qty_unit) #in that case qty_unit is recipe name
        
        if len(options) > 0:
            qlwi = QListWidgetItem('\nOptionnel :')
            qlwi.setFlags(qlwi.flags() & ~Qt.ItemIsSelectable)
            self.lW_shopping.addItem(qlwi)
            self.lW_shopping.addItems(options)
        
        if len(missing) > 0:
            qlwi = QListWidgetItem(u'\n-> Ingrédients manquants pour :')
            qlwi.setFlags(qlwi.flags() & ~Qt.ItemIsSelectable)
            self.lW_shopping.addItem(qlwi)
            self.lW_shopping.addItems(missing[0])

    def populate_menu_list(self):
        #reset list
        self.lW_menu.clear()
        self.lW_menu.addItems(list(dict.fromkeys(['  -  ' + name for name in recipe_db.get_recipe_names(self.current_menu.table)])))
        #+dessert list
        self.lW_menu.addItems(list(dict.fromkeys(['  -  ' + name for name in recipe_db.get_recipe_names(self.dessert_list)])))

    def on_card_recipe_selection(self, row, column):
        recipe_name = self.tW_menu.item(row, column).text()
        self.tW.setCurrentWidget(self.tab_recipe)
        lwi = self.lW_recipe.findItems(recipe_name, Qt.MatchExactly)[0]
        self.lW_recipe.scrollToItem(lwi)
        self.lW_recipe.setCurrentItem(lwi)
        lwi.setSelected(True)
    
    def on_history_recipe_selection(self, row, column):
        if self.tab_recipe.isEnabled():#no effect when waiting for user confirmation in history tab
            recipe_name = self.tW_history.item(row, column).text()
            self.tW.setCurrentWidget(self.tab_recipe)
            lwi = self.lW_recipe.findItems(recipe_name, Qt.MatchExactly)[0]
            self.lW_recipe.scrollToItem(lwi)
            self.lW_recipe.setCurrentItem(lwi)
            lwi.setSelected(True)
    
    def on_tab_changed(self, tab_index):
        if tab_index == 1 and self.lW_recipe.selectedItems() == []: #recipe tab selected
            #select first recipe if nothing previously selected to avoid blank fields
            self.lW_recipe.setCurrentRow(0)
            self.lW_recipe.setItemSelected(self.lW_recipe.item(0), True)
            
    def on_recipe_selection(self):
        if self.lW_recipe.count() > 0:
            #display title
            recipe_name = self.lW_recipe.currentItem().text()
            self.label_recipe_title.setText(recipe_name)
            recipe_object = self.recipe_db.get_recipe_object(recipe_name)
            #display image
            display_image(recipe_object, self.dirname, self.label_recipe_image, icon = False)
            #display instructions
            self.tE_recipe.setText(recipe_object.preparation)
            #display ingredients
            self.tE_ingredients.setText(recipe_object.ingredients_string(self.recipe_db).replace('\n', '<br/>'))
            #update tags
            tags = [self.tag_vegan, self.tag_kids, self.tag_double, self.tag_summer, self.tag_winter, self.tag_dessert, self.tag_tips]
            tags_names = ['vegan', 'kids', 'double', 'ete', 'hiver', 'dessert', 'tips']
            for tag, tag_name in zip(tags, tags_names):
                load_pic(tag, self.dirname + '/UI/images/tag_%s_%s_LD.png' % (tag_name, ['black', 'color'][recipe_object.isTagged(tag_name)]))
            if recipe_object.isTagged('midi'):
                load_pic(self.tag_lunchdinner, self.dirname + '/UI/images/tag_lunch_color_LD.png')
            elif recipe_object.isTagged('soir'):
                load_pic(self.tag_lunchdinner, self.dirname + '/UI/images/tag_dinner_color_LD.png')
            else:
                load_pic(self.tag_lunchdinner, self.dirname + '/UI/images/tag_lunch_black_LD.png')
    
    def on_recipe_link(self, link):
        self.previous_recipe_name = self.label_recipe_title.text()
        lwi = self.lW_recipe.findItems(link.toString(), Qt.MatchFixedString)[0]
        self.lW_recipe.scrollToItem(lwi)
        self.lW_recipe.setCurrentItem(lwi)
        lwi.setSelected(True)
        self.pB_back.show()
    
    def on_previous_recipe(self):
        self.pB_back.hide()
        lwi = self.lW_recipe.findItems(self.previous_recipe_name, Qt.MatchExactly)[0]
        self.lW_recipe.scrollToItem(lwi)
        self.lW_recipe.setCurrentItem(lwi)
        lwi.setSelected(True)
        
    def on_card_modif(self):
        if self.pB_modif.isChecked():
            #lock editing outside qtw
            self.pB_new_menu.setEnabled(False)
            self.dateEdit.setEnabled(False)
            self.sB_days.setEnabled(False)
            self.sB_desserts.setEnabled(False)
            self.cB_restes.setEnabled(False)
            self.pB_save.setEnabled(False)
            #replace qtwi text(+image) by combobox
            for r in range(self.tW_menu.rowCount()):
                for c in range(self.tW_menu.columnCount()):
                    if r < 2 or c < self.sB_desserts.value():
                        #create combobox
                        qcb = QComboBox(self.tW_menu)
                        #populate with recipe_db_list
                        if r < 2:
                            #remove desserts and tips from list
                            menu_list = recipe_db.get_recipe_sublist(self.recipe_db.recipe_list, tagsOut = ['dessert', 'tips'])
                            recipe_list = sorted(recipe_db.get_recipe_names(menu_list), 
                                                 key= str.lower)
                        else:
                            recipe_list = sorted(recipe_db.get_recipe_names(recipe_db.get_recipe_sublist(self.recipe_db.recipe_list,tagsIn = ['dessert'])), 
                                                 key=str.lower)
                        
                        qcb.addItems(recipe_list)
                        
                        #remember initial recipe
                        selected_recipe = self.tW_menu.item(r, c).text()
                        qcb.setCurrentText(selected_recipe)
                        #delete initial text and image
                        self.tW_menu.takeItem(r, c)
                        #add combobox to tW_menu
                        self.tW_menu.setCellWidget(r, c, qcb)
                    
        else:
            #unlock editing
            #lock editing outside qtw
            self.pB_new_menu.setEnabled(True)
            self.dateEdit.setEnabled(True)
            self.sB_days.setEnabled(True)
            self.sB_desserts.setEnabled(True)
            self.cB_restes.setEnabled(True)
            self.pB_save.setEnabled(True)
            #populate tW_menu with selected text(+image)
            #update current_menu
            self.current_menu.table = []
            self.dessert_list = []
            for c in range(self.tW_menu.columnCount()):
                for r in range(self.tW_menu.rowCount()):
                    if r < 2 or c < self.sB_desserts.value():
                        text = self.tW_menu.cellWidget(r, c).currentText()
                        recipe_object = self.recipe_db.get_recipe_object(text)
                        if r < 2:
                            self.current_menu.table.append(recipe_object)
                        else:
                            self.dessert_list.append(recipe_object)
            #call populate function
            self.populate_tW_menu(self.current_menu)
            
            #update dessert
            self.populate_tW_dessert(dessert_list = self.dessert_list)
            self.current_menu.desserts = self.dessert_list
            #update shopping and menu list
            self.populate_shopping_list()
            self.populate_menu_list()

            self.compute_score()
    
    def on_dessert_selection(self, number):

        #reset dessert row
        self.tW_menu.setRowCount(2)
        self.tW_menu.setRowCount(3)
        self.tW_menu.setVerticalHeaderLabels([' Midi ', ' Soir ', ' Desserts '])
        # self.tW_dessert.setColumnCount(number)
        if number == 0:
            load_pic(self.label_dessert, self.dirname + '/UI/images/icon_cupcake_t.png')
            # self.frame_dessert.setVisible(False)
            
            # self.tW_menu.setRowCount(2)
            self.tW_menu.hideRow(2)
            self.tW_menu.setIconSize(QSize(160, 160))
            #reset dessert list in menu object
            self.current_menu.desserts = []
            self.dessert_list = []
        else:
            load_pic(self.label_dessert, self.dirname + '/UI/images/icon_cupcake.png')
            # self.frame_dessert.setVisible(True)

            # self.tW_menu.setRowCount(3)
            self.tW_menu.showRow(2)
            self.tW_menu.setIconSize(QSize(100, 100))
            self.populate_tW_dessert()
            # self.tW_menu.setVerticalHeaderLabels(['Midi', 'Soir', 'Desserts'])

        if self.tW_menu.item(0,0) is not None:#make sure table has been generated
            self.populate_shopping_list()
            self.populate_menu_list()
    
    def on_save_menu(self):
        #self.recipe_db.history = [['date(yyyy-mm-dd)','lunch','dinner'],...]
        #self.current_menu.start_day = datetime.date , datetime.strptime('2021-10-19', '%Y-%m-%d').date()
        #last_entry_date = datetime.strptime(self.recipe_db.history[-1][0], '%Y-%m-%d').date()
        # last_entry_date = datetime.strptime(self.tW_history.verticalHeaderItem(self.tW_history.rowCount()-1).text(), '%Y-%m-%d').date()
        # first_menu_date = self.current_menu.start_day

        new_history = []
        #get current header labels
        verticalHeader_labels = [self.tW_history.verticalHeaderItem(r).text() for r in range(self.tW_history.rowCount())]
        for i in range(self.current_menu.number_of_days):
            date = self.current_menu.start_day + timedelta(days = i)
            lunch_recipe_name = self.tW_menu.item(0, i).text()
            dinner_recipe_name = self.tW_menu.item(1, i).text()
            date_text = recipe_db.date_to_text(date)
            #build new history list
            new_history.append([date_text, lunch_recipe_name, dinner_recipe_name])

        self.new_history = self.recipe_db.consider_history_update(new_history)

        for history in self.new_history:
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


            qtwi_lunch.setTextColor(QColor(215,38,49))
            qtwi_dinner.setTextColor(QColor(215,38,49))
        
        self.tW_history.setVerticalHeaderLabels(verticalHeader_labels)
        #show warning and disable other actions
        self.frame_confirm.show()
        self.tW.setTabEnabled(0, False)
        self.tW.setTabEnabled(1, False)
        
        #display history tab with modifications higlighted
        self.tW.setCurrentIndex(2)
        self.tW_history.scrollToItem(self.tW_history.item(self.tW_history.rowCount()-1, 0), QAbstractItemView.PositionAtTop)

    def reset_history(self):
        self.tW_history.clear()
        self.tW_history.setHorizontalHeaderLabels(['Midi', 'Soir'])
        self.tW_history.setRowCount(len(self.recipe_db.history))
        self.tW_history.setVerticalHeaderLabels([h[0] for h in self.recipe_db.history])
        # self.tW_history.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.tW_history.resizeColumnsToContents()
        for i, day in enumerate(self.recipe_db.history):
            date, lunch, dinner = day
            self.tW_history.setItem(i, 0, QTableWidgetItem(lunch))
            self.tW_history.setItem(i, 1, QTableWidgetItem(dinner))

        self.frame_confirm.hide()
        
    
    def on_confirm_history_update(self):
        #update rows where recipe has been replaced
        for i in range(self.tW_history.rowCount()):
            qtwi_lunch = self.tW_history.item(i, 0)
            qtwi_dinner = self.tW_history.item(i, 1)
            if qtwi_lunch.textColor().getRgb() == (215,38,49,255):
                # print(i,qtwi_lunch.textColor().getRgb())
                #take new entry
                lunch_recipe_name = qtwi_lunch.text().split(' -> ')[-1]
                dinner_recipe_name = qtwi_dinner.text().split(' -> ')[-1]
                qtwi_lunch.setText(lunch_recipe_name)
                qtwi_dinner.setText(dinner_recipe_name)
                #reset color
                qtwi_lunch.setTextColor(QColor(0,0,0))
                qtwi_dinner.setTextColor(QColor(0,0,0))
        
        #backup file
        copy2(self.recipe_db.history_file, self.dirname + '/backup/history_backup.ods')
        #update recipe_db variables and file
        self.recipe_db.update_history(self.new_history)
        
        #re-enable tabs
        self.frame_confirm.hide()
        self.tW.setTabEnabled(0, True)
        self.tW.setTabEnabled(1, True)
        
    
    def on_cancel_history_update(self):
        # print('cancel')
        self.frame_confirm.hide()
        self.tW.setTabEnabled(0, True)
        self.tW.setTabEnabled(1, True)
        self.reset_history()

    def on_ingredient_selection(self):
        #reset list menu background
        for item in [self.lW_menu.item(i) for i in range(self.lW_menu.count())]:
            item.setBackground(QBrush(QColor(183,202,185)))
            item.setTextColor(QColor(0, 0, 0))
        
        #get ingredient text
        if len(self.lW_shopping.selectedItems()) > 0:
            text = self.lW_shopping.selectedItems()[0].text()
            ingredient = text.split(' : ')[0][2:]
            for item in [self.lW_menu.item(i) for i in range(self.lW_menu.count())]:

                if self.recipe_db.get_recipe_object(item.text()[5:]).hasIngredient(ingredient):
                    item.setBackground(QBrush(QColor(92,60,146)))
                    item.setTextColor(QColor(162,213,198))
                else:
                    item.setBackground(QBrush(QColor(183,202,185)))
    
    def on_copy_shopping_list(self):
        string_to_copy = 'Liste de courses:\n'
        for item in [self.lW_shopping.item(i) for i in range(self.lW_shopping.count())]:
            string_to_copy += item.text() + '\n'
        # print(string_to_copy)
        copy(string_to_copy)

    def on_send_shopping_list(self):        
        user_id_file = self.dirname + '/user.id'
        if os.path.isfile(user_id_file):
            with open(user_id_file, 'r') as f:
                self.default_email = f.readline().strip()
            # print(self.default_email)
        else:
            text, ok = QInputDialog.getText(self, 'Enregistrement de votre adresse email', 'Votre adresse email:')
		
            if ok:
                self.default_email = text

                with open(user_id_file, 'w') as f:
                    f.write(self.default_email)

        images = [self.dirname + '/UI/images/icon_menu_3colors_LD_t.png']
        images.append(self.dirname + '/UI/images/icon_shopping_cart_LD_t.png')
        images.append(self.dirname + '/UI/images/icon_table_3colors_t.png')
        icon_dict = {'[ICON_MENU_PATH]': 'cid:%s' % (basename(images[0]))}
        icon_dict['[ICON_SHOPPING_PATH]'] = 'cid:%s' % (basename(images[1]))
        icon_dict['[ICON_TABLE_PATH]'] = 'cid:%s' % (basename(images[2]))

        # my_mailbox = mail.Mailbox()
        # my_mailbox.send_shopping_list(self.current_menu, self.default_email, images, icon_dict)
        
        # my_mailbox_worker = mail.Mailbox(self.current_menu, self.default_email, images, icon_dict)
        my_mailbox_worker = mail.Mailbox('shopping', [self.current_menu, self.default_email, images, icon_dict])
        
        my_mailbox_worker.signal.sig.connect(self.print_thread_function)
        
        self.myThreads.append(my_mailbox_worker)
        my_mailbox_worker.start()

    def on_print_shopping_list(self):
        pdf_title = self.dirname + '/Mes_Fiches/Menus/Menus(%s-%s).pdf' % (self.current_menu.start_day.strftime('%d_%m_%Y'), 
                                                                            self.current_menu.to_day().strftime('%d_%m_%Y'))
        images = [self.dirname + '/UI/images/icon_menu_3colors_LD_t.png']
        images.append(self.dirname + '/UI/images/icon_shopping_cart_LD_t.png')
        images.append(self.dirname + '/UI/images/icon_table_3colors_t.png')
        my_printer = printer.Printer(pdf_title)
        # my_printer = printer.Printer('test.pdf')
        my_printer.print_shopping_list(self.current_menu, icons=images, images=self.compute_score(draw=False))
    
    def on_send_recipe(self):
        user_id_file = self.dirname + '/user.id'
        if os.path.isfile(user_id_file):
            with open(user_id_file, 'r') as f:
                self.default_email = f.readline().strip()
            # print(self.default_email)
        else:
            text, ok = QInputDialog.getText(self, 'Enregistrement de votre adresse email', 'Votre adresse email:')
		
            if ok:
                self.default_email = text

                with open(user_id_file, 'w') as f:
                    f.write(self.default_email)

        recipe_name = self.lW_recipe.currentItem().text()
        recipe_object = self.recipe_db.get_recipe_object(recipe_name)

        images = [self.dirname + '/UI/images/icon_recipe_3colors_LD_t.png']
        images.append(self.dirname + '/UI/images/icon_table_3colors_t.png')
        icon_dict = {'[ICON_RECIPE_PATH]': 'cid:%s' % (basename(images[0]))}
        icon_dict['[ICON_TABLE_PATH]'] = 'cid:%s' % (basename(images[1]))

        recipe_pdf = self.on_print_recipe()
        
        if os.path.isfile(recipe_pdf):
            my_mailbox_worker = mail.Mailbox('recipe', [recipe_object, self.default_email, images, icon_dict, recipe_pdf])
            
            my_mailbox_worker.signal.sig.connect(self.print_thread_function)
            
            self.myThreads.append(my_mailbox_worker)
            my_mailbox_worker.start()
        else:
            print('error while creating pdf')

    def on_print_recipe(self):
        recipe_name = self.lW_recipe.currentItem().text()
        pdf_title = self.dirname + '/Mes_Fiches/Recettes/%s.pdf' % recipe_name
        recipe_object = self.recipe_db.get_recipe_object(recipe_name)

        tags_names = ['vegan', 'kids', 'double', 'ete', 'hiver', 'dessert']
        images = [self.dirname + '/UI/images/tag_%s_%s_LD.png' % (tag, ['black', 'color'][recipe_object.isTagged(tag)]) for tag in tags_names]

        my_printer = printer.Printer(pdf_title)
        my_printer.print_recipe(recipe_object, images)

        return pdf_title

    def compute_score(self, draw = True):
        tags = [self.score_double, self.score_kids, self.score_vegan, self.score_summer, self.score_winter]
        tags_names = ['double', 'kids', 'vegan', 'ete', 'hiver']
        score = dict(zip(tags_names, [self.current_menu.tag_score(tag_name) for tag_name in tags_names]))
        
        if draw:
            for tag, tag_name in zip(tags, tags_names):
                load_pic(tag, self.dirname + '/UI/images/score_%s_%s.png' % (tag_name, score[tag_name]))

        return [self.dirname + '/UI/images/score_%s_%s.png' % (tag_name, score[tag_name]) for tag, tag_name in zip(tags, tags_names)]
    
    def on_filter_selection(self):
        if self.pB_filter.isChecked():
            #extract filter values
            with_list = self.lE_with.text().split(',')
            without_list = self.lE_without.text().split(',')
            filtered_list = []
            total_recipe_count = self.lW_recipe.count()
            for recipe_object in [self.recipe_db.get_recipe_object(self.lW_recipe.item(i).text()) for i in range(total_recipe_count)]:
                #with
                is_selected = True
                for with_text in with_list: #must meet all the with criteria
                    is_selected *= recipe_object.meet_with_criteria(with_text)
                #without
                for without_text in without_list: #must meet all the without criteria
                    is_selected *= recipe_object.meet_without_criteria(without_text)
                if is_selected:
                    filtered_list.append(recipe_object)

            #reset list
            self.lW_recipe.clear()
            self.lW_recipe.addItems(recipe_db.get_recipe_names(filtered_list))
            if filtered_list != []:
                self.lW_recipe.setCurrentRow(0)

            #display result summary on search label
            self.cB_search.setText('Recherche (%s/%s)' % (len(filtered_list), total_recipe_count))
        else:
            #reset list
            self.lW_recipe.clear()
            #repopulate recipe list
            self.lW_recipe.addItems(recipe_db.get_recipe_names(self.recipe_db.recipe_list))

            #reset search label
            self.cB_search.setText('Recherche')
    
    def on_new_recipe(self):
        # print('new recipe')
        #disable other tabs
        self.tW.setTabEnabled(0, False)
        self.tW.setTabEnabled(2, False)
        self.cB_search.setEnabled(False)
        self.pB_new_recipe.setEnabled(False)
        #reset all fields
        self.label_newedit.setText('Nouvelle Recette')
        self.lE_title.setText('Nouveau Titre')
        self.label_image_2.setPixmap(QPixmap())
        self.tW_ingredients.clear()
        self.tW_ingredients.setColumnCount(1)
        self.tW_ingredients.setRowCount(0)
        self.lE_qty.clear()
        self.tB_preparation.clear()
        tags = [self.cB_tagdessert, self.cB_tagdinner, self.cB_tagdouble, self.cB_tagkids, self.cB_taglunch,
                self.cB_tagsummer, self.cB_tagwinter, self.cB_tagvegan, self.cB_tagtips]
        for tag in tags:
            tag.setChecked(False)
        
        self.cB_ingredient.clear()
        self.cB_unit.clear()
        ingredients, units = self.recipe_db.get_ingredients_units_list()
        self.cB_ingredient.addItems([''] + ingredients)
        self.cB_unit.addItems([''] + units)
        self.cB_ingredient.setCurrentIndex(0)
        self.cB_unit.setCurrentIndex(0)
        
        self.sB_time.setValue(0)
        #create pushButton list
        self.pB_remove_list = []
        
        
    
    def on_edit_recipe(self):
        #disable other tabs
        self.tW.setTabEnabled(0, False)
        self.tW.setTabEnabled(2, False)
        self.cB_search.setEnabled(False)
        self.pB_modif_2.setEnabled(False)
        #populate all fields
        self.label_newedit.setText('Modifier la recette')
        recipe_name = self.lW_recipe.currentItem().text()
        self.lE_title.setText(recipe_name)
        recipe_object = self.recipe_db.get_recipe_object(recipe_name)
        display_image(recipe_object, self.dirname, self.label_image_2, icon=False)
        
        self.tW_ingredients.clear()
        ing_list = recipe_object.ingredients_string_list()
        self.tW_ingredients.setColumnCount(1)
        self.tW_ingredients.setRowCount(len(ing_list))
        
        #create pushButton list
        self.pB_remove_list = []
        for r, ing in enumerate(ing_list):
            qtwi = QTableWidgetItem(ing)
            self.tW_ingredients.setItem(r, 0, qtwi)
            if ing != '' and ing != 'Optionnel :':
                pB_widget, pB_remove = self.create_qtwi_pb(ing)
                
                self.tW_ingredients.setCellWidget(r, 0, pB_widget)
                self.pB_remove_list.append(pB_remove)
        
        self.cB_ingredient.clear()
        self.cB_unit.clear()
        ingredients, units = self.recipe_db.get_ingredients_units_list()
        self.cB_ingredient.addItems([''] + ingredients)
        self.cB_unit.addItems([''] + units)
        self.cB_ingredient.setCurrentIndex(0)
        self.cB_unit.setCurrentIndex(0)
        
        if recipe_object.time is not None:
            self.sB_time.setValue(int(recipe_object.time))
        else:
            self.sB_time.setValue(0)
        
        tags = [self.cB_tagdessert, self.cB_tagdinner, self.cB_tagdouble, self.cB_tagkids, self.cB_taglunch,
                self.cB_tagsummer, self.cB_tagwinter, self.cB_tagvegan, self.cB_tagtips]
        tag_names = ['dessert', 'soir', 'double', 'kids', 'midi', 'ete', 'hiver', 'vegan', 'tips']
        for tag, tag_name in zip(tags, tag_names):
            tag.setChecked(recipe_object.isTagged(tag_name))
        
        self.tB_preparation.setText(recipe_object.preparation)

    def create_qtwi_pb(self, ingredient):
        pB_widget = QWidget(self.tW_ingredients)
        pB_remove = QPushButton('', self.tW_ingredients)
        pB_remove.setFixedSize(25,25)
        pB_remove.setIconSize(QSize(18,18))
        pB_remove.setIcon(QIcon(self.dirname + '/UI/images/icon_bin.png'))
        pB_remove.setToolTip('Supprimer : ' + ingredient)
        pB_remove.setCheckable(True)
        pB_remove.clicked.connect(self.on_delete_ingredient)
        label_ing = QLabel(ingredient, self.tW_ingredients)
        layout_pB = QHBoxLayout(pB_widget)
        layout_pB.addWidget(label_ing)
        layout_pB.addWidget(pB_remove)
        layout_pB.setContentsMargins(0,0,0,0)
        
        return pB_widget, pB_remove
        
        
        
    def on_delete_ingredient(self):
        for pB in self.pB_remove_list:
            if pB.isChecked():
                ing = pB.toolTip().split('Supprimer : ')[-1]
                self.tW_ingredients.removeRow(self.tW_ingredients.findItems(ing, Qt.MatchExactly)[0].row())
                self.pB_remove_list.remove(pB)
                break
        
        #if last optional deleted, delete last 2 rows
        if self.tW_ingredients.item(self.tW_ingredients.rowCount()-1, 0).text() == 'Optionnel :':
            self.tW_ingredients.removeRow(self.tW_ingredients.rowCount()-1)
            self.tW_ingredients.removeRow(self.tW_ingredients.rowCount()-1)

        
    def on_add_ingredient(self):
        ing = self.cB_ingredient.currentText()
        qty = self.lE_qty.text()
        unit = self.cB_unit.currentText()
        
        text = '- %s : %s%s' % (ing, qty, unit)
        
        #if not optional and optional does not exist, append
        #if not optional and optional exists, add before optional row
        #if optional and optional does not exist, create optional row and append
        #if optional and optional exists, append
        already_in = False
        ing_in = ''
        for r in range(self.tW_ingredients.rowCount()):
            # print('--%s--' % ing, '--%s--' % self.tW_ingredients.item(r, 0).text().split(' :')[0].split('- ')[-1])
            if ing == self.tW_ingredients.item(r, 0).text().split(' :')[0].split('- ')[-1]:
                already_in = True
                ing_in = self.tW_ingredients.item(r, 0).text()
                break
        
        if not already_in:#make sure ingredient does not already exist (avoid conflict with delete function)
        
            if self.pB_option.isChecked():#if optional
                if self.tW_ingredients.findItems('Optionnel :', Qt.MatchExactly) == []:#and optional does not exist
                    #create optional row 
                    rowCount = self.tW_ingredients.rowCount()
                    self.tW_ingredients.insertRow(rowCount)
                    self.tW_ingredients.setItem(rowCount, 0, QTableWidgetItem(''))
                    self.tW_ingredients.insertRow(rowCount+1)
                    self.tW_ingredients.setItem(rowCount+1, 0, QTableWidgetItem('Optionnel :'))
                    self.tW_ingredients.insertRow(rowCount+2)
                    #and append
                    qtwi = QTableWidgetItem(text)
                    self.tW_ingredients.setItem(rowCount+2, 0, qtwi)
                    pB_widget, pB_remove = self.create_qtwi_pb(text)
                    self.tW_ingredients.setCellWidget(rowCount+2, 0, pB_widget)
                    self.pB_remove_list.append(pB_remove)
                
                else:#and optional exists
                    #append
                    rowCount = self.tW_ingredients.rowCount()
                    self.tW_ingredients.insertRow(rowCount)
                    qtwi = QTableWidgetItem(text)
                    self.tW_ingredients.setItem(rowCount, 0, qtwi)
                    pB_widget, pB_remove = self.create_qtwi_pb(text)
                    self.tW_ingredients.setCellWidget(rowCount, 0, pB_widget)
                    self.pB_remove_list.append(pB_remove)
            else:#if not optional
                if self.tW_ingredients.findItems('Optionnel :', Qt.MatchExactly) == []:#and optional does not exist
                    #append
                    rowCount = self.tW_ingredients.rowCount()
                    self.tW_ingredients.insertRow(rowCount)
                    qtwi = QTableWidgetItem(text)
                    self.tW_ingredients.setItem(rowCount, 0, qtwi)
                    pB_widget, pB_remove = self.create_qtwi_pb(text)
                    self.tW_ingredients.setCellWidget(rowCount, 0, pB_widget)
                    self.pB_remove_list.append(pB_remove)
                else:#and optional exists
                    #add before optional row
                    r = self.tW_ingredients.findItems('Optionnel :', Qt.MatchExactly)[0].row()-1
                    self.tW_ingredients.insertRow(r)
                    qtwi = QTableWidgetItem(text)
                    self.tW_ingredients.setItem(r, 0, qtwi)
                    pB_widget, pB_remove = self.create_qtwi_pb(text)
                    self.tW_ingredients.setCellWidget(r, 0, pB_widget)
                    self.pB_remove_list.append(pB_remove)
        else:
            # print('tu en as deja mis!')
            error_dialog = QMessageBox(self)
            error_dialog.setWindowTitle('Attention')
            error_dialog.setWindowModality(Qt.WindowModal)
            error_dialog.setText('Cet ingrédient est déjà dans la recette : "%s"' % ing_in)
            error_dialog.setIcon(QMessageBox.Warning)
            # error_dialog.setDetailedText(text)
            error_dialog.exec_()
            
    
    def on_tag_selected(self, cB):
        tags = {'cB_tagdinner': [1, 0, 1, 1, 0, 1, 1, 1, 0],
                'cB_tagdessert': [0, 1, 0, 1, 0, 1, 1, 1, 0],
                'cB_tagdouble': [1, 0, 1, 1, 1, 1, 1, 1, 0],
                'cB_tagkids': [1, 1, 1, 1, 1, 1, 1, 1, 0],
                'cB_taglunch': [0, 0, 1, 1, 1, 1, 1, 1, 0],
                'cB_tagwinter': [1, 1, 1, 1, 1, 1, 0, 1, 0],
                'cB_tagsummer': [1, 1, 1, 1, 1, 0, 1, 1, 0],
                'cB_tagvegan': [1, 1, 1, 1, 1, 1, 1, 1, 0],
                'cB_tagtips': [0, 0 ,0, 0, 0, 0, 0, 0, 1]
        }
        
        if cB.isChecked():
            bool_matrix = tags[cB.objectName()]
            for other_cB, checkable in zip(self.selectable_tags, bool_matrix):
                if other_cB.isChecked() and not checkable:
                    other_cB.setChecked(checkable)
    
    def on_add_photo(self):
        self.recipe_image_path, filter = QFileDialog.getOpenFileName(self, 'Choisir une image', self.dirname, 'Images (*.png *.jpg)')
        # print(image_path=='')
        display_new_image(self.recipe_image_path, self.label_image_2)
        
        
        
    def on_confirm_recipe(self):
        #check if ok to save
        #title not empty
        title = self.lE_title.text()
        title_empty =  title == ''
        
        #if not ok to save -> warning message
        if title_empty:
            error_dialog = QMessageBox(self)
            error_dialog.setWindowTitle('Attention')
            error_dialog.setWindowModality(Qt.WindowModal)
            error_dialog.setText('Il manque au moins un titre pour la recette')
            error_dialog.setIcon(QMessageBox.Warning)
            # error_dialog.setDetailedText(text)
            error_dialog.exec_()
        elif self.label_newedit.text() == 'Nouvelle Recette' and self.recipe_db.contains(title):#recipe already exists
            error_dialog = QMessageBox(self)
            error_dialog.setWindowTitle('Attention')
            error_dialog.setWindowModality(Qt.WindowModal)
            error_dialog.setText('Cette recette existe déjà, choisir "Modifier la recette" au lieu de "Nouvelle recette"')
            error_dialog.setIcon(QMessageBox.Warning)
            # error_dialog.setDetailedText(text)
            error_dialog.exec_()
        else:
            #case with/without picture to be saved (filename = new_title.jpg and new_title_icon.jpg)
            if self.recipe_image_path != '':
                image_cell = title.lower().replace(' ', '_') #to be written in cell
                filepath = self.dirname + '/images/%s.jpg' % image_cell #to be saved
                filpath_icon = self.dirname + '/images/%s_icon.jpg' % image_cell #to be saved
                #try to save it to file:
                qpix = QPixmap(self.recipe_image_path)
                if qpix.width() > qpix.height():
                    # qpix_scaled = qpix.scaled(400, 300)
                    qpix_scaled = qpix.scaled(1333, int(1333/qpix.width()*qpix.height()))
                    qpix_scaled_icon = qpix.scaled(400, int(400/qpix.width()*qpix.height()))
                else:
                    # qpix_scaled = qpix.scaled(300, 400)
                    qpix_scaled = qpix.scaled(int(1333/qpix.height()*qpix.width()), 1333)
                    qpix_scaled_icon = qpix.scaled(int(400/qpix.height()*qpix.width()), 400)
                    
                image_file = QFile(filepath)
                image_file.open(QIODevice.WriteOnly)
                qpix_scaled.save(filepath, 'JPG')
                
                image_file_icon = QFile(filpath_icon)
                image_file_icon.open(QIODevice.WriteOnly)
                qpix_scaled_icon.save(filpath_icon, 'JPG')
                
                #reset internal variable
                self.recipe_image_path = ''
            else:
                image_cell = ''
                
            image = ''
            if image_cell != '':
                image = '/images/' + image_cell
            #case with ingredients not empty -> combine ingredients to string
            now_optionals = False
            ing_cell = ''
            ing_list = []
            ing_dict = {}
            for r in range(self.tW_ingredients.rowCount()):
                full_ing_description = self.tW_ingredients.item(r, 0).text()
                if full_ing_description != '' and full_ing_description != 'Optionnel :':
                    raw_ing, raw_qty = full_ing_description.split(' : ')
                    ing = raw_ing[2:]
                    qty = extract_number(raw_qty)
                    if qty is None:
                        qty = '1'
                        unit = '()'
                    else:
                        unit = raw_qty.replace(qty, '')
                    if now_optionals:
                        ing = '[%s]' % ing
                    ing_dict[ing] = [qty, unit]
                else:
                    now_optionals = True
                
                ing_list.append('%s,%s,%s' % (ing, qty, unit))
            ing_cell = '/'.join(ing_list)
                    
            #combine tags to string
            tags = [self.cB_tagdessert, self.cB_tagdinner, self.cB_tagdouble, self.cB_tagkids, self.cB_taglunch,
                    self.cB_tagsummer, self.cB_tagwinter, self.cB_tagvegan, self.cB_tagtips]
            tag_names = ['dessert', 'soir', 'double', 'kids', 'midi', 'ete', 'hiver', 'vegan', 'tips']
            tag_checked_list = [tag_name for tag, tag_name in zip(tags, tag_names) if tag.isChecked()]
            tag_cell = '/'.join(tag_checked_list)
            #case with preparation not empty -> combine preparation to string
            preparation_cell = self.tB_preparation.toPlainText()
            #case with preparation time not 0
            time_cell = ''
            if self.sB_time.text() != '0':
                time_cell = self.sB_time.text()
            
            time = None
            if time_cell != '':
                time = time_cell

            #update recipe_db
            newedit_recipe = Recipe(title, ing_dict, preparation_cell, time, tag_checked_list, image)
            if self.label_newedit.text() == 'Modifier la recette':#update recipe_db
                initial_recipe_name = self.lW_recipe.currentItem().text()
                index_of_recipe = recipe_db.get_recipe_names(self.recipe_db.recipe_list).index(initial_recipe_name)
                self.recipe_db.recipe_list[index_of_recipe] = newedit_recipe
                
            else:#add new recipe
                self.recipe_db.recipe_list.append(newedit_recipe)
                
            #update qlw
            self.lW_recipe.clear()
            recipe_list = sorted(recipe_db.get_recipe_names(self.recipe_db.recipe_list), key=str.lower)
            self.lW_recipe.addItems(recipe_list)
            
            #backup file
            copy2(self.recipe_db.recipe_file, self.dirname + '/backup/recipe_backup.ods')
            #update recipe sheet (fully rewrite)
            self.recipe_db.update_recipe_file()
            #TODO info message recipe correctly created/updated
        #reenable other tabs
        self.tW.setTabEnabled(0, True)
        self.tW.setTabEnabled(2, True)
        self.cB_search.setEnabled(True)
        self.pB_new_recipe.setEnabled(True)
        self.pB_modif_2.setEnabled(True)
        self.pB_delete.setEnabled(True)
        self.pB_new_recipe.setChecked(False)
        self.pB_modif_2.setChecked(False)
    
    def on_delete_recipe(self):
        #TODO
        #check if a recipe is selected
        recipe_name = self.lW_recipe.currentItem().text()
        recipe_object = self.recipe_db.get_recipe_object(recipe_name)
        if recipe_name != '':
        #confirmation window
            confirm_dialog = QMessageBox(self)
            confirm_dialog.setWindowTitle('Attention')
            confirm_dialog.setWindowModality(Qt.WindowModal)
            confirm_dialog.setText('Voulez-vous vraiment supprimer la recette "%s" ?' % recipe_name)
            confirm_dialog.setIcon(QMessageBox.Warning)
            yesButton = confirm_dialog.addButton("Oui", QMessageBox.YesRole)
            noButton = confirm_dialog.addButton("Non", QMessageBox.NoRole)
            confirm_dialog.setDefaultButton(noButton)
            
            #confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            # confirm_dialog.setDetailedText(text)
            answer = confirm_dialog.exec_()
            if not answer:
                print('removing %s' % recipe_name)
        #update recipe_db
        #update qlw
        #backup file
        #update recipe sheet (fully rewrite)
        #info message recipe correctly removed
        print(recipe_name)
    
    def on_cancel_recipe(self):
        # print('cancel recipe')
        #reenable other tabs
        self.tW.setTabEnabled(0, True)
        self.tW.setTabEnabled(2, True)
        self.cB_search.setEnabled(True)
        self.pB_new_recipe.setEnabled(True)
        self.pB_modif_2.setEnabled(True)
        self.pB_delete.setEnabled(True)
        self.pB_new_recipe.setChecked(False)
        self.pB_modif_2.setChecked(False)


def load_pic(widget, picture_path):
    # picture_path = "/home/jv/Documents/MyScripts/VSCODE/PY/Recipe/UI/images/restaurant_background2.jpg"
    picture = QPixmap(picture_path)
    widget.setPixmap(picture)


def display_image(recipe_object, dirname, widget, icon = True):
    if icon:
        if recipe_object is None:#special case for header icon
            image_path = dirname
            icon = QIcon()
            qpix = QPixmap(image_path)
            icon.addPixmap(qpix, mode = QIcon.Selected, state = QIcon.On)
            widget.setSizeHint(QSize(60, 60))
            widget.setIcon(icon)

        elif recipe_object.image != '' and recipe_object.image != '/images/':
            image_path = dirname + recipe_object.image + '_icon.jpg'
            # icon = QIcon()
            qpix = QPixmap(image_path)

            qpix_to_widget(qpix, widget)

    else:
        if recipe_object.image != '' and recipe_object.image != '/images/':
            image_path = dirname + recipe_object.image + '.jpg'
            qpix = QPixmap(image_path)


            if qpix.width() > qpix.height():
                # qpix_scaled = qpix.scaled(400, 300)
                qpix_scaled = qpix.scaled(270, 200)
            else:
                # qpix_scaled = qpix.scaled(300, 400)
                qpix_scaled = qpix.scaled(200, 270)

            # print('-%s-' % recipe_object.image)
            qpix_to_widget(qpix_scaled, widget, icon=False)
            
        else:
            widget.setPixmap(QPixmap())

def display_new_image(image_path, widget, icon = False):
    qpix = QPixmap(image_path)

    if qpix.width() > qpix.height():
        # qpix_scaled = qpix.scaled(400, 300)
        qpix_scaled = qpix.scaled(270, 200)
    else:
        # qpix_scaled = qpix.scaled(300, 400)
        qpix_scaled = qpix.scaled(200, 270)
        
    qpix_to_widget(qpix_scaled, widget, icon)

def qpix_to_widget(qpix, widget, icon = True):
    x_size, y_size = qpix.width(), qpix.height()
    rounded = QPixmap(x_size, y_size)
    rounded.fill(Qt.transparent)
    path = QPainterPath()
    path.addRoundedRect(rounded.rect(), 25, 25, mode=Qt.RelativeSize)
    painter = QPainter()
    painter.begin(rounded)
    painter.setClipPath(path)
    painter.fillRect(rounded.rect(), Qt.transparent)
    x = int((qpix.width() - x_size)/2)
    y = int((qpix.height() - y_size)/2)
    painter.drawPixmap(x, y, qpix.width(), qpix.height(), qpix)
    painter.end()
    if icon:
        widget.setIcon(QIcon(rounded))
    else:
        widget.setPixmap(rounded)

def image_from_base64(base64_table, image_name):
    with open(base64_table, 'r') as f:
        data = f.readlines()
    for line in data:
        if image_name == line.split(':')[0]:
            base64 = line.split('ICON_MENU_PATH:<img src="')[1].strip()[:-3]
            return base64

def extract_number(string):
    number = []
    no_decimal = True
    for c in string:
        if c.isdigit() or (c == '.' and no_decimal):
            number.append(c)
            if c == '.':
                no_decimal = False
        else:

            return ''.join(number)

def start(recipe_db):
    
    app = QApplication(sys.argv)
    
    dirname = os.path.dirname(__file__)
    myUiFile = dirname + '/UI/Main_Window.ui'
    w = QUiLoader().load(myUiFile)

    myGUI = MainGUI(parent = w, recipe_db = recipe_db)
    
    
    myGUI.main()
    # for i in range(100):
    #     myGUI.pB_new_menu.click()
    
    sys.exit(app.exec_())

def debug():
    
    #Backend code debug
    # input_csv = '/home/jv/Documents/MyScripts/VSCODE/PY/Recipe/MesRecettes.ods'
    # my_recipe_DB = recipe_db.RecipeDB(input_csv)
    # print(myRecipeDB.recipe_list[23].background_score)

    # b = full_background(input_csv)
    # print(b)

    # myMenu = menu.Menu()
    # myMenu.start_day = datetime.now().date()
    # myMenu.generate_smart_menu(my_recipe_DB)
    # for i in range(100):
    #     myMenu.generate_random_menu(my_recipe_DB)
    #     myMenu.use_double()
    # print(recipe_db.get_recipe_names(myMenu.table))
    # print(myMenu.full_menu())
    # print(myMenu.tag_score('vegan'))
    
    # pass
    
    s = '1.5c. a c.'
    qty = extract_number(s)
    print(qty)

def main():
    dirname = os.path.dirname(__file__)
    # input_recipe = dirname + '/MesRecettes (copy).ods'
    input_recipe = dirname + '/MesRecettes.ods'
    input_history = dirname + '/Historique.ods'
    
    my_recipe_DB = recipe_db.RecipeDB(recipe_file= input_recipe, history_file= input_history)
    start(my_recipe_DB)

class TableWidgetCustom(QTableWidget):
    def __init__(self, parent=None):
        super(TableWidgetCustom, self).__init__(parent)
    
    def viewOptions(self) -> PySide2.QtWidgets.QStyleOptionViewItem:
        option = QTableWidget.viewOptions(self)
        option.decorationAlignment = Qt.AlignHCenter | Qt.AlignCenter
        option.decorationPosition = QStyleOptionViewItem.Top
        # return super().viewOptions()
        return option

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    main()
    # debug()
    # app = QApplication(sys.argv)
    
    # dirname = os.path.dirname(__file__)
    # myUiFile = dirname + '/Main_Window.ui'

    # w = QUiLoader().load(myUiFile)

    # myGUI = MainGUI(w)
    # myGUI.main()
    
    
    # sys.exit(app.exec_())
    