import datetime
from re import split
from uid_widget import UIDWidget
from ingredient import Ingredient
import string
from ingredient_item import IngredientItem
from stacked_recipes import StackedRecipes, RecipeCard
from user_settings import UserSettings
from history import History
from edit_recipe import EditRecipe
from time_edition import TimeEdition
from right_click_menu import RightClickMenu
from line_recipe import LineRecipe
from stylesheet_update import COLORS
import os
from os.path import basename
import time

from PySide2 import QtCore
from PySide2 import QtGui
from recipe import Recipe
import sys
import recipe_db
import menu
import google_api as gapi
import printer
import html_parser as web
import custom_widgets as cw
import stacked_recipes as sr
from datetime import date, timedelta
from pyperclip import copy
from shutil import copy2
# import pyautogui
import uuid

import PySide2
from PySide2.QtWidgets import*
# QApplication, QWidget, QPushButton, QTableWidget, QSpinBox
from PySide2.QtGui import QBrush, QDoubleValidator, QMovie, QPainterPath, QPixmap, QIcon, QColor, QPainter, QFontDatabase, QFont, QWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import*
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
# from PySide2 import QtQuickWidgets
# QDate

#COLOR THEME HISTORY
RED = '#d72631' #215,38,49
LIGHT_GREEN = '#a2d5c6' #162,213,198
FADED_LIGHT_GREEN = '#b7cab9' #183,202,185
GREEN = '#077b8a' #7,123,138
VIOLET = '#5c3c92' #92,60,146
BEIGE = '#ccc1ae' #204,193,174
LIGHT_BEIGE = '#e8ddc8' #232,221,200

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
        
        self.save_components()
        self.initial_state(recipe_db)
        self.connect_actions()
        self.update_modif()

        self.set_custom_font()

        #generate default menu at startup
        self.pB_new_menu.click()

    def set_custom_font(self):
        fontDir = self.dirname + '/fonts/aller-font/Aller_It.ttf'
        QFontDatabase.addApplicationFont(fontDir)
       
        self.parentWidget().setStyleSheet("QWidget{font-family:Aller;}" + self.parentWidget().styleSheet())
        self.tB.setFont(QFont('Aller', 20, QtGui.QFont.Light))
        self.lW_shopping.setFont(QFont('Aller', 13, QtGui.QFont.Bold))
        self.lW_menu.setFont(QFont('Aller', 13, QtGui.QFont.Bold))
        self.tW_menu.setFont(QFont('Aller', 13, QtGui.QFont.Light))
        self.tW_menu.verticalHeader().setFont(QFont('Aller', 10, QtGui.QFont.Bold))
        self.tW_menu.horizontalHeader().setFont(QFont('Aller', 10, QtGui.QFont.Bold))
        self.cB_restes.setFont(QFont('Aller', 14, QtGui.QFont.Bold))

    def save_components(self):
        self.pW = self.parentWidget()
        #-- ui widgets --
        self.tW: QTabWidget
        self.tW = self.pW.tabWidget
        self.frame: QFrame
        self.frame = self.pW.frame
        self.frame_settings: QFrame
        self.frame_settings = self.pW.frame_settings
        #-tab menu
        self.tab_menus: QWidget
        self.tab_menus = self.pW.tab_menus
        self.tB: QToolBox
        self.tB = self.pW.toolBox
        self.frame_top_actions: QFrame
        self.frame_top_actions = self.pW.frame_top_actions
        self.vL_time: QVBoxLayout
        self.vL_time = self.pW.vL_time
        self.cB_restes: QCheckBox
        self.cB_restes = self.pW.cB_restes_2
        self.p_carte: QWidget
        self.p_carte = self.pW.page_carte
        # self.pB_save: QPushButton
        # self.pB_save = self.pW.pB_save
        self.cB_calendar: QCheckBox
        self.cB_calendar = self.pW.cB_calendar
        self.cB_history: QCheckBox
        self.cB_history = self.pW.cB_history
        self.pB_calendar: QPushButton
        self.pB_calendar = self.pW.pB_calendar
        self.pB_new_menu: QPushButton
        self.pB_new_menu = self.pW.pB_new_menu_2
        self.tW_menu: QTableWidget
        self.tW_menu = self.pW.tW_menu
        self.label_lunch: QLabel
        self.label_lunch = self.pW.label_lunch
        self.label_dinner: QLabel
        self.label_dinner = self.pW.label_dinner
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
        self.tE_ingredients: QTextEdit
        self.tE_ingredients = self.pW.tE_ingredients
        self.tE_recipe: QTextBrowser
        self.tE_recipe = self.pW.tE_recipe
        self.lW_recipe: QListWidget
        self.lW_recipe = self.pW.lW_recettes
        self.cB_search: QCheckBox
        self.cB_search = self.pW.cB_recherche
        self.cB_search_recipe_name: QCheckBox
        self.cB_search_recipe_name = self.pW.cB_search_recipe_name
        self.cB_search_ingredients: QCheckBox
        self.cB_search_ingredients = self.pW.cB_search_ingredients
        self.cB_search_preparation: QCheckBox
        self.cB_search_preparation = self.pW.cB_search_preparation
        self.cB_search_tag_double: QCheckBox
        self.cB_search_tag_double = self.pW.cB_search_tag_double
        self.cB_search_tag_kids: QCheckBox
        self.cB_search_tag_kids = self.pW.cB_search_tag_kids
        self.cB_search_tag_vegan: QCheckBox
        self.cB_search_tag_vegan = self.pW.cB_search_tag_vegan
        self.cB_search_tag_summer: QCheckBox
        self.cB_search_tag_summer = self.pW.cB_search_tag_summer
        self.cB_search_tag_winter: QCheckBox
        self.cB_search_tag_winter = self.pW.cB_search_tag_winter
        self.cB_search_tag_dessert: QCheckBox
        self.cB_search_tag_dessert = self.pW.cB_search_tag_dessert
        self.cB_search_tag_dinner: QCheckBox
        self.cB_search_tag_dinner = self.pW.cB_search_tag_dinner
        self.cB_search_tag_lunch: QCheckBox
        self.cB_search_tag_lunch = self.pW.cB_search_tag_lunch
        self.cB_search_tag_tips: QCheckBox
        self.cB_search_tag_tips = self.pW.cB_search_tag_tips
        self.frame_search: QFrame
        self.frame_search = self.pW.frame_recherche
        self.frame_edit_recipe: QFrame
        self.frame_edit_recipe = self.pW.frame_edit_recipe
        self.lE_with: QLineEdit
        self.lE_with = self.pW.lE_with
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
        self.vL_edit_recipe: QVBoxLayout
        self.vL_edit_recipe = self.pW.vL_edit_recipe
        #tab settings
        self.vL_settings: QVBoxLayout
        self.vL_settings = self.pW.vL_settings
    
    def initial_state(self, my_recipe_db):
        #variables
        self.recipe_db: recipe_db.RecipeDB
        self.recipe_db = my_recipe_db
        self.current_menu = menu.Menu()
        self.dessert_list = []
        # self.dirname = os.path.dirname(__file__)
        self.dirname = os.path.dirname(os.path.abspath(__file__))
        self.just_dropped = False
        self.cell_signal_count = 0
        self.from_cell = ()
        self.to_cell = ()
        self.html_source_file_shopping = self.dirname + '/shopping_core.html'
        
        self.default_email = ''
        self.default_nb_days = 7
        self.default_storage = self.dirname + '/Mes_Fiches/'
        self.homepage = QUrl("https://www.google.com/")
        self.user_id_file = self.dirname + '/user.id'
        
        self.recipe_image_path = ''
        self.myThreads = []
        self.delete_flag = False
        self.contact = 'notification.a.table@gmail.com'
        self.stacks = {}
        self.lockKeyId = 'xx'
        self.lockedForEdition = False
        self.recipeMultiSelection = []
        
        

        self.init_colors = {'RED' :         ('#d72631', [215,38,49]),
                    'LIGHT_GREEN' :         ('#a2d5c6', [162,213,198]),
                    'FADED_LIGHT_GREEN' :   ('#b7cab9', [183,202,185]),
                    'GREEN' :               ('#077b8a', [7,123,138]),
                    'VIOLET' :              ('#5c3c92', [92,60,146]),
                    'BEIGE' :               ('#ccc1ae', [204,193,174]),
                    'LIGHT_BEIGE' :         ('#e8ddc8', [232,221,200])
                    }

        self.init_colors = {
                    '#color1_bright#'   : '#16d9f3',
                    '#color1#'          : '#0aacc2',
                    '#color1_dark#'     : '#077b8a',
                    '#color2_bright#'   : '#e3636c',
                    '#color2#'          : '#d72631',
                    '#color2_dark#'     : '#ad1f28',
                    '#color3_bright#'   : '#7751b8',
                    '#color3#'          : '#5c3c92',
                    '#color3_dark#'     : '#3f2965',
                    '#color4_bright#'   : '#b7cab9',
                    '#color4#'          : '#a2d5c6',
                    '#color4_dark#'     : '#80c6b1',
                    '#color5_bright#'   : '#e8ddc8',
                    '#color5#'          : '#ccc1ae',
                    '#color5_dark#'     : '#b8a98e'
        }
        
        self.colors = COLORS
        
        # cw.style_factory(self.pW, init_colors = self.init_colors, colors = self.colors)
        
        #default state
        self.window().setWindowState(Qt.WindowMaximized)
        #-replace qtablewidget tW_menu by custom class
        new_tW_menu = cw.TableWidgetCustom(self.pW)
        new_tW_menu.setRowCount(3)
        # new_tW_menu.setVerticalHeaderLabels([' Midi ', ' Soir ', ' Desserts '])
        new_tW_menu.verticalHeader().hide()
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
        new_tW_menu.setLineWidth(0)
        new_tW_menu.setShowGrid(False)
        new_tW_menu.setStyleSheet(self.pW.styleSheet())
        self.pW.gridLayout_4.replaceWidget(self.tW_menu, new_tW_menu)
        self.tW_menu = new_tW_menu
        self.pW.tW_menu.setParent(None)
        
        self.tW_menu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_menu.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_menu.setIconSize(QSize(160, 160))
        self.tW_menu.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tW_menu.viewport().installEventFilter(self)
        
        # self.pB_save.setEnabled(False)
        
        self.info_dialog = QMessageBox(self)

        # self.tW_shopping.setVisible(False)
        # recipe_list = sorted(recipe_db.get_recipe_names(self.recipe_db.recipe_list), key=str.lower)
        # self.lW_recipe.addItems(recipe_list)
        self.reset_recipes_list()
        self.lW_recipe.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.lW_recipe.setMouseTracking(True)
        self.pB_back.hide()      

        # self.populate_lW_recipe()
        
        self.frame_settings.hide()
        self.frame_search.hide()
        
        #User settings
        self.init_user_settings()
        self.user_settings_pB()
        
        self.time_edition = TimeEdition(self.default_nb_days)
        self.vL_time.addWidget(self.time_edition)
        
        #init edit_recipe
        self.init_edit_recipe()
        self.frame_edit_recipe.hide()
        
        #self.tW_ingredients.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.tW_ingredients.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
         
        #images
        self.window().setWindowIcon(QIcon(self.dirname + '/UI/images/donut.png'))

        # cw.load_pic(self.label_dessert, self.dirname + '/UI/images/icon_cupcake_t.png')
        # cw.load_pic(self.label_user, self.dirname + '/UI/images/icon_user_color.png')
        # load_pic(self.label_dessert_2, self.dirname + '/UI/images/tag_dessert_color_LD.png')
        self.tW.setTabIcon(0,QIcon(self.dirname + '/UI/images/icon_chef_3colors.png'))
        self.tW.setTabIcon(1,QIcon(self.dirname + '/UI/images/icon_recipe_3colors.png'))
        self.tW.setTabIcon(2,QIcon(self.dirname + '/UI/images/icon_plate_3colors.png'))
        self.tB.setItemIcon(0, QIcon(self.dirname + '/UI/images/icon_menu_3colors.png'))
        self.tB.setItemIcon(1, QIcon(self.dirname + '/UI/images/icon_shopping_cart.png'))
        self.pB_user.setIcon(QIcon(self.dirname + '/UI/images/icon_user_t.png'))
        # self.pB_new_menu.setIcon(QIcon(self.dirname + '/UI/images/icon_cover_3colors_new.png'))
        self.pB_new_menu.setIcon(QIcon(self.dirname + '/UI/images/icon_cover_5.png'))
        # self.pB_modif.setIcon(QIcon(self.dirname + '/UI/images/icon_edit.png'))
        # self.pB_save.setIcon(QIcon(self.dirname + '/UI/images/icon_plate_3colors.png'))
        self.pB_calendar.setIcon(QIcon(self.dirname + '/UI/images/icon_calendar.png'))
        cw.load_pic(self.tag_vegan, self.dirname + '/UI/images/tag_vegan_black_LD.png')
        cw.load_pic(self.tag_kids, self.dirname + '/UI/images/tag_kids_black_LD.png')
        cw.load_pic(self.tag_double, self.dirname + '/UI/images/tag_double_black_LD.png')
        cw.load_pic(self.tag_summer, self.dirname + '/UI/images/tag_ete_black_LD.png')
        cw.load_pic(self.tag_winter, self.dirname + '/UI/images/tag_hiver_black_LD.png')
        cw.load_pic(self.tag_dessert, self.dirname + '/UI/images/tag_dessert_black_LD.png')
        cw.load_pic(self.tag_tips, self.dirname + '/UI/images/tag_tips_black_LD.png')
        cw.load_pic(self.tag_lunchdinner, self.dirname + '/UI/images/tag_lunch_black_LD.png')
        self.pB_back.setIcon(QIcon(self.dirname + '/UI/images/icon_back.png'))
        self.pB_print_2.setIcon(QIcon(self.dirname + '/UI/images/icon_print.png'))
        self.pB_send_2.setIcon(QIcon(self.dirname + '/UI/images/icon_send.png'))

        cw.load_pic(self.label_lunch, self.dirname + '/UI/images/tag_lunch_color_LD.png')
        cw.load_pic(self.label_dinner, self.dirname + '/UI/images/tag_dinner_color_LD.png')
        cw.load_pic(self.score_vegan, self.dirname + '/UI/images/score_vegan_0.png')
        cw.load_pic(self.score_kids, self.dirname + '/UI/images/score_kids_0.png')
        cw.load_pic(self.score_double, self.dirname + '/UI/images/score_double_0.png')
        cw.load_pic(self.score_summer, self.dirname + '/UI/images/score_ete_0.png')
        cw.load_pic(self.score_winter, self.dirname + '/UI/images/score_hiver_0.png')
        
        cw.load_pic(self.label_top, self.dirname + '/UI/images/icon_list.png')
        cw.load_pic(self.label_icon_carte, self.dirname + '/UI/images/icon_menu_3colors_LD.png')
        cw.load_pic(self.label_cocktail, self.dirname + '/UI/images/icon_cocktail_3colors_LD.png')
        self.pB_print.setIcon(QIcon(self.dirname + '/UI/images/icon_print.png'))
        self.pB_send.setIcon(QIcon(self.dirname + '/UI/images/icon_send.png'))
        self.pB_copy.setIcon(QIcon(self.dirname + '/UI/images/icon_copy.png'))

        self.pB_modif_2.setIcon(QIcon(self.dirname + '/UI/images/icon_edit.png'))
        self.pB_new_recipe.setIcon(QIcon(self.dirname + '/UI/images/icon_new_recipe.png'))
        self.pB_delete.setIcon(QIcon(self.dirname + '/UI/images/icon_bin.png'))
        
    def main(self):
        self.pW.show()

    def connect_actions(self):
        self.pB_new_menu.clicked.connect(self.on_new_menu)
        self.tW_menu.cellDoubleClicked.connect(self.on_card_recipe_selection)
        # self.pB_save.clicked.connect(self.on_save_menu)
        # self.pB_calendar.clicked.connect(self.on_calendar)
        self.pB_calendar.clicked.connect(self.on_export_menu)
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
        self.pB_user.clicked.connect(self.on_user_settings)
        
    def update_modif(self):
        self.tW_menu.cellChanged.connect(self.on_drag_drop_event)
        self.time_edition.on_start_date_changed.connect(self.on_date_changed)
        self.time_edition.on_nb_days_changed.connect(self.on_nb_days_changed)
        # self.time_edition.on_dates_changed.connect(self.on_nb_days_changed)
        self.cB_calendar.stateChanged.connect(self.on_export_condition)
        self.cB_history.stateChanged.connect(self.on_export_condition)
        self.lW_recipe.itemSelectionChanged.connect(self.on_recipe_selection)
        self.lW_shopping.itemSelectionChanged.connect(self.on_ingredient_selection)
        self.tW.currentChanged.connect(self.on_tab_changed)
        self.lE_with.textChanged.connect(self.dynamic_filter)
        self.cB_search_ingredients.stateChanged.connect(self.dynamic_filter)
        self.cB_search_preparation.stateChanged.connect(self.dynamic_filter)
        self.cB_search_recipe_name.stateChanged.connect(self.dynamic_filter)
        self.cB_search_tag_dessert.stateChanged.connect(self.dynamic_filter)
        self.cB_search_tag_dinner.stateChanged.connect(self.dynamic_filter)
        self.cB_search_tag_lunch.stateChanged.connect(self.dynamic_filter)
        self.cB_search_tag_double.stateChanged.connect(self.dynamic_filter)
        self.cB_search_tag_kids.stateChanged.connect(self.dynamic_filter)
        self.cB_search_tag_summer.stateChanged.connect(self.dynamic_filter)
        self.cB_search_tag_tips.stateChanged.connect(self.dynamic_filter)
        self.cB_search_tag_vegan.stateChanged.connect(self.dynamic_filter)
        self.cB_search_tag_winter.stateChanged.connect(self.dynamic_filter)
        
    def dummy_function(self, item):
        print('dummy function triggered %s' % item)

    # def is_filter_in_recipe_name(self, filter, recipe):
    #     if self.cB_search_recipe_name.isChecked():
    #         return filter in recipe.name.lower()
    #     return False

    # def is_filter_in_ing_list(self,filter,recipe):
    #     if self.cB_search_ingredients.isChecked() and recipe.ingredients_list_qty is not None: 
    #         for ingredient in list(map(str.lower, recipe.ingredients_list_qty)):
    #             if filter in ingredient:
    #                 return True
    #     return False

    # def is_filter_in_preparation(self, filter, recipe):
    #     if self.cB_search_preparation.isChecked() and recipe.preparation is not None:
    #         return filter in recipe.preparation.lower()
    #     return False

    def is_filter_in_tags(self, recipe):
        output = True
        if self.cB_search_tag_double.isChecked():
            if recipe.tags is not None:
                output = output and recipe.isTagged("double")
            else:
                output = False
        if self.cB_search_tag_kids.isChecked():
            if recipe.tags is not None:
                output = output and recipe.isTagged("kids")
            else:
                output = False
        if self.cB_search_tag_dessert.isChecked():
            if recipe.tags is not None:
                output = output and recipe.isTagged("dessert")
            else:
                output = False
        if self.cB_search_tag_dinner.isChecked():
            if recipe.tags is not None:
                output = output and recipe.isTagged("soir")
            else:
                output = False
        if self.cB_search_tag_lunch.isChecked():
            if recipe.tags is not None:
                output = output and recipe.isTagged("midi")
            else:
                output = False
        if self.cB_search_tag_summer.isChecked():
            if recipe.tags is not None:
                output = output and recipe.isTagged("ete")
            else:
                output = False
        if self.cB_search_tag_tips.isChecked():
            if recipe.tags is not None:
                output = output and recipe.isTagged("tips")
            else:
                output = False
        if self.cB_search_tag_vegan.isChecked():
            if recipe.tags is not None:
                output = output and recipe.isTagged("vegan")
            else:
                output = False
        if self.cB_search_tag_winter.isChecked():
            if recipe.tags is not None:
                output = output and recipe.isTagged("hiver")
            else:
                output = False
        return output

    def dynamic_filter(self):
        # with_filters = self.lE_with.text().split(',')
        # recipeCount = 0

        # for recipeIndex in range(self.lW_recipe.count()):
        #     recipeListItem = self.lW_recipe.item(recipeIndex)
        #     recipe = self.recipe_db.get_recipe_object(recipeListItem.text())
        #     show_recipe_flag = True
            
        #     for filter in with_filters:
        #         filter = filter.strip()
        #         isCriteriaMet = self.is_filter_in_recipe_name(filter, recipe)
        #         isCriteriaMet = isCriteriaMet or self.is_filter_in_ing_list(filter, recipe)
        #         isCriteriaMet = isCriteriaMet or self.is_filter_in_preparation(filter, recipe)
                
        #         show_recipe_flag = show_recipe_flag and isCriteriaMet

        #     show_recipe_flag = show_recipe_flag and self.is_filter_in_tags(recipe)

        #     self.lW_recipe.setItemHidden(recipeListItem, not show_recipe_flag)
        #     if show_recipe_flag:
        #         recipeCount += 1
        
        cw.dynamic_filter(self.lE_with.text(), self.lW_recipe, self.recipe_db, tagFunc = self.is_filter_in_tags)

    def print_thread_function(self, data, icon_path = None):
        self.info_dialog.close()
        self.info_dialog = QMessageBox(self)
        self.info_dialog.setWindowTitle('Information')
        self.info_dialog.setWindowModality(Qt.WindowModal)
        self.info_dialog.setTextFormat(Qt.RichText)
        self.info_dialog.setText(data)
        if icon_path is None or not os.path.isfile(icon_path):
            self.info_dialog.setIcon(QMessageBox.Information)
        else:
            self.info_dialog.setIconPixmap(QPixmap(icon_path).scaled(50,50))
        # info_dialog.setDetailedText(text)
        self.info_dialog.exec_()
    
    def populate_lW_recipe(self):
        for recipeIndex in range(self.lW_recipe.count()):
            recipeListItem = self.lW_recipe.item(recipeIndex)
            recipeListItem.setSizeHint(QSize(0,27))
            recipe_object = self.recipe_db.get_recipe_object(recipeListItem.text())
            
            line_widget = LineRecipe(recipe_object, recipeIndex)
            line_widget.on_menu_request.connect(self.on_update_line_widget)
            line_widget.on_validate.connect(self.on_update_full_menu)
            self.lW_recipe.setItemWidget(recipeListItem, line_widget)
            
            QCoreApplication.processEvents()
    
    def on_update_line_widget(self, recipeIndex):
        recipeListItem = self.lW_recipe.item(recipeIndex)
        self.lW_recipe.itemWidget(recipeListItem).on_update_rcm(self.current_menu)
    
    def on_new_menu(self):
        # start = time.process_time()
        
        movie = cw.gif_to_button(self.dirname + '/UI/images/icon_cover.gif', self.pB_new_menu)
        
        self.new_menu()
        
        # print('step 1 : %f' % (time.process_time() - start))
        # start = time.process_time()
        
        self.populate_tW_menu(self.current_menu)
        # self.populate_lW_recipe()
        self.populate_shopping_list()
        self.populate_menu_list()
        self.compute_score()
        
        # self.pB_save.setEnabled(True)
        
        movie.stop()
        # QCoreApplication.processEvents()
        # self.pB_new_menu.setIcon(QIcon(self.dirname + '/UI/images/icon_cover_5.png'))
        self.pB_new_menu.setIcon(QIcon(self.dirname + '/UI/images/icon_cover_5.png'))
    
    def new_menu(self):
        # current_QDate = self.dateEdit.date()
        current_QDate = self.time_edition.date_from.date()
        y = current_QDate.year()
        m = current_QDate.month()
        d = current_QDate.day()
        self.current_menu.start_day = date(y, m, d)
        # self.current_menu.number_of_days = self.sB_days.value()
        self.current_menu.number_of_days = self.time_edition.slider.value()

        # self.current_menu.generate_random_menu(self.recipe_db)
        options = []
        if self.cB_restes.isChecked():
            options = ['leftovers']
        self.current_menu.generate_smart_menu_v2(self.recipe_db, options = options)
        self.current_menu.use_double()

        # print(self.current_menu)

    def populate_tW_menu(self, menu):
        # movie = cw.gif_to_button(self.dirname + '/UI/images/icon_cover.gif', self.pB_new_menu)
        
        #reset tW_Menu
        self.tW_menu.setColumnCount(0)
        #update tW_menu with days
        self.tW_menu.setColumnCount(self.time_edition.slider.value())
        
        table_menu = menu.full_menu()
        self.tW_menu.setHorizontalHeaderLabels([m[0] for m in table_menu])
        
        self.stacks = {}
        
        #update tW_menu with menus
        recipe_list_lunch = [m[1] for m in table_menu]
        recipe_list_dinner = [m[2] for m in table_menu]
        
        recipe_list = zip(recipe_list_lunch, recipe_list_dinner)
        length = len(recipe_list_lunch)
        for i, recipes_of_day in enumerate(recipe_list):
            recipe_lunch, recipe_dinner = recipes_of_day
            
            idplus = '0' + str(i+1)
            idplus = idplus[-2:]
            idminus = '-' + idplus
            idplus = '+' + idplus
            
            if type(recipe_lunch) == Recipe:
                recipe_lunch_stack = [recipe_lunch]
            elif type(recipe_lunch) == list:
                recipe_lunch_stack = recipe_lunch
            if type(recipe_dinner) == Recipe:
                recipe_dinner_stack = [recipe_dinner]
            elif type(recipe_dinner) == list:
                recipe_dinner_stack = recipe_dinner
            
            #separate lunch and dinner processes:
            #--lunch
            self.on_new_stack(recipe_lunch_stack, idplus, i, length)
            #--dinner
            self.on_new_stack(recipe_dinner_stack, idminus, i, length)
        
        QCoreApplication.processEvents()
        # self.pB_new_menu.setIcon(QIcon(self.dirname + '/UI/images/icon_cover_5.png'))

    def on_new_stack(self, recipe_stack, id, k, length):
        qtwi = QTableWidgetItem(sr.row_column_to_id(0,k))
        stack = StackedRecipes(recipe_stack, self.recipe_db, id)
        stack.on_enter_recipe_stack.connect(self.on_enter_recipe_stack)
        stack.on_lock_for_edition.connect(self.on_lock_for_edition)
        stack.on_update_current_menu.connect(self.on_update_current_menu)
        self.stacks[id] = stack
        if id[0] == '+':
            self.tW_menu.setItem(0, k, qtwi)
            self.tW_menu.setCellWidget(0, k, stack)
            x = (k * 2) % (length+1)
        elif id[0] == '-':
            self.tW_menu.setItem(1, k, qtwi)
            self.tW_menu.setCellWidget(1, k, stack)
            x = (k * 2 + 1) % (length+1)
        
        QCoreApplication.processEvents()
        
    def on_enter_recipe_stack(self, id):
        if not self.lockedForEdition:#ongoing edition of recipe, locking others
            for key in self.stacks:
                if key != id:
                    # self.stacks[key].frame_buttons.setVisible(False)
                    self.stacks[key].on_enter_exit_stack(False)
            if id in self.stacks:
                # self.stacks[id].frame_buttons.setVisible(True)
                self.stacks[id].on_enter_exit_stack(True)
                self.stacks[id].finish_init()
            
    def on_lock_for_edition(self, id, lock):
        if lock:
            self.lockKeyId = id
            self.lockedForEdition = True
            self.pB_new_menu.setEnabled(False)
            self.frame_top_actions.setEnabled(False)
            self.cB_restes.setEnabled(False)
            # self.pB_save.setEnabled(False)
            self.pB_calendar.setEnabled(False)
        elif (not lock) and id == self.lockKeyId:
            self.lockKeyId = 'xx'
            self.lockedForEdition = False
            self.pB_new_menu.setEnabled(True)
            self.frame_top_actions.setEnabled(True)
            self.cB_restes.setEnabled(True)
            # self.pB_save.setEnabled(True)
            self.pB_calendar.setEnabled(True)
            self.populate_shopping_list()
            self.populate_menu_list()
            self.compute_score()
    
    def on_update_current_menu(self, recipe_list, row, column):
        table_index = row + column*2
        self.current_menu.table[table_index] = recipe_list
        self.populate_shopping_list()
        self.populate_menu_list()
        self.compute_score()
        # print(self.current_menu.table)
    
    def on_update_full_menu(self, table):
        self.current_menu.table = [
            self.recipe_db.get_recipe_object_list(stack)
            for stack in table
        ]
        self.populate_tW_menu(self.current_menu)
        self.populate_shopping_list()
        self.populate_menu_list()
        self.compute_score()
    
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

            #take recipe from original to_cell
            # original_to_cell_recipe = self.current_menu.full_menu()[column][row + 1]
            # text = original_to_cell_recipe.name
            # qtwi = QTableWidgetItem(text)
            # qtwi.setTextAlignment(Qt.AlignCenter)
            #and insert in from_cell (now empty after drop)
            from_row, from_column = self.from_cell
            qtwi_to = QTableWidgetItem(sr.row_column_to_id(row,column))
            self.tW_menu.setItem(from_row, from_column, qtwi_to)
            # self.tW_menu.setItem(from_row, from_column, qtwi)

            # cw.display_image(original_to_cell_recipe, self.dirname, qtwi, icon = True)
            
            #take stack from original to_cell and from_cell
            original_to_cell_stack = self.stacks[sr.row_column_to_id(row, column)]
            original_from_cell_stack = self.stacks[sr.row_column_to_id(from_row, from_column)]
            
            original_to_cell_stack_list = original_to_cell_stack.recipe_list
            original_from_cell_stack_list = original_from_cell_stack.recipe_list
            
            new_stacked_to = StackedRecipes(original_from_cell_stack_list, self.recipe_db, id = sr.row_column_to_id(row, column))
            new_stacked_from = StackedRecipes(original_to_cell_stack_list, self.recipe_db, id = sr.row_column_to_id(from_row, from_column))
            
            new_stacked_to.on_enter_recipe_stack.connect(self.on_enter_recipe_stack)
            new_stacked_to.on_lock_for_edition.connect(self.on_lock_for_edition)
            new_stacked_to.on_update_current_menu.connect(self.on_update_current_menu)
            new_stacked_from.on_enter_recipe_stack.connect(self.on_enter_recipe_stack)
            new_stacked_from.on_lock_for_edition.connect(self.on_lock_for_edition)
            new_stacked_from.on_update_current_menu.connect(self.on_update_current_menu)
            
            self.stacks[sr.row_column_to_id(row, column)] = new_stacked_to
            self.stacks[sr.row_column_to_id(from_row, from_column)] = new_stacked_from
            
            qtwi_to = new_stacked_to
            qtwi_from = new_stacked_from
            self.tW_menu.setCellWidget(from_row, from_column, qtwi_from)
            self.tW_menu.setCellWidget(row, column, qtwi_to)
            
            
            #update menu object
            #take from recipe
            from_recipe = self.current_menu.table[from_row + from_column*2]
            #take to recipe
            to_row, to_column = self.to_cell
            to_recipe = self.current_menu.table[to_row + to_column*2]
            #switch
            self.current_menu.table[to_row + to_column*2] = from_recipe
            self.current_menu.table[from_row + from_column*2] = to_recipe

            # self.tW_menu.item(to_row, to_column).setSelected(True)
            # self.tW_menu.item(from_row, from_column).setSelected(False)
                
            #**Improvement: make sure drop was not forgotten (dropped between 2 cells)
            
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
                
            #reinit qtwi text (for consistency or possible reuse)
            for i in range(self.tW_menu.columnCount()):
                qtwi_lunch, qtwi_dinner = (QTableWidgetItem(sr.row_column_to_id(0,i)), QTableWidgetItem(sr.row_column_to_id(1,i)))
                self.tW_menu.setItem(0, i, qtwi_lunch)
                self.tW_menu.setItem(1, i, qtwi_dinner)

    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent) -> bool:

        # if watched == self.tW_menu.viewport() and event.type() == QDropEvent:
        if event.type() == QEvent.Drop:
            #start special process
            self.just_dropped = True
            self.cell_signal_count += 1
            # print(self.cell_signal_count)
        # elif event.type() == QEvent.HoverEnter:
        #     print('just entered qtablewidget')
        elif event.type() == QEvent.HoverLeave:
            # print('just left qtablewidget')
            self.on_enter_recipe_stack('00')
        # else:
        #     print(type(watched), event.type())
        return super().eventFilter(watched, event)
    
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
 
        # recipe_name = self.tW_menu.item(row, column).text()
        id = self.tW_menu.item(row, column).text()
        stack = self.stacks[id]
        recipe_name = stack.get_current_recipe().name
        self.tW.setCurrentWidget(self.tab_recipe)
        self.reset_recipes_list()
        self.reset_filters()
        lwi = self.lW_recipe.findItems(recipe_name, Qt.MatchExactly)[0]
        self.lW_recipe.scrollToItem(lwi)
        self.lW_recipe.setCurrentItem(lwi)
        lwi.setSelected(True)

    def switch_to_recipe(self, recipe_name):
        self.on_quit_settings()
        self.tW.setCurrentWidget(self.tab_recipe)
        self.reset_recipes_list()
        self.reset_filters()
        try:
            lwi = self.lW_recipe.findItems(recipe_name, Qt.MatchExactly)[0]
            self.lW_recipe.scrollToItem(lwi)
            self.lW_recipe.setCurrentItem(lwi)
            lwi.setSelected(True)
        except:
            self.on_wrong_recipe_name(recipe_name)
    
    def on_tab_changed(self, tab_index):
        if tab_index == 1 and self.lW_recipe.selectedItems() == []: #recipe tab selected
            #select first recipe if nothing previously selected to avoid blank fields
            self.lW_recipe.setCurrentRow(0)
            self.lW_recipe.setItemSelected(self.lW_recipe.item(0), True)
            
    def on_recipe_selection(self): #display recipe when selected in the list
        if self.lW_recipe.count() > 0:
            #display title
            recipe_name = self.lW_recipe.currentItem().text()
            self.label_recipe_title.setText(recipe_name)
            if self.recipe_db.contains(recipe_name):
                recipe_object = self.recipe_db.get_recipe_object(recipe_name)
                #display image
                cw.display_image(recipe_object, self.dirname, self.label_recipe_image, icon = False)
                #display instructions
                self.tE_recipe.setText(recipe_object.preparation.replace('\n', '<br/>'))
                #display ingredients
                self.tE_ingredients.setText(recipe_object.ingredients_string(self.recipe_db).replace('\n', '<br/>'))
                #update tags
                tags = [self.tag_vegan, self.tag_kids, self.tag_double, self.tag_summer, self.tag_winter, self.tag_dessert, self.tag_tips]
                tags_names = ['vegan', 'kids', 'double', 'ete', 'hiver', 'dessert', 'tips']
                for tag, tag_name in zip(tags, tags_names):
                    cw.load_pic(tag, self.dirname + '/UI/images/tag_%s_%s_LD.png' % (tag_name, ['black', 'color'][recipe_object.isTagged(tag_name)]))
                if recipe_object.isTagged('midi'):
                    cw.load_pic(self.tag_lunchdinner, self.dirname + '/UI/images/tag_lunch_color_LD.png')
                elif recipe_object.isTagged('soir'):
                    cw.load_pic(self.tag_lunchdinner, self.dirname + '/UI/images/tag_dinner_color_LD.png')
                else:
                    cw.load_pic(self.tag_lunchdinner, self.dirname + '/UI/images/tag_lunch_black_LD.png')
            else:
                self.on_wrong_recipe_name(recipe_name)
                # self.display_error("La recette '%s' n'est plus dans la base de données, elle a peut-être été modifiée ou supprimée" % recipe_name)
        
    def on_recipe_link(self, link):
        self.reset_recipes_list()
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
    
    def on_date_changed(self, qdate):
        self.current_menu.start_day = datetime.date(qdate.year(), qdate.month(), qdate.day())
        #update headers only
        table_menu = self.current_menu.full_menu()
        self.tW_menu.setHorizontalHeaderLabels([m[0] for m in table_menu])
        
    def on_nb_days_changed(self, number):
        # #add/remove columns to table
        # adding = (number - self.tW_menu.columnCount()) == 1
        # self.tW_menu.setColumnCount(number)
        # self.tW_menu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)        
        # #update existing menu
        self.current_menu.update(self.recipe_db, number)
        # #update tW_menu with menus
        # table_menu = self.current_menu.full_menu()
        # self.tW_menu.setHorizontalHeaderLabels([m[0] for m in table_menu])

        # #update tW_menu with menus
        # recipe_list_lunch = [m[1] for m in table_menu]
        # recipe_list_dinner = [m[2] for m in table_menu]
        # for i, recipes_of_day in enumerate(zip(recipe_list_lunch, recipe_list_dinner)):
        #     recipe_lunch, recipe_dinner = recipes_of_day
        #     text_lunch, text_dinner = (recipe_lunch.name, recipe_dinner.name)
        #     # print((text_lunch, self.recipe_db.background_score(recipe_lunch, self.current_menu.start_day)))
        #     qtwi_lunch, qtwi_dinner = (QTableWidgetItem(text_lunch), QTableWidgetItem(text_dinner))
        #     qtwi_lunch.setTextAlignment(Qt.AlignCenter)
        #     qtwi_dinner.setTextAlignment(Qt.AlignCenter)

        #     self.tW_menu.setItem(0, i, qtwi_lunch)
        #     self.tW_menu.setItem(1, i, qtwi_dinner)

        #     cw.display_image(recipe_lunch, self.dirname, qtwi_lunch, icon = True)
        #     cw.display_image(recipe_dinner, self.dirname, qtwi_dinner, icon = True)
        self.populate_tW_menu(self.current_menu)
        #update shopping list and menu list
        self.populate_shopping_list()
        self.populate_menu_list()
        self.compute_score()
    
    def on_export_menu(self):
        if self.cB_calendar.isChecked():
            self.on_calendar()
        if self.cB_history.isChecked():
            self.on_save_menu()
    
    def on_export_condition(self):
        self.pB_calendar.setEnabled(True)
        if self.cB_calendar.isChecked():
            tooltip = "Copier dans l'Agenda"
            if self.cB_history.isChecked():
                tooltip += " + Sauvegarder l'Historique"
        elif self.cB_history.isChecked():
            tooltip = "Sauvegarder l'Historique"
        else:
            tooltip = "Sélectionner au moins une option !"
            self.pB_calendar.setEnabled(False)
        self.pB_calendar.setToolTip(tooltip)

    def on_save_menu(self):
        new_history = []
        
        for i in range(self.current_menu.number_of_days):
            date = self.current_menu.start_day + timedelta(days = i)
            # lunch_recipe_name = self.tW_menu.item(0, i).text()
            # dinner_recipe_name = self.tW_menu.item(1, i).text()
            
            lunch_id = self.tW_menu.item(0, i).text()
            dinner_id = self.tW_menu.item(1, i).text()
            lunch_recipe_name = ' | '.join(recipe_db.get_recipe_names(self.stacks[lunch_id].recipe_list))
            dinner_recipe_name = ' | '.join(recipe_db.get_recipe_names(self.stacks[dinner_id].recipe_list))
            
            
            date_text = recipe_db.date_to_text(date)
            #build new history list
            new_history.append([date_text, lunch_recipe_name, dinner_recipe_name])

        self.new_history = self.recipe_db.consider_history_update(new_history)

        self.history_popup.on_save_menu(self.new_history)
        self.on_display_history(self.new_history)
    
    def on_confirm_history_update(self):
        #backup file
        copy2(self.recipe_db.history_file, self.dirname + '/backup/history_backup.csv')
        #update recipe_db variables and file
        self.recipe_db.update_history(self.new_history)
        self.history_popup.history = self.recipe_db.history

    def on_calendar(self):
        self.movie = cw.gif_to_button(self.dirname + '/UI/images/icon_calendar.gif', self.pB_calendar)
        
        # my_calendar_worker = cal.MyCalendar(self.current_menu)
        my_calendar_worker = gapi.MyCalendar(self.current_menu)
        
        # my_calendar_worker.signal.sig.connect(self.print_thread_function)
        my_calendar_worker.on_message.connect(self.print_thread_function)
        my_calendar_worker.on_finish.connect(self.on_calendar_gif_stop)
        self.myThreads.append(my_calendar_worker)
        my_calendar_worker.start()
    
    def on_calendar_gif_stop(self):
        self.movie.stop()
        self.pB_calendar.setIcon(QIcon(self.dirname + '/UI/images/icon_calendar.png'))
        
    def on_ingredient_selection(self):
        #reset list menu background
        for item in [self.lW_menu.item(i) for i in range(self.lW_menu.count())]:
            # r,g,b = self.colors['#color3_bright#'][1]
            # item.setBackground(QBrush(QColor(r,g,b)))
            item.setBackground(QBrush(QColor(self.colors['#color3_bright#'])))
            # item.setTextColor(QColor(0, 0, 0))
            item.setTextColor(QColor(self.colors['#color1_dark#']))
        
        #get ingredient text
        if len(self.lW_shopping.selectedItems()) > 0:
            text = self.lW_shopping.selectedItems()[0].text()
            ingredient = text.split(' : ')[0][2:]
            for item in [self.lW_menu.item(i) for i in range(self.lW_menu.count())]:

                if self.recipe_db.get_recipe_object(item.text()[5:]).hasIngredient(ingredient):
                    # r,g,b = self.colors['#color3#'][1]
                    # item.setBackground(QBrush(QColor(r,g,b)))
                    item.setBackground(QBrush(QColor(self.colors['#color3#'])))
                    # r,g,b = self.colors['#color4#'][1]
                    # item.setTextColor(QColor(r,g,b))
                    item.setTextColor(QColor(self.colors['#color1_dark#']))
                else:
                    # r,g,b = self.colors['#color4_bright#'][1]
                    # item.setBackground(QBrush(QColor(r,g,b)))
                    item.setBackground(QBrush(QColor(self.colors['#color3_bright#'])))
                    item.setTextColor(QColor(self.colors['#color1_dark#']))
    
    def on_copy_shopping_list(self):
        string_to_copy = 'Liste de courses:\n'
        for item in [self.lW_shopping.item(i) for i in range(self.lW_shopping.count())]:
            string_to_copy += item.text() + '\n'
        # print(string_to_copy)
        copy(string_to_copy)

    def on_send_shopping_list(self):        
        if os.path.isfile(self.user_id_file):
            with open(self.user_id_file, 'r') as f:
                self.default_email = f.readline().strip().split(';')[0]
            # print(self.default_email)
        else:
            text, ok = QInputDialog.getText(self, 'Enregistrement de votre adresse email', 'Votre adresse email:')
		
            if ok:
                self.default_email = text

                with open(self.user_id_file, 'w') as f:
                    f.write(';'.join([self.default_email, 
                                    str(self.default_nb_days), 
                                    self.default_storage,
                                    self.homepage.toString()]))

        images = [self.dirname + '/UI/images/icon_menu_3colors_LD.png']
        images.append(self.dirname + '/UI/images/icon_shopping_cart_LD.png')
        images.append(self.dirname + '/UI/images/icon_user_color.png')
        icon_dict = {'[ICON_MENU_PATH]': 'cid:%s' % (basename(images[0]))}
        icon_dict['[ICON_SHOPPING_PATH]'] = 'cid:%s' % (basename(images[1]))
        icon_dict['[ICON_TABLE_PATH]'] = 'cid:%s' % (basename(images[2]))

        # my_mailbox_worker = mail.Mailbox('shopping', [self.current_menu, self.default_email, images, icon_dict])
        my_mailbox_worker = gapi.MyMailbox('shopping', [self.current_menu, self.default_email, images, icon_dict])
        
        my_mailbox_worker.signal.sig.connect(self.print_thread_function)
        
        self.myThreads.append(my_mailbox_worker)
        my_mailbox_worker.start()

    def on_print_shopping_list(self):
        os.makedirs(self.default_storage + '/Menus/', exist_ok=True)
        pdf_title = self.default_storage + '/Menus/Menus(%s-%s).pdf' % (self.current_menu.start_day.strftime('%d_%m_%Y'), 
                                                                            self.current_menu.to_day().strftime('%d_%m_%Y'))
        images = [self.dirname + '/UI/images/icon_menu_3colors_LD.png']
        images.append(self.dirname + '/UI/images/icon_shopping_cart_LD.png')
        images.append(self.dirname + '/UI/images/icon_user_color.png')
        my_printer = printer.Printer(pdf_title)
        # my_printer = printer.Printer('test.pdf')
        my_printer.print_shopping_list(self.current_menu, icons=images, images=self.compute_score(draw=False))
        
        self.print_thread_function('Les menus du %s au %s ont été enregistrés<br/><a href="%s">%s</a>' % (self.current_menu.start_day.strftime('%d/%m/%Y'),
                                                                                        self.current_menu.to_day().strftime('%d/%m/%Y'), 
                                                                                        pdf_title, pdf_title),
                                   icon_path = self.dirname + '/UI/images/icon_print.png')
    
    def on_send_recipe(self):
        user_id_file = self.dirname + '/user.id'
        if os.path.isfile(user_id_file):
            with open(user_id_file, 'r') as f:
                self.default_email = f.readline().strip().split(';')[0]
            # print(self.default_email)
        else:
            text, ok = QInputDialog.getText(self, 'Enregistrement de votre adresse email', 'Votre adresse email:')
		
            if ok:
                self.default_email = text

                with open(self.user_id_file, 'w') as f:
                    f.write(';'.join([self.default_email, 
                                    str(self.default_nb_days), 
                                    self.default_storage,
                                    self.homepage.toString()]))

        recipe_name = self.lW_recipe.currentItem().text()
        recipe_object = self.recipe_db.get_recipe_object(recipe_name)

        images = [self.dirname + '/UI/images/icon_recipe_3colors_LD_t.png']
        images.append(self.dirname + '/UI/images/icon_user_color.png')
        icon_dict = {'[ICON_RECIPE_PATH]': 'cid:%s' % (basename(images[0]))}
        icon_dict['[ICON_TABLE_PATH]'] = 'cid:%s' % (basename(images[1]))

        recipe_pdf = self.on_print_recipe(silent=True)
        
        if os.path.isfile(recipe_pdf):
            # my_mailbox_worker = mail.Mailbox('recipe', [recipe_object, self.default_email, images, icon_dict, recipe_pdf])
            my_mailbox_worker = gapi.MyMailbox('recipe', [recipe_object, self.default_email, images, icon_dict, recipe_pdf])
            
            my_mailbox_worker.signal.sig.connect(self.print_thread_function)
            
            self.myThreads.append(my_mailbox_worker)
            my_mailbox_worker.start()
        else:
            print('error while creating pdf')

    def on_print_recipe(self, silent = False):
        recipe_name = self.lW_recipe.currentItem().text()
        os.makedirs(self.default_storage + '/Recettes/', exist_ok=True)
        pdf_title = self.default_storage + '/Recettes/%s.pdf' % recipe_name
        recipe_object = self.recipe_db.get_recipe_object(recipe_name)

        tags_names = ['vegan', 'kids', 'double', 'ete', 'hiver', 'dessert']
        images = [self.dirname + '/UI/images/tag_%s_%s_LD.png' % (tag, ['black', 'color'][recipe_object.isTagged(tag)]) for tag in tags_names]

        my_printer = printer.Printer(pdf_title)
        my_printer.print_recipe(recipe_object, images)

        if not silent:
            # self.print_thread_function('La recette "%s" a été enregistrée<br/><a href="%s">%s</a>' % 
            #                            (recipe_name, pdf_title, pdf_title),
            #                         icon_path = self.dirname + '/UI/images/icon_print.png')
            self.print_thread_function('La recette "%s" a été enregistrée<br/>%s' % 
                                       (recipe_name, pdf_title),
                                    icon_path = self.dirname + '/UI/images/icon_print.png')

        return pdf_title

    def compute_score(self, draw = True):
        tags = [self.score_double, self.score_kids, self.score_vegan, self.score_summer, self.score_winter]
        tags_names = ['double', 'kids', 'vegan', 'ete', 'hiver']
        score = dict(zip(tags_names, [self.current_menu.tag_score(tag_name) for tag_name in tags_names]))
        
        if draw:
            for tag, tag_name in zip(tags, tags_names):
                cw.load_pic(tag, self.dirname + '/UI/images/score_%s_%s.png' % (tag_name, score[tag_name]))

        return [self.dirname + '/UI/images/score_%s_%s.png' % (tag_name, score[tag_name]) for tag, tag_name in zip(tags, tags_names)]
    
    def reset_recipes_list(self): #reset list of recipes
        self.lW_recipe.clear()     #reset list
        recipe_list = sorted(recipe_db.get_recipe_names(self.recipe_db.recipe_list), key=str.lower)
        self.lW_recipe.addItems(recipe_list)         #repopulate recipe list
        self.populate_lW_recipe()

    def reset_filters(self): #reset search/filter section(frame)
        self.cB_search.setText('Recherche avancée')   
        self.lE_with.setText('')
        self.cB_search_recipe_name.setChecked(True)
        self.cB_search_ingredients.setChecked(True)
        self.cB_search_preparation.setChecked(True)
        self.cB_search_tag_lunch.setChecked(False)
        self.cB_search_tag_dinner.setChecked(False)
        self.cB_search_tag_dessert.setChecked(False)
        self.cB_search_tag_double.setChecked(False)
        self.cB_search_tag_kids.setChecked(False)
        self.cB_search_tag_summer.setChecked(False)
        self.cB_search_tag_tips.setChecked(False)
        self.cB_search_tag_vegan.setChecked(False)
        self.cB_search_tag_winter.setChecked(False)
        if self.frame_search.isVisible():
            self.cB_search.click()

    def init_edit_recipe(self):
        self.edit_recipe = EditRecipe(self.user_settings, self.recipe_db)
        self.edit_recipe.on_ok.connect(self.on_confirm_recipe)
        self.edit_recipe.on_cancel.connect(self.on_cancel_recipe)
        self.edit_recipe.on_error.connect(self.display_error)
        self.edit_recipe.on_message.connect(self.print_thread_function)
        self.vL_edit_recipe.addWidget(self.edit_recipe)

    def disable_other_tabs(self):
        self.tW.setTabEnabled(0, False)
        self.tW.setTabEnabled(2, False)
        self.cB_search.setEnabled(False)
        self.pB_new_recipe.setEnabled(False)
        self.pB_modif_2.setEnabled(False)

    def on_new_recipe(self):
        self.disable_other_tabs()
        self.edit_recipe.new_mode()
         
    def on_edit_recipe(self):
        self.disable_other_tabs()
        recipe = self.recipe_db.get_recipe_object(self.lW_recipe.currentItem().text())
        self.edit_recipe.edit_mode(recipe)
        
    def on_confirm_recipe(self, input):
        title, image_cell, ing_dict, preparation_cell, time, tag_checked_list, mode, auto_switch = input
        
        if auto_switch != 'edit':
            image = ''
            if self.recipe_db.contains(title):
                image = self.recipe_db.get_recipe_object(title).image
            if image_cell != '':
                image = '/images/' + image_cell
            

            #add recipe to database
            recipe = Recipe(uuid.uuid4(), title, ing_dict, preparation_cell, time, tag_checked_list, image)
            if self.edit_recipe.label_newedit.text() == 'Modifier la recette':  #update existing recipe
                initial_recipe_name = self.lW_recipe.currentItem().text()
                index_of_recipe = recipe_db.get_recipe_names(self.recipe_db.recipe_list).index(initial_recipe_name)
                self.recipe_db.recipe_list[index_of_recipe] = recipe
            else:   #add new recipe
                self.recipe_db.recipe_list.append(recipe)
                
            #update qlw
            self.update_recipe_list()
            # self.lW_recipe.clear()
            # recipe_list = sorted(recipe_db.get_recipe_names(self.recipe_db.recipe_list), key=str.lower)
            # self.lW_recipe.addItems(recipe_list)
            
            #backup file
            copy2(self.recipe_db.recipe_file, self.dirname + '/backup/recipe_backup.csv')
            #update recipe sheet (fully rewrite)
            self.recipe_db.update_recipe_file()
            
        #reenable other tabs
        self.reenable_other_tabs()
        
        #auto select the newly created/modified recipe
        #select existing recipe in list
        lwi = self.lW_recipe.findItems(title, Qt.MatchExactly)[0]
        self.lW_recipe.scrollToItem(lwi)
        self.lW_recipe.setCurrentItem(lwi)
        lwi.setSelected(True)
        
        #auto-switch feature
        if auto_switch == 'edit':
            self.pB_modif_2.click()

        # self.clear_edit_recipe_window()

    def reenable_other_tabs(self):
        self.tW.setTabEnabled(0, True)
        self.tW.setTabEnabled(2, True)
        self.cB_search.setEnabled(True)
        self.pB_new_recipe.setEnabled(True)
        self.pB_modif_2.setEnabled(True)
        self.pB_delete.setEnabled(True)
        self.pB_new_recipe.setChecked(False)
        self.pB_modif_2.setChecked(False)
        self.edit_recipe.cB_web.setChecked(False)

    def on_delete_recipe(self):
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
                # print('removing %s' % recipe_name)
                #update recipe_dbs
                self.recipe_db.remove_recipe(recipe_name)
                #update qlw
                self.delete_flag = True #to avoid error message displayed twice
                self.update_recipe_list()
                self.delete_flag = False
                lwi = self.lW_recipe.item(0)
                self.lW_recipe.scrollToItem(lwi)
                self.lW_recipe.setCurrentItem(lwi)
                lwi.setSelected(True)
        #backup file
        copy2(self.recipe_db.recipe_file, self.dirname + '/backup/recipe_backup.ods')
        #update recipe sheet (fully rewrite)
        self.recipe_db.update_recipe_file()
        #info message recipe correctly removed
        # print(recipe_name)
    
    def on_cancel_recipe(self):
        self.reenable_other_tabs()
    
    def update_recipe_list(self):
        self.lW_recipe.clear()
        recipe_list = sorted(recipe_db.get_recipe_names(self.recipe_db.recipe_list), key=str.lower)
        self.lW_recipe.addItems(recipe_list)
    
    def display_error(self, text, title = 'Attention'):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle(title)
        error_dialog.setWindowModality(Qt.WindowModal)
        error_dialog.setText(text)
        error_dialog.setIcon(QMessageBox.Warning)
        # error_dialog.setDetailedText(text)
        answer = error_dialog.exec_()
    
    def on_wrong_recipe_name(self, recipe_name):
        if self.lW_recipe.count() == 0:
            self.display_error('La base de données est vide ! Aucune recette à afficher')
        else:
            if not self.delete_flag:
                self.display_error("La recette '%s' n'est plus dans la base de données, elle a peut-être été modifiée ou supprimée" % recipe_name)
                lwi = self.lW_recipe.item(0)
                self.lW_recipe.scrollToItem(lwi)
                self.lW_recipe.setCurrentItem(lwi)
                lwi.setSelected(True)
            else:
                self.display_error("La recette '%s' a bien été supprimée" % recipe_name)
    
    def init_user_settings(self):
        if os.path.isfile(self.user_id_file):
            with open(self.user_id_file, 'r') as f:
                #for legacy compatibility
                data = f.readline().strip().split(';')
                if len(data) == 1:
                    self.default_email = data[0]
                elif len(data) == 3:
                    self.default_email, nb_days, self.default_storage = data
                    self.default_nb_days = int(nb_days)
                elif len(data) == 4:
                    self.default_email, nb_days, self.default_storage, homepage = data
                    self.default_nb_days = int(nb_days)
                    self.homepage = QUrl(homepage)
        
        
        self.user_settings = UserSettings()
        self.user_settings.on_save.connect(self.on_save_settings)
        self.user_settings.on_quit.connect(self.on_quit_settings)
        self.user_settings.on_error.connect(self.display_error)
        self.user_settings.on_history.connect(self.on_display_history)
        self.vL_settings.addWidget(self.user_settings)
        
        # qmlview = QtQuickWidgets.QQuickWidget(source= QUrl(self.dirname + '/UI/MyElement.qml'))
        # self.vL_settings.addWidget(qmlview)
        
        self.history_popup = History(history = self.recipe_db.history, new_history = [])
        self.history_popup.on_switch_to_recipe.connect(self.switch_to_recipe)
        self.history_popup.on_confirm.connect(self.on_confirm_history_update)
        
    def on_user_settings(self):
        self.frame_settings.show()
        self.frame.hide()
        #test if values are different than user file and highlight accordingly
        self.user_settings.highlight_diff()
        
    def on_save_settings(self, input):
        email, nb_days, storage, homepage = input
        self.default_email = email
        self.default_nb_days = int(nb_days)
        self.default_storage = storage
        self.homepage = QUrl(homepage)
        
        self.frame_settings.hide()
        self.frame.show()
        
    def on_quit_settings(self):
        self.frame_settings.hide()
        self.frame.show()
    
    def on_display_history(self, new_history = []):
        self.history_popup.selectWidgetMode(new_history)
        self.history_popup.show()
        
    def on_add_recipe_right_click(self, id):
        recipe_name = self.lW_recipe.currentItem().text()
        recipe = self.recipe_db.get_recipe_object(recipe_name)
        stack = self.stacks[id]
        stack.on_add_random_recipe(recipe = recipe)
        
        #highlight success and keep current tab
        # self.tW.setCurrentWidget(self.tab_menus)
        self.print_thread_function('Recette "%s" ajoutée aux Menus !' % recipe_name,
                                   icon_path = self.dirname + '/UI/images/icon_choice_recipe.png')
    
    def openDir(self, field, titre, dirpath = ''):
        if dirpath == '':
            dirpath = self.dirname
        path = QFileDialog.getExistingDirectory(self, u"Choix de l'emplacement " + titre, directory = dirpath)
        field.setText(str(path).replace('\\', '/'))
        
    def user_settings_pB(self):
        self.pB_user = QPushButton('', self.pW)
        self.pB_user.setIconSize(QSize(60,60))
        self.pB_user.setToolTip('Préférences')
        self.pB_user.setStyleSheet('''
                                QPushButton{
                                    image: url(file:///../UI/images/icon_user.png);
                                    background-color: %s;
                                    border-width: 0px;
                                    border-radius: 0px;
                                    border-color: %s;
                                }

                                QPushButton:hover{
                                    image: url(file:///../UI/images/icon_user_color.png);
                                }

                                QPushButton:pressed{
                                    image: url(file:///../UI/images/icon_user_color_.png);
                                }
                                   ''' % (self.colors['#color5#'], self.colors['#color5#']))
        self.tW.setCornerWidget(self.pB_user)

def image_from_base64(base64_table, image_name):#Legacy function to store and read images -- can be removed
    with open(base64_table, 'r') as f:
        data = f.readlines()
    for line in data:
        if image_name == line.split(':')[0]:
            base64 = line.split('ICON_MENU_PATH:<img src="')[1].strip()[:-3]
            return base64

def extract_number(string):#Extract number from ingredient quantity string
    number = []
    no_decimal = True
    for c in string:
        # print(c)
        if c.isdigit() or (c == '.' and no_decimal):
            number.append(c)
            if c == '.':
                no_decimal = False
        # else:
        #     return ''.join(number)
    try:
        float_num = float(''.join(number))
        if str(float_num)[-2:] == '.0':
            return str(int(float_num))
        else:
            return str(float_num)
    except:
        return ''.join(number)

def start(recipe_db):
    app = QApplication(sys.argv)

    #current working directory
    # dirname = os.path.dirname(__file__)
    dirname = os.path.dirname(os.path.abspath(__file__))
    #declare and read GUI file
    myUiFile = dirname + '/UI/Main_Window.ui'

    splash_pic = QPixmap(dirname + '/UI/images/splash_cooking.gif')
    splash = QSplashScreen(splash_pic)
    
    movie = QMovie()
    movie.setFileName(dirname + '/UI/images/splash_cooking.gif')
    movie.frameChanged.connect(lambda: splash.setPixmap(movie.currentPixmap()))
    movie.start()
    splash.show()
    app.processEvents()
    splash.showMessage('Veuillez patienter pendant la préparation de votre table...', 
                        Qt.AlignHCenter | Qt.AlignBottom, 
                        QColor(COLORS['#color1_dark#']))
    
    w = QUiLoader().load(myUiFile)
    #Create and display GUI object
    myGUI = MainGUI(parent = w, recipe_db = recipe_db)
    myGUI.main()
    
    splash.finish(myGUI.window())

    sys.exit(app.exec_())

def debug(input = None):
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
    # s = '250 l'
    # qty = extract_number(s)
    # print(qty)
    # import re

    # myString = "This is my tweet check it out https://example.com/blah"

    # print(re.search("(?P<url>https?://[^\s]+)", myString).group("url"))
    try:
        print('hello %i' % input )
    except:
        debug(1)

def main(): #Entry point

    # dirname = os.path.dirname(__file__)
    dirname = os.path.dirname(os.path.abspath(__file__))
    # input_recipe = dirname + '/MesRecettes (copy).ods'
    input_recipe = dirname + '/MesRecettes.csv'
    input_history = dirname + '/Historique.csv'
    
    #Create Recipe_db object reading input files
    my_recipe_DB = recipe_db.RecipeDB(recipe_file= input_recipe, history_file= input_history)
    #Launch app
    start(my_recipe_DB)



if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    main()
    # debug()

    
















        #def on_filter_selection(self): #DEPRECATED - first recipe search algorithm relying on a button. 
    #    if self.pB_filter.isChecked():
    #        #extract filter values
    #        with_list = self.lE_with.text().split(',')
    #        #without_list = self.lE_without.text().split(',')
    #        filtered_list = []
    #        total_recipe_count = self.lW_recipe.count()
    #        for recipe_object in [self.recipe_db.get_recipe_object(self.lW_recipe.item(i).text()) for i in range(total_recipe_count)]:
    #            #with
    #            is_selected = True
    #            for with_text in with_list: #must meet all the with criteria
    #                is_selected *= recipe_object.meet_with_criteria(with_text)
    #            #without
    #            for without_text in without_list: #must meet all the without criteria
    #                is_selected *= recipe_object.meet_without_criteria(without_text)
    #            if is_selected:
    #                filtered_list.append(recipe_object)
    #
    #        #reset list
    #        self.lW_recipe.clear()
    #        self.lW_recipe.addItems(recipe_db.get_recipe_names(filtered_list))
    #        if filtered_list != []:
    #            self.lW_recipe.setCurrentRow(0)
    #
    #        #display result summary on search label
    #        self.cB_search.setText('Recherche (%s/%s)' % (len(filtered_list), total_recipe_count))
    #    else:
    #        self.reset_recipes_list()
    #        self.cB_search.setText('Recherche')
