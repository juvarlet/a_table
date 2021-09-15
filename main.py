from re import split
from uid_widget import UIDWidget
from ingredient import Ingredient
import string
from ingredient_item import IngredientItem
import os
from os.path import basename

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
from datetime import date, timedelta
from pyperclip import copy
from shutil import copy2
import pyautogui
import uuid

import PySide2
from PySide2.QtWidgets import*
# QApplication, QWidget, QPushButton, QTableWidget, QSpinBox
from PySide2.QtGui import QBrush, QDoubleValidator, QPainterPath, QPixmap, QIcon, QColor, QPainter, QFontDatabase, QFont
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import*
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
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
        self.dateEdit.setFont(QFont('Aller', 11, QtGui.QFont.Bold))
        self.cB_restes.setFont(QFont('Aller', 14, QtGui.QFont.Bold))
        
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
        self.default_nb_days = 7
        self.default_storage = self.dirname + '/Mes_Fiches/'
        self.homepage = QUrl("https://www.google.com/")
        self.user_id_file = self.dirname + '/user.id'
        self.init_user_settings()
        
        self.recipe_image_path = ''
        self.myThreads = []
        self.delete_flag = False
        self.contact = 'notification.a.table@gmail.com'
        self.stacks = {}
        self.lockKeyId = 'xx'
        self.lockedForEdition = False
        self.recipeMultiSelection = []
        
        #-- ui widgets --
        self.tW: QTabWidget
        self.tW = self.pW.tabWidget
        self.frame: QFrame
        self.frame = self.pW.frame
        self.frame_settings: QFrame
        self.frame_settings = self.pW.frame_settings
        self.label_user: QLabel
        self.label_user = self.pW.label_user
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
        self.sB_days = self.pW.sB_days
        self.p_carte: QWidget
        self.p_carte = self.pW.page_carte
        self.pB_save: QPushButton
        self.pB_save = self.pW.pB_save
        self.pB_calendar: QPushButton
        self.pB_calendar = self.pW.pB_calendar
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
        self.frame_new_recipe: QFrame
        self.frame_new_recipe = self.pW.frame_new_recipe
        self.frame_edit_recipe: QFrame
        self.frame_edit_recipe = self.pW.frame_edit_recipe
        self.lE_title: QLineEdit
        self.lE_title = self.pW.lE_titre
        self.img_dish: QLabel
        self.img_dish = self.pW.img_dish


        #self.tW_ingredients: QTableWidget
        #self.tW_ingredients = self.pW.tW_ingredients

        self.lw_ingredients:QListWidget
        self.lw_ingredients = self.pW.lw_ingredients


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
        self.gL_web: QGridLayout
        self.gL_web = self.pW.gL_web
        self.hL_tools: QHBoxLayout
        self.hL_tools = self.pW.hL_tools
        self.frame_wB: QFrame
        self.frame_wB = self.pW.frame_wB
        self.cB_web: QCheckBox
        self.cB_web = self.pW.cB_web
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
        #tab settings
        self.pB_ok_3: QPushButton
        self.pB_ok_3 = self.pW.pB_ok_3
        self.pB_cancel_3: QPushButton
        self.pB_cancel_3 = self.pW.pB_cancel_3
        self.lE_email: QLineEdit
        self.lE_email = self.pW.lE_email
        self.sB_settings_days: QSpinBox
        self.sB_settings_days = self.pW.sB_settings_days
        self.lE_storage: QLineEdit
        self.lE_storage = self.pW.lE_storage
        self.tB_storage: QToolBox
        self.tB_storage = self.pW.toolButton
        self.lE_homepage: QLineEdit
        self.lE_homepage = self.pW.lE_homepage
        self.label_contact: QLabel
        self.label_contact = self.pW.label_contact
        self.img_settings_email: QLabel
        self.img_settings_email = self.pW.img_settings_email
        self.img_settings_days: QLabel
        self.img_settings_days = self.pW.img_settings_days
        self.img_settings_storage: QLabel
        self.img_settings_storage = self.pW.img_settings_storage
	self.label_homepage: QLabel
        self.label_homepage = self.pW.label_homepage

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
        
        self.colors = {
                    '#color1_bright#'   : '#36a9d3',
                    '#color1#'          : '#2584a7',
                    '#color1_dark#'     : '#1a5d75',
                    '#color2_bright#'   : '#fe9a9d',
                    '#color2#'          : '#fe6d73',
                    '#color2_dark#'     : '#fe484e',
                    '#color3_bright#'   : '#ffe0ad',
                    '#color3#'          : '#ffcb77',
                    '#color3_dark#'     : '#ffc05c',
                    '#color4_bright#'   : '#24e5d2',
                    '#color4#'          : '#17c3b2',
                    '#color4_dark#'     : '#13a496',
                    '#color5_bright#'   : '#fef9ef',
                    '#color5#'          : '#fdf1d9',
                    '#color5_dark#'     : '#fae2b2'
                    }
        
        # cw.style_factory(self.pW, init_colors = self.init_colors, colors = self.colors)
        
        #default state
        self.window().setWindowState(Qt.WindowMaximized)
        #-replace qtablewidget tW_menu by custom class
        new_tW_menu = cw.TableWidgetCustom(self.pW)
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
        new_tW_menu.setLineWidth(0)
        new_tW_menu.setShowGrid(False)
        new_tW_menu.setStyleSheet(self.pW.styleSheet())
        self.pW.gridLayout_10.replaceWidget(self.tW_menu, new_tW_menu)
        self.tW_menu = new_tW_menu
        self.pW.tW_menu.setParent(None)
        
        new_sB_days = cw.SpinBoxCustom(self.pW)
        new_sB_days.setMinimumHeight(50)
        new_sB_days.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        new_sB_days.setSuffix(' jours')
        new_sB_days.setValue(self.default_nb_days)
        new_sB_days.setMinimum(1)
        self.pW.gridLayout_13.replaceWidget(self.sB_days, new_sB_days)
        # self.pW.horizontalLayout.insertWidget(5,new_sB_days)
        self.sB_days = new_sB_days
        self.pW.sB_days.setParent(None)

        self.dateEdit.setDate(QDate().currentDate().addDays(1))
        self.tW_menu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_menu.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_menu.setIconSize(QSize(160, 160))
        self.tW_menu.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tW_menu.viewport().installEventFilter(self)

        self.pB_modif.setEnabled(False)
        
        #transition before complete deletion
        self.pB_modif.hide()
        self.label_dessert.hide()
        self.sB_desserts.hide()
        
        self.pB_save.setEnabled(False)
        
        self.info_dialog = QMessageBox(self)

        # self.tW_shopping.setVisible(False)
        recipe_list = sorted(recipe_db.get_recipe_names(self.recipe_db.recipe_list), key=str.lower)
        self.lW_recipe.addItems(recipe_list)
        self.lW_recipe.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pB_back.hide()      

        self.frame_settings.hide()
        self.frame_search.hide()
        self.frame_edit_recipe.hide()
        
        #self.tW_ingredients.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.tW_ingredients.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.tW_history.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_history.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tW_history.setColumnCount(2)
        self.tW_history.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.reset_history()
        
        #User settings
        self.user_settings_ui()
        
        #webBrowser
        self.web_browser_ui()
         
        #images
        self.window().setWindowIcon(QIcon(self.dirname + '/UI/images/donut.png'))

        cw.load_pic(self.label_date, self.dirname + '/UI/images/icon_date_3colors_t_LD.png')
        # cw.load_pic(self.label_dessert, self.dirname + '/UI/images/icon_cupcake_t.png')
        cw.load_pic(self.label_user, self.dirname + '/UI/images/icon_user_color.png')
        # load_pic(self.label_dessert_2, self.dirname + '/UI/images/tag_dessert_color_LD.png')
        self.tW.setTabIcon(0,QIcon(self.dirname + '/UI/images/icon_chef_3colors.png'))
        self.tW.setTabIcon(1,QIcon(self.dirname + '/UI/images/icon_recipe_3colors.png'))
        self.tW.setTabIcon(2,QIcon(self.dirname + '/UI/images/icon_plate_3colors.png'))
        self.tB.setItemIcon(0, QIcon(self.dirname + '/UI/images/icon_menu_3colors.png'))
        self.tB.setItemIcon(1, QIcon(self.dirname + '/UI/images/icon_shopping_cart.png'))
        self.pB_user.setIcon(QIcon(self.dirname + '/UI/images/icon_user_t.png'))
        self.pB_new_menu.setIcon(QIcon(self.dirname + '/UI/images/icon_cover_3colors_new.png'))
        # self.pB_modif.setIcon(QIcon(self.dirname + '/UI/images/icon_edit.png'))
        self.pB_save.setIcon(QIcon(self.dirname + '/UI/images/icon_plate_3colors.png'))
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

        labels = [self.label_deco_1,self.label_deco_2,self.label_deco_3,self.label_deco_4,
                  self.label_deco_5,self.label_deco_6,self.label_deco_7,self.label_deco_8,
                  self.label_deco_9,self.label_deco_10,self.label_deco_11,self.label_deco_12,
                  self.label_deco_13,self.label_deco_14,self.label_deco_15,self.label_deco_16]
        
        for i, label in enumerate(labels):
            cw.load_pic(label, self.dirname + '/UI/images/icon_deco_%s.png' % (i+1))
        
        cw.load_pic(self.label_warning, self.dirname + '/UI/images/icon_fork_X_3colors_t_LD.png')
        self.pB_cancel.setIcon(QIcon(self.dirname + '/UI/images/icon_cancel.png'))
        self.pB_ok.setIcon(QIcon(self.dirname + '/UI/images/icon_ok.png'))
        self.pB_cancel_2.setIcon(QIcon(self.dirname + '/UI/images/icon_cancel.png'))
        self.pB_ok_2.setIcon(QIcon(self.dirname + '/UI/images/icon_ok.png'))
        self.pB_cancel_3.setIcon(QIcon(self.dirname + '/UI/images/icon_cancel.png'))
        self.pB_ok_3.setIcon(QIcon(self.dirname + '/UI/images/icon_ok.png'))
        self.pB_modif_2.setIcon(QIcon(self.dirname + '/UI/images/icon_edit.png'))
        self.pB_new_recipe.setIcon(QIcon(self.dirname + '/UI/images/icon_new_recipe.png'))
        self.pB_delete.setIcon(QIcon(self.dirname + '/UI/images/icon_bin.png'))
        self.pB_photo.setIcon(QIcon(self.dirname + '/UI/images/icon_photo.png'))
        
        self.img_settings_email.setPixmap(QPixmap(self.dirname + '/UI/images/icon_send.png').scaled(40,40))
        self.img_settings_days.setPixmap(QPixmap(self.dirname + '/UI/images/icon_date_3colors_t_LD.png').scaled(40,40))
        self.img_settings_storage.setPixmap(QPixmap(self.dirname + '/UI/images/icon_print.png').scaled(40,40))
        self.label_homepage.setPixmap(QPixmap(self.dirname + '/UI/images/icon_web_search_gp.png').scaled(40,40))
        # load_pic(self.img_settings_days, self.dirname + '/UI/images/icon_date_3colors_t_LD.png')
        # load_pic(self.img_settings_storage, self.dirname + '/UI/images/icon_print.png')

    def main(self):
        self.pW.show()

    def connect_actions(self):
        self.pB_new_menu.clicked.connect(self.on_new_menu)
        self.tW_menu.cellDoubleClicked.connect(self.on_card_recipe_selection)
        self.tW_history.cellDoubleClicked.connect(self.on_history_recipe_selection)
        # self.pB_modif.clicked.connect(self.on_card_modif)
        self.pB_save.clicked.connect(self.on_save_menu)
        self.pB_calendar.clicked.connect(self.on_calendar)
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
        self.pB_photo.clicked.connect(self.on_add_photo)
        self.pB_user.clicked.connect(self.on_user_settings)
        self.tB_storage.clicked.connect(lambda : self.openDir(self.lE_storage, u'de sauvegarde des fiches', dirpath = self.default_storage))
        self.pB_ok_3.clicked.connect(self.on_save_settings)
        self.pB_cancel_3.clicked.connect(self.on_quit_settings)
        self.lW_recipe.customContextMenuRequested.connect(self.on_recipe_right_click)
        self.tW_history.customContextMenuRequested.connect(self.on_history_right_click)
        self.cB_web.stateChanged.connect(self.on_show_web)
        
    def update_modif(self):
        self.dateEdit.dateChanged.connect(self.dummy_function)
        self.tW_menu.cellChanged.connect(self.on_drag_drop_event)
        self.sB_days.valueChanged.connect(self.on_nb_days_changed)
        self.lW_recipe.itemSelectionChanged.connect(self.on_recipe_selection)
        self.lE_title.textChanged.connect(self.on_title_changed)
        # self.sB_desserts.valueChanged.connect(self.on_dessert_selection)
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
        
        self.selectable_tags = [self.cB_tagdinner, self.cB_tagdessert, self.cB_tagdouble, self.cB_tagkids,
                                self.cB_taglunch, self.cB_tagwinter, self.cB_tagsummer, self.cB_tagvegan, self.cB_tagtips]
        for tag in self.selectable_tags:
            tag.toggled.connect(lambda _, cB=tag: self.on_tag_selected(cB))
        
        self.wV.urlChanged.connect(self.update_urlbar)
        
    def dummy_function(self, row, column):
        print('dummy function triggered %s %s' % (row, column))

    def is_filter_in_recipe_name(self, filter, recipe):
        if self.cB_search_recipe_name.isChecked():
            return filter in recipe.name.lower()
        return False

    def is_filter_in_ing_list(self,filter,recipe):
        if self.cB_search_ingredients.isChecked() and recipe.ingredients_list_qty is not None: 
            for ingredient in list(map(str.lower, recipe.ingredients_list_qty)):
                if filter in ingredient:
                    return True
        return False

    def is_filter_in_preparation(self, filter, recipe):
        if self.cB_search_preparation.isChecked() and recipe.preparation is not None:
            return filter in recipe.preparation.lower()
        return False

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
        with_filters = self.lE_with.text().split(',')
        recipeCount = 0

        for recipeIndex in range(self.lW_recipe.count()):
            recipeListItem = self.lW_recipe.item(recipeIndex)
            recipe = self.recipe_db.get_recipe_object(recipeListItem.text())
            show_recipe_flag = True
            
            for filter in with_filters:
                filter = filter.strip()
                isCriteriaMet = self.is_filter_in_recipe_name(filter, recipe)
                isCriteriaMet = isCriteriaMet or self.is_filter_in_ing_list(filter, recipe)
                isCriteriaMet = isCriteriaMet or self.is_filter_in_preparation(filter, recipe)
                
                show_recipe_flag = show_recipe_flag and isCriteriaMet

            show_recipe_flag = show_recipe_flag and self.is_filter_in_tags(recipe)

            self.lW_recipe.setItemHidden(recipeListItem, not show_recipe_flag)
            if show_recipe_flag:
                recipeCount += 1

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
    
    def on_new_menu(self):
        self.new_menu()
        self.populate_tW_menu(self.current_menu)
        # self.on_dessert_selection(self.sB_desserts.value()) #includes dessert, menu_list, shopping list #DEPRECATED
        self.populate_shopping_list()
        self.populate_menu_list()
        self.compute_score()
        # self.pB_modif.setEnabled(True)
        self.pB_save.setEnabled(True)
    
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
        
        self.stacks = {}
        
        #update tW_menu with menus
        recipe_list_lunch = [m[1] for m in table_menu]
        recipe_list_dinner = [m[2] for m in table_menu]
        for i, recipes_of_day in enumerate(zip(recipe_list_lunch, recipe_list_dinner)):
            recipe_lunch, recipe_dinner = recipes_of_day
            # text_lunch, text_dinner = (recipe_lunch.name, recipe_dinner.name)
            # # print((text_lunch, self.recipe_db.background_score(recipe_lunch, self.current_menu.start_day)))
            qtwi_lunch, qtwi_dinner = (QTableWidgetItem(cw.row_column_to_id(0,i)), QTableWidgetItem(cw.row_column_to_id(1,i)))
            # qtwi_lunch.setTextAlignment(Qt.AlignCenter)
            # qtwi_dinner.setTextAlignment(Qt.AlignCenter)

            self.tW_menu.setItem(0, i, qtwi_lunch)
            self.tW_menu.setItem(1, i, qtwi_dinner)

            # cw.display_image(recipe_lunch, self.dirname, qtwi_lunch, icon = True)
            # cw.display_image(recipe_dinner, self.dirname, qtwi_dinner, icon = True)
    
        #ability to add several recipes to a given slot
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
            
            stacked_lunch = cw.create_stack(recipe_lunch_stack, self.recipe_db, id = idplus)
            stacked_dinner = cw.create_stack(recipe_dinner_stack, self.recipe_db, id = idminus)
            
            stacked_lunch.signal.sig.connect(self.on_enter_recipe_stack)
            stacked_lunch.signal2.sig2.connect(self.on_lock_for_edition)
            stacked_lunch.signal3.sig3.connect(self.on_update_current_menu)
            stacked_dinner.signal.sig.connect(self.on_enter_recipe_stack)
            stacked_dinner.signal2.sig2.connect(self.on_lock_for_edition)
            stacked_dinner.signal3.sig3.connect(self.on_update_current_menu)
            
            self.stacks[idplus] = stacked_lunch
            self.stacks[idminus] = stacked_dinner
            
            qtwi_lunch = stacked_lunch.parentWidget()
            qtwi_dinner = stacked_dinner.parentWidget()
            # qtwi_lunch = cw.style_factory(qtwi_lunch, self.init_colors, self.colors)
            # qtwi_dinner = cw.style_factory(qtwi_dinner, self.init_colors, self.colors)
            
            self.tW_menu.setCellWidget(0, i, qtwi_lunch)
            self.tW_menu.setCellWidget(1, i, qtwi_dinner)

            # print(self.tW_menu.item(0,i).text())
    
    def on_enter_recipe_stack(self, id):
        if not self.lockedForEdition:#ongoing edition of recipe, locking others
            for key in self.stacks:
                if key != id:
                    self.stacks[key].frame_buttons.setVisible(False)
            if id in self.stacks:
                self.stacks[id].frame_buttons.setVisible(True)
            
    def on_lock_for_edition(self, id, lock):
        if lock:
            self.lockKeyId = id
            self.lockedForEdition = True
            self.pB_new_menu.setEnabled(False)
            self.dateEdit.setEnabled(False)
            self.sB_days.setEnabled(False)
            self.sB_desserts.setEnabled(False)
            self.cB_restes.setEnabled(False)
            self.pB_save.setEnabled(False)
        elif (not lock) and id == self.lockKeyId:
            self.lockKeyId = 'xx'
            self.lockedForEdition = False
            self.pB_new_menu.setEnabled(True)
            self.dateEdit.setEnabled(True)
            self.sB_days.setEnabled(True)
            self.sB_desserts.setEnabled(True)
            self.cB_restes.setEnabled(True)
            self.pB_save.setEnabled(True)
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
            qtwi_to = QTableWidgetItem(cw.row_column_to_id(row,column))
            self.tW_menu.setItem(from_row, from_column, qtwi_to)
            # self.tW_menu.setItem(from_row, from_column, qtwi)

            # cw.display_image(original_to_cell_recipe, self.dirname, qtwi, icon = True)
            
            #take stack from original to_cell and from_cell
            original_to_cell_stack = self.stacks[cw.row_column_to_id(row, column)]
            original_from_cell_stack = self.stacks[cw.row_column_to_id(from_row, from_column)]
            
            original_to_cell_stack_list = original_to_cell_stack.recipe_list
            original_from_cell_stack_list = original_from_cell_stack.recipe_list
            
            new_stacked_to = cw.create_stack(original_from_cell_stack_list, self.recipe_db, id = cw.row_column_to_id(row, column))
            new_stacked_from = cw.create_stack(original_to_cell_stack_list, self.recipe_db, id = cw.row_column_to_id(from_row, from_column))
            
            new_stacked_to.signal.sig.connect(self.on_enter_recipe_stack)
            new_stacked_to.signal2.sig2.connect(self.on_lock_for_edition)
            new_stacked_to.signal3.sig3.connect(self.on_update_current_menu)
            new_stacked_from.signal.sig.connect(self.on_enter_recipe_stack)
            new_stacked_from.signal2.sig2.connect(self.on_lock_for_edition)
            new_stacked_from.signal3.sig3.connect(self.on_update_current_menu)
            
            self.stacks[cw.row_column_to_id(row, column)] = new_stacked_to
            self.stacks[cw.row_column_to_id(from_row, from_column)] = new_stacked_from
            
            qtwi_to = new_stacked_to.parentWidget()
            qtwi_from = new_stacked_from.parentWidget()
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
                qtwi_lunch, qtwi_dinner = (QTableWidgetItem(cw.row_column_to_id(0,i)), QTableWidgetItem(cw.row_column_to_id(1,i)))
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

    
    def on_history_recipe_selection(self, row, column):
        if self.tab_recipe.isEnabled():#no effect when waiting for user confirmation in history tab
            recipes = self.tW_history.item(row, column).text().split(' | ')
            if len(recipes) == 1:
                recipe_name = recipes[0]
                self.switch_to_recipe(recipe_name)
            else:
                #display context menu with choices
                self.recipeMultiSelection = recipes
                pyautogui.click(button='right')
    
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
            
    def switch_to_recipe(self, recipe_name):
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
    
    def on_title_changed(self):
        title_ok = self.lE_title.text() != ''
        self.pB_ok_2.setEnabled(title_ok)
        self.pB_ok_2.setToolTip(['Il manque un titre pour la recette', 'Enregistrer'][title_ok])
    
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


            qtwi_lunch.setTextColor(QColor(self.colors['#color2#']))
            qtwi_dinner.setTextColor(QColor(self.colors['#color2#']))
        
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
        
        self.tW_history.scrollToBottom()
    
    def on_confirm_history_update(self):
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

    def on_calendar(self):
        # my_calendar_worker = cal.MyCalendar(self.current_menu)
        my_calendar_worker = gapi.MyCalendar(self.current_menu)
        
        my_calendar_worker.signal.sig.connect(self.print_thread_function)
        
        self.myThreads.append(my_calendar_worker)
        my_calendar_worker.start()
    
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
                    f.write(self.default_email)

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

                with open(user_id_file, 'w') as f:
                    f.write(self.default_email)

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
        self.lW_recipe.addItems(recipe_db.get_recipe_names(self.recipe_db.recipe_list))         #repopulate recipe list

    def reset_filters(self): #reset search/filter section(frame)
        self.cB_search.setText('Recherche avancée')   
        self.lE_with.setText('')
        self.cB_search_recipe_name.setChecked(True)
        self.cB_search_ingredients.setChecked(False)
        self.cB_search_preparation.setChecked(False)
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

    def clear_edit_recipe_window(self):
        self.img_dish.setPixmap(QPixmap())

        self.lw_ingredients.clear()

        self.tB_preparation.clear()
        tags = [self.cB_tagdessert, self.cB_tagdinner, self.cB_tagdouble, self.cB_tagkids, self.cB_taglunch,
                self.cB_tagsummer, self.cB_tagwinter, self.cB_tagvegan, self.cB_tagtips]
        for tag in tags:
            tag.setChecked(False)
        
        # We keep that for now to remember how to add ing/units items to combo box
        #ingredients, units = self.recipe_db.get_ingredients_units_list()
        #self.cB_unit.addItems([''] + units)
        #self.cB_unit.setCurrentIndex(0)
        self.sB_time.setValue(0)

    def disable_other_tabs(self):
        self.tW.setTabEnabled(0, False)
        self.tW.setTabEnabled(2, False)
        self.cB_search.setEnabled(False)
        self.pB_new_recipe.setEnabled(False)
        self.pB_modif_2.setEnabled(False)

    def on_new_recipe(self):
        self.disable_other_tabs()
        #reset all fields
        self.label_newedit.setText('Nouvelle Recette')
        self.lE_title.setText('Nouveau Titre')
        
        self.add_new_ingredient_to_list(Ingredient()) #Add empty ing for input
        
    def on_edit_recipe(self):
        self.disable_other_tabs()
        #populate all fields
        self.label_newedit.setText('Modifier la recette')
        recipe:Recipe
        recipe = self.recipe_db.get_recipe_object(self.lW_recipe.currentItem().text())
        self.lE_title.setText(recipe.name)
        cw.display_image(recipe, self.dirname, self.img_dish, icon=False)
        self.populate_ing_list(recipe)
        if recipe.time is not None:
            self.sB_time.setValue(int(recipe.time))
        else:
            self.sB_time.setValue(0)
        tags = [self.cB_tagdessert, self.cB_tagdinner, self.cB_tagdouble, self.cB_tagkids, self.cB_taglunch,
                self.cB_tagsummer, self.cB_tagwinter, self.cB_tagvegan, self.cB_tagtips]
        tag_names = ['dessert', 'soir', 'double', 'kids', 'midi', 'ete', 'hiver', 'vegan', 'tips']
        for tag, tag_name in zip(tags, tag_names):
            tag.setChecked(recipe.isTagged(tag_name))
        self.tB_preparation.setText(recipe.preparation.replace('\n', '<br/>'))

    def populate_ing_list(self, recipe:Recipe): #OK but can be improved
        if recipe.ing_list is None:
            return
        mand_ing_list, opt_ing_list = recipe.get_mandatory_and_optional_ing_lists()
        for ingredient in mand_ing_list:
            self.add_new_ingredient_to_list(ingredient)
        #self.lw_ingredients.addItem(QListWidgetItem("Optionels : "))
        for ingredient in opt_ing_list:
            self.add_new_ingredient_to_list(ingredient)
        self.add_new_ingredient_to_list(Ingredient()) # Add extra line for new ing input

    def on_btn_confirm_changes_clicked(self, ing_item_id):
        ing_item:IngredientItem
        ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(self.lw_ingredients.count()-1)).findChild(IngredientItem)
        if ing_item.getUID() == ing_item_id:
            self.add_new_ingredient_to_list(Ingredient())

    def rm_ing_item_from_list(self, ing_item_id):
        for i in range(0, self.lw_ingredients.count()):
            ing_item:IngredientItem
            ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(i)).findChild(IngredientItem)
            if ing_item_id == ing_item.getUID():
                self.lw_ingredients.takeItem(i)
                break

    def add_new_ingredient_to_list(self, ingredient:Ingredient):
        #TODO : handle the case were the ingredient is already in the list
        ui_file = QFile(os.path.dirname(__file__) + '/UI/ingredient_item.ui')
        ing_item = IngredientItem(ingredient, self.lw_ingredients, parent = QUiLoader().load(ui_file))
        ing_item.on_btn_confirm_changes_clicked.connect(self.on_btn_confirm_changes_clicked)
        ing_item.on_btn_rm_item_clicked.connect(self.rm_ing_item_from_list)
        if ingredient.name == "" and ingredient.qty_unit == "" and ingredient.qty == -1:
            ing_item.selectWidgetMode(IngredientItem.WIDGET_EDIT_ING_MODE)

        list_widget_item = QListWidgetItem()
        list_widget_item.setSizeHint(QSize(0,30))

        self.lw_ingredients.addItem(list_widget_item)
        self.lw_ingredients.setItemWidget(list_widget_item,ing_item.parent_widget)

    def on_confirm_recipe(self):
        #check if ok to save
        #title not empty
        title = self.lE_title.text()
        #allow auto switch in case of warning message
        auto_switch = ''
        
        #if not ok to save -> warning message
        if self.label_newedit.text() == 'Nouvelle Recette' and self.recipe_db.contains(title):#recipe already exists
            self.display_error('Cette recette existe déjà, vous pouvez la modifier')
            
            #enable swicth to edit mode
            auto_switch = 'edit'
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
            if self.recipe_db.contains(title):
                image = self.recipe_db.get_recipe_object(title).image
            if image_cell != '':
                image = '/images/' + image_cell
            #case with ingredients not empty -> combine ingredients to string
            now_optionals = False
            ing_dict = {}

            for ing_index in range(self.lw_ingredients.count()-1): # "-1 in order to ignore the last 'input' line"
                ing_item:IngredientItem
                ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(ing_index)).findChild(IngredientItem)
                ing_dict[ing_item.lbl_ing_name.text()] = [float(ing_item.lbl_ing_qty.text()), ing_item.lbl_ing_qty_unit.text()]

            #combine tags to string
            tags = [self.cB_tagdessert, self.cB_tagdinner, self.cB_tagdouble, self.cB_tagkids, self.cB_taglunch,
                    self.cB_tagsummer, self.cB_tagwinter, self.cB_tagvegan, self.cB_tagtips]
            tag_names = ['dessert', 'soir', 'double', 'kids', 'midi', 'ete', 'hiver', 'vegan', 'tips']
            tag_checked_list = [tag_name for tag, tag_name in zip(tags, tag_names) if tag.isChecked()]
            tag_cell = '/'.join(tag_checked_list)
            #case with preparation not empty -> combine preparation to string
            preparation_cell = web.with_clickable_links(self.tB_preparation.toPlainText())
            #case with preparation time not 0
            time_cell = ''
            if self.sB_time.text() != '0':
                time_cell = self.sB_time.text()
            
            time = None
            if time_cell != '':
                time = time_cell

            #add recipe to database
            recipe = Recipe(uuid.uuid4(), title, ing_dict, preparation_cell, time, tag_checked_list, image)
            if self.label_newedit.text() == 'Modifier la recette':  #update existing recipe
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
            copy2(self.recipe_db.recipe_file, self.dirname + '/backup/recipe_backup.ods')
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

        self.clear_edit_recipe_window()

    def reenable_other_tabs(self):
        self.tW.setTabEnabled(0, True)
        self.tW.setTabEnabled(2, True)
        self.cB_search.setEnabled(True)
        self.pB_new_recipe.setEnabled(True)
        self.pB_modif_2.setEnabled(True)
        self.pB_delete.setEnabled(True)
        self.pB_new_recipe.setChecked(False)
        self.pB_modif_2.setChecked(False)
        self.cB_web.setChecked(False)

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
        cw.display_new_image(self.recipe_image_path, self.img_dish)
    
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
        self.clear_edit_recipe_window()
    
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
                    
    def on_user_settings(self):
        self.frame_settings.show()
        self.frame.hide()
        
        # if os.path.isfile(self.user_id_file):
        #     with open(self.user_id_file, 'r') as f:
        #         #for legacy compatibility
        #         data = f.readline().strip().split(';')
        #         if len(data) == 1:
        #             self.default_email = data[0]
        #         else:
        #             self.default_email, nb_days, self.default_storage = data
        #             self.default_nb_days = int(nb_days)
        self.lE_email.setText(self.default_email)
        self.sB_settings_days.setValue(self.default_nb_days)
        self.lE_storage.setText(self.default_storage)
        self.lE_homepage.setText(self.homepage.toString())
    
    def on_save_settings(self):
        self.default_email = self.lE_email.text()
        self.default_nb_days = self.sB_settings_days.value()
        storage = self.lE_storage.text()
        if os.path.isdir(storage):
            self.default_storage = storage
        else:
            self.default_storage = self.dirname + '/Mes_Fiches/'
            self.display_error("Le chemin pour l'enregistrement des fiches n'est pas valide," +
                               " l'emplacement par défaut a été sélectionné (%s)" % self.default_storage)
        
        self.homepage = QUrl(self.lE_homepage.text())
        
        with open(self.user_id_file, 'w') as f:
            f.write(';'.join([self.default_email, 
                              str(self.default_nb_days), 
                              self.default_storage,
                              self.homepage.toString()]))
            
        self.frame_settings.hide()
        self.frame.show()
        
    def on_quit_settings(self):
        self.frame_settings.hide()
        self.frame.show()
        
    def on_recipe_right_click(self, pos):
        # print('right clicked')
        # print(pos)
        globalPos = self.lW_recipe.mapToGlobal(pos)
        # print(globalPos)
        #create right-click menu
        right_click_menu = QMenu(self)
        right_click_menu.setToolTipsVisible(True)
        right_click_menu.setStyleSheet('QWidget{color:%s;selection-color:%s;}' % 
                                       (self.colors['#color1_dark#'], self.colors['#color3_dark#']))
        
        #modify
        actionModify = QAction(right_click_menu)
        actionModify.setText('Modifier')
        actionModify.setIcon(QIcon(self.dirname + '/UI/images/icon_edit_2.png'))
        actionModify.triggered.connect(self.pB_modif_2.click)
        #print
        actionPrint = QAction(right_click_menu)
        actionPrint.setText('Imprimer')
        actionPrint.setIcon(QIcon(self.dirname + '/UI/images/icon_print.png'))
        actionPrint.triggered.connect(self.pB_print_2.click)
        #send
        actionSend = QAction(right_click_menu)
        actionSend.setText('Envoyer')
        actionSend.setIcon(QIcon(self.dirname + '/UI/images/icon_send.png'))
        actionSend.triggered.connect(self.pB_send_2.click)
        #add to menu -> days -> lunch/dinner -> add/replace
        add_to_menu = QMenu('Prévoir cette recette...', right_click_menu)
        add_to_menu.setToolTipsVisible(True)
        
        mapper = QSignalMapper(self) #instead of lambda to connect action signals properly
         
        for i in range(self.tW_menu.columnCount()):
            menuDay = QMenu(self.tW_menu.horizontalHeaderItem(i).text(), add_to_menu)
            menuDay.setToolTipsVisible(True)
            
            actionLunch = QAction(menuDay)
            actionLunch.setText('Midi')
            actionLunch.setIcon(QIcon(self.dirname + '/UI/images/tag_lunch_color_2.png'))
            lunchToolTip = '\n'.join(recipe_db.get_recipe_names(self.stacks[cw.row_column_to_id(0, i)].recipe_list))
            actionLunch.setToolTip(lunchToolTip)
            
            mapper.setMapping(actionLunch, cw.row_column_to_id(0, i))
            actionLunch.triggered.connect(mapper.map)
            
            actionDinner = QAction(menuDay)
            actionDinner.setText('Soir')
            actionDinner.setIcon(QIcon(self.dirname + '/UI/images/tag_dinner_color_2.png'))
            dinnerToolTip = '\n'.join(recipe_db.get_recipe_names(self.stacks[cw.row_column_to_id(1, i)].recipe_list))
            actionDinner.setToolTip(dinnerToolTip)
            
            mapper.setMapping(actionDinner, cw.row_column_to_id(1, i))
            actionDinner.triggered.connect(mapper.map)
            
            menuDay.addAction(actionLunch)
            menuDay.addAction(actionDinner)
            add_to_menu.addMenu(menuDay)
        
        right_click_menu.addMenu(add_to_menu)
        right_click_menu.addSeparator()
        right_click_menu.addAction(actionModify)
        right_click_menu.addAction(actionPrint)
        right_click_menu.addAction(actionSend)
        mapper.mappedString.connect(self.on_add_recipe_right_click)
        
        right_click_menu.exec_(globalPos)
        
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
        
    def user_settings_ui(self):
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
        
        self.label_contact.setOpenExternalLinks(True)
        self.label_contact.setTextFormat(Qt.RichText)
        self.label_contact.setText("<a href='mailto:%s?Subject=Contact'>%s</a>" % (self.contact, self.contact))
        
    def web_browser_ui(self):
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"
        self.frame_wB.hide()
        self.wV = QWebEngineView()
        page = cw.WebEnginePage(self.wV)
        self.wV.setPage(page)
        
        self.wV.load(self.homepage)
        self.gL_web.addWidget(self.wV)
        self.navtb = QToolBar("Navigation")
        self.navtb.setStyleSheet('QToolBar{background-color:transparent;}QToolButton{background:transparent;}')
        self.navtb.setIconSize( QSize(30,30) )
        self.hL_tools.addWidget(self.navtb)
        
        self.pB_cook = QPushButton('', self.frame_wB)
        self.pB_cook.setFixedSize(60,60)
        self.pB_cook.setIconSize(QSize(40,40))
        self.pB_cook.setIcon(QIcon(self.dirname + '/UI/images/icon_service.png'))
        self.pB_cook.setToolTip('Recopier cette recette')
        self.pB_cook.clicked.connect(self.on_parse_html)
        self.navtb.addWidget(self.pB_cook)
        
        back_btn = QAction( QIcon(self.dirname + '/UI/images/icon_back.png'), "Back", self)
        back_btn.setToolTip("Page précédente")
        back_btn.triggered.connect( self.wV.back )
        self.navtb.addAction(back_btn)
        
        next_btn = QAction( QIcon(self.dirname + '/UI/images/icon_fwd.png'), "Forward", self)
        next_btn.setToolTip("Page suivante")
        next_btn.triggered.connect( self.wV.forward )
        self.navtb.addAction(next_btn)

        reload_btn = QAction( QIcon(self.dirname + '/UI/images/icon_reload.png'), "Reload", self)
        reload_btn.setToolTip("Recharger la page")
        reload_btn.triggered.connect( self.wV.reload )
        self.navtb.addAction(reload_btn)

        home_btn = QAction( QIcon(self.dirname + '/UI/images/icon_chef.png'), "Home", self)
        home_btn.setToolTip("Page d'accueil")
        home_btn.triggered.connect(lambda: self.wV.setUrl(self.homepage))
        self.navtb.addAction(home_btn)
        
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap( QPixmap(self.dirname + '/UI/images/icon_nolock_.png') )
        self.navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect( self.navigate_to_url )
        self.navtb.addWidget(self.urlbar)

        stop_btn = QAction( QIcon(self.dirname + '/UI/images/icon_fork_X.png'), "Stop", self)
        stop_btn.setToolTip("Interrompre le chargement")
        stop_btn.triggered.connect( self.wV.stop )
        self.navtb.addAction(stop_btn)
        
        open_file_action = QAction( QIcon(self.dirname + '/UI/images/icon_open.png'), "Ouvrir une page web...", self)
        open_file_action.setToolTip("Ouvrir le fichier HTML")
        open_file_action.triggered.connect( self.open_html )
        self.navtb.addAction(open_file_action)

        save_file_action = QAction( QIcon(self.dirname + '/UI/images/icon_save.png'), "Enregistrer sous...", self)
        save_file_action.setToolTip("Enregistrer la page en cours")
        save_file_action.triggered.connect( self.save_file )
        self.navtb.addAction(save_file_action)
    
    def open_html(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Ouvrir le fichier", "",
                        "Hypertext Markup Language (*.htm *.html);;"
                        "Tous types de fichiers (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.wV.setHtml( html )
            self.urlbar.setText( filename )
    
    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Enregistrer la page sous", "",
                        "Hypertext Markup Language (*.htm *html);;"
                        "Tous types de fichiers (*.*)")

        if filename:
            
            def write_html_to_file(html):
                with open(filename, 'w') as f:
                    f.write(html)

            self.wV.page().toHtml(write_html_to_file)
            
            # html = self.wV.page().toHtml()
            # with open(filename, 'w') as f:
            #     f.write(html)
                
    def navigate_to_url(self): # Does not receive the Url
        q = QUrl( self.urlbar.text() )
        if q.scheme() == "":
            q.setScheme("http")

        self.wV.setUrl(q)
    
    def update_urlbar(self, q):

        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap( QPixmap(self.dirname + '/UI/images/icon_lock_.png') )

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap( QPixmap(self.dirname + '/UI/images/icon_nolock_.png') )

        self.urlbar.setText( q.toString() )
        self.urlbar.setCursorPosition(0)
        
        my_html_worker = web.MyHTMLParser(self.urlbar.text())
            
        my_html_worker.signal.sig.connect(self.on_new_webpage)
        
        self.myThreads.append(my_html_worker)
        my_html_worker.start()
    
    def on_parse_html(self):
        url = self.urlbar.text()
        recipe_name, ingredients_list, steps = web.marmiton_parser(url)
        list_failed = []
        message = ''
        
        if recipe_name != '':
            self.lE_title.setText(recipe_name)
        else:
            list_failed.append('- Titre')
            self.lE_title.setText('Nouvelle Recette')

        if ingredients_list != []:
            ing_dict = {}
            for ing in ingredients_list:
                ing_qty, ing_name = ing.split(" ", 1)
                ing_dict[ing_name] = [ing_qty,""]
            recipe = Recipe(uuid.uuid4(), "", ing_dict)
            self.populate_ing_list(recipe)
        else:
            list_failed.append('- Liste des ingrédients')
            self.tW_ingredients.clear()
            self.tW_ingredients.setColumnCount(1)
            self.tW_ingredients.setRowCount(1)
            
        if steps != []:
            self.tB_preparation.setText('\n'.join(steps))
        else:
            list_failed.append('- Préparation')
            self.tB_preparation.clear()
            
        #TBC to avoid previous settings removal, following lines commented
        # self.sB_time.setValue(0)
        
        # tags = [self.cB_tagdessert, self.cB_tagdinner, self.cB_tagdouble, self.cB_tagkids, self.cB_taglunch,
        #         self.cB_tagsummer, self.cB_tagwinter, self.cB_tagvegan, self.cB_tagtips]
        # tag_names = ['dessert', 'soir', 'double', 'kids', 'midi', 'ete', 'hiver', 'vegan', 'tips']
        # for tag, tag_name in zip(tags, tag_names):
        #     tag.setChecked(False)
                    
        self.tB_preparation.append("<a href='%s'>%s</a>" % (url, url))
        message += 'Le lien vers la recette a été ajouté.'
        
        if len(list_failed) > 0:
            message += "\nLes éléments suivants n'ont pas pu être copiés :\n%s" % '\n'.join(list_failed)
            self.display_error(message)
        else:
            message += "<br/>La recette a été correctement importée !"
            self.print_thread_function(message, icon_path = self.dirname + '/UI/images/icon_service.png')
       
    def on_new_webpage(self, url, okToParse):
        if url == self.urlbar.text():#make sure url validated matches current url (asynchronous thread treatment)
            icon = QIcon(self.dirname + '/UI/images/icon_service%s.png' % ['_', ''][okToParse])
            self.pB_cook.setIcon(icon)
            self.pB_cook.setToolTip(['Copier le lien', 'Importer la recette'][okToParse])
    
    def on_show_web(self):
        if self.cB_web.isChecked():
            if self.lE_title.text() != 'Nouveau Titre':
                new_search = QUrl("https://www.google.com/search?q=%s" %
                                  self.lE_title.text().replace(' ', '+'))
                self.wV.setUrl(new_search)
        else:
            self.wV.setUrl(self.homepage)


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
    dirname = os.path.dirname(__file__)
    #declare and read GUI file
    myUiFile = dirname + '/UI/Main_Window.ui'
    w = QUiLoader().load(myUiFile)
    #Create and display GUI object
    myGUI = MainGUI(parent = w, recipe_db = recipe_db)
    myGUI.main()
    
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
    s = '250 l'
    qty = extract_number(s)
    print(qty)
    # import re

    # myString = "This is my tweet check it out https://example.com/blah"

    # print(re.search("(?P<url>https?://[^\s]+)", myString).group("url"))

def main(): #Entry point

    dirname = os.path.dirname(__file__)
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
