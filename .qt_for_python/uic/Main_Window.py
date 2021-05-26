# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_Window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource2_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModal)
        MainWindow.resize(1183, 783)
        font = QFont()
        font.setFamily(u"Poiret One")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"/**/\n"
"QWidget{\n"
"background-color:#ccc1ae;\n"
"font-family:Poiret One;\n"
"font: bold;\n"
"}\n"
"/**/\n"
"\n"
"QCheckBox#cB_restes_2::indicator:unchecked {\n"
"    image: url(file:///../UI/images/icon_recycle_uncheck.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_restes_2::indicator:checked {\n"
"    image: url(file:///../UI/images/icon_recycle_check.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_restes_2::indicator:hover {\n"
"	width:45px;\n"
"	height:45px;\n"
"}\n"
"\n"
"\n"
"QCheckBox#cB_recherche::indicator:unchecked {\n"
"    image: url(file:///../UI/images/icon_up_arrow.png);\n"
"	width:20px;\n"
"	height:20px;\n"
"}\n"
"\n"
"QCheckBox#cB_recherche::indicator:checked {\n"
"    image: url(file:///../UI/images/icon_down_arrow.png);\n"
"	width:20px;\n"
"	height:20px;\n"
"}\n"
"\n"
"QCheckBox#cB_recherche::indicator:hover{\n"
"	width:18px;\n"
"	height:18px;\n"
"}\n"
"\n"
"/*\n"
"QGroupBox::indicator:unchecked {\n"
"    image: url(:/images/icon_unchecked_.png);\n"
""
                        "}\n"
"\n"
"QGroupBox::indicator:checked {\n"
"    image: url(:/images/icon_checked_.png);\n"
"background:white;\n"
"}\n"
"\n"
"QGroupBox::indicator {\n"
"    width: 30px;\n"
"    height: 31px;\n"
"}\n"
"*/\n"
"\n"
"/*\n"
"QTabBar::tab {\n"
"    background: transparent;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"	background:white;\n"
"font: bold;\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; \n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    left: 5px; \n"
"}\n"
"*/\n"
"\n"
"/**/\n"
"QTabWidget::pane { /* The tab widget frame */\n"
"    border-top: 2px solid #077B8A;\n"
"    position: absolute;\n"
"    top: -0.5em;\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    alignment: center;\n"
"}\n"
"\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"   /* \n"
"	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #A2D5C6, stop: 0.2 #077B8A,\n"
"                                stop: 0.8 #0"
                        "77B8A, stop: 1.0 #A2D5C6);\n"
"*/\n"
"	background-color:#A2D5C6;\n"
"    border: 2px solid #077B8A;\n"
"    border-bottom-color: #077B8A; /* same as the pane color */\n"
"    border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"    min-width: 8ex;\n"
"    padding: 5px;\n"
"	color:#077B8A;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"   /* \n"
"	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #077B8A, stop: 0.3 #A2D5C6,\n"
"                                stop: 0.7 #A2D5C6, stop: 1.0 #077B8A);\n"
"	*/\n"
"	background-color:#077B8A;\n"
"	color:#A2D5C6;\n"
"\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color: #077B8A;\n"
"    border-bottom-color: #077B8A; /* same as pane color */\n"
"\n"
"}\n"
"/**/\n"
"\n"
"QToolBox::tab {\n"
"   /* \n"
"	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #077B8A, stop: 0.4 #A2D5C6,\n"
"                                stop: 0.5 #A2D5C6"
                        ", stop: 1.0 #077B8A);\n"
"	*/\n"
"	background-color:#A2D5C6;\n"
"    border-radius: 5px;\n"
"	color: #077B8A;\n"
"}\n"
"QToolBox::tab:hover, QToolBox::tab:selected {\n"
"   /* \n"
"	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #D1D1D1, stop: 1.0 #EEEEEE);\n"
"   */\n"
"	 background-color:#077B8A;\n"
"	border-radius: 5px;\n"
"    color: #A2D5C6;\n"
"	\n"
"}\n"
"\n"
"QToolBox::tab:selected {\n"
"\n"
"}\n"
"\n"
"QPushButton{\n"
"     background-color: #5C3C92;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: #A2D5C6;\n"
"     font: bold 18px;\n"
"     /*min-width: 10em;*/\n"
"     padding: 8px;\n"
"	color:#A2D5C6;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	border-color: #D72631;\n"
"}\n"
"\n"
"QPushButton:pressed,  QPushButton:checked{\n"
"    border-width: 5px;\n"
"	border-radius: 15px;\n"
"	font:  15px;\n"
"	border-color: #D72631;\n"
"}\n"
"\n"
"QPushButton#pB_filter{\n"
"image: url(file:///../"
                        "UI/images/icon_filter.png);\n"
"max-width:70px;\n"
"max-height:70px;\n"
"}\n"
"\n"
"QPushButton#pB_filter:pressed,  QPushButton#pB_filter:checked{\n"
"    border-width: 5px;\n"
"	border-radius: 15px;\n"
"	image: url(file:///../UI/images/icon_filter_red.png);\n"
"	border-color: #D72631;\n"
"}\n"
"\n"
"QPushButton#pB_option, QPushButton#pB_option_2 {\n"
"     background-color: #ccc1ae;\n"
"     border-style: outset;\n"
"     border-width: 0px;\n"
"     border-radius: 0px;\n"
"     border-color: #ccc1ae;\n"
"     font: 18px;\n"
"     /*min-width: 10em;*/\n"
"     padding: 4px;\n"
"	color:#077b8a;\n"
"\n"
"}\n"
"\n"
"QPushButton#pB_option:hover, QPushButton#pB_option_2:hover {\n"
"	color:#d72631;\n"
"}\n"
"\n"
"QPushButton#pB_option:pressed, QPushButton#pB_option_2:pressed, QPushButton#pB_option:checked, QPushButton#pB_option_2:checked {\n"
"	color:#5c3c92;\n"
"font: bold 20px;\n"
"}\n"
"\n"
"QTableWidget {\n"
"background-color: #b7cab9;\n"
"selection-background-color: #5C3C92;\n"
"selection-color: #A2D5C6;\n"
"al"
                        "ternate-background-color: #CCC1AE;\n"
"}\n"
"\n"
"QTableWidget::item:hover{\n"
"color:#5C3C92;\n"
"}\n"
"\n"
"QTableWidget#tW_historique {\n"
"background-color: #e8ddc8;\n"
"\n"
"}\n"
"\n"
"QDateEdit {\n"
"\n"
"background-color: #A2D5C6;\n"
"}\n"
"\n"
"QSpinBox {\n"
"background-color: #A2D5C6;\n"
"}\n"
"\n"
"QListWidget {\n"
"background-color: #e8ddc8;\n"
"selection-background-color: #5C3C92;\n"
"selection-color: #b7cab9;\n"
"alternate-background-color: #CCC1AE;\n"
"}\n"
"\n"
"QListWidget::item:hover{\n"
"color:#5C3C92;\n"
"}\n"
"\n"
"QListWidget#lW_menu, QListWidget#lW_courses {\n"
"background-color: #b7cab9;\n"
"\n"
"}\n"
"\n"
"QListWidget#lW_menu {\n"
"border: 1px solid #077b8a;\n"
"}\n"
"\n"
"QLineEdit {\n"
"background-color: #A2D5C6;\n"
"}\n"
"\n"
"QFrame#frame_tags, QFrame#frame_tags_2 {\n"
"    background-color: #A2D5C6;\n"
"	border: 2px solid #077B8A;\n"
"    /*border-bottom-color: #077B8A;  same as the pane color */\n"
"    /*border-top-left-radius: 5px;*/\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QL"
                        "abel#label_vegan, QLabel#label_kids, QLabel#label_double, QLabel#label_summer, QLabel#label_winter, QLabel#label_dessert_2, QLabel#label_lunchdinner, QLabel#label_tips{\n"
"background-color: #A2D5C6;\n"
"}\n"
"\n"
"QLabel#label_newedit{\n"
"color: #5c3c92;\n"
"}\n"
"\n"
"QCheckBox#cB_tagdouble, QCheckBox#cB_tagkids, QCheckBox#cB_tagvegan, QCheckBox#cB_tagsummer, QCheckBox#cB_tagwinter, QCheckBox#cB_tagdessert, QCheckBox#cB_taglunch, QCheckBox#cB_tagdinner, QCheckBox#cB_tagtips{\n"
"background-color: #A2D5C6;\n"
"}\n"
"\n"
"QComboBox {\n"
"	border: 4px solid #5C3C92;\n"
"	border-radius: 3px;\n"
"	/*background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a2d5c6, stop:0.1 #b7cab9, stop:0.9 #b7cab9, stop:1 #a2d5c6);*/\n"
"	background: #b7cab9;\n"
"	padding: 1px 23px 1px 3px;\n"
"	min-width: 6em;\n"
"	color: #077B8A;\n"
"font-size: 18px;\n"
"\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 20px;\n"
"\n"
"	border-top-right-radius: 3px;\n"
"	borde"
                        "r-bottom-right-radius: 3px;\n"
"}\n"
"QComboBox::down-arrow {\n"
"     image: url(file:///../UI/images/icon_down_arrow.png);\n"
"	/*image: url(file:///../UI/images/icon_edit.png);*/\n"
"	width: 20px;\n"
"	height: 20px;\n"
"}\n"
"\n"
"QComboBox#cB_ingredient, QComboBox#cB_unit{\n"
"border: 1px solid #5C3C92;\n"
"	border-radius: 2px;\n"
"	/*background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a2d5c6, stop:0.1 #b7cab9, stop:0.9 #b7cab9, stop:1 #a2d5c6);*/\n"
"	background: #b7cab9;\n"
"	padding: 1px 1px 1px 1px;\n"
"	min-width: 6em;\n"
"	color: #077B8A;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"QComboBox#cB_ingredient::down-arrow, QComboBox#cB_unit::down-arrow {\n"
"	width: 15px;\n"
"	height: 15px;\n"
"}\n"
"/*\n"
"QComboBox::down-arrow:hover {\n"
"	width: 18px;\n"
"	height: 18px;\n"
"}*/\n"
"\n"
" \n"
"QComboBox QAbstractItemView{\n"
"	background-color: #CCC1AE;\n"
"	/*color: #077B8A;*/\n"
" 	\n"
"	selection-background-color: #5C3C92;\n"
"	/*selection-color: #A2D5C6;*/\n"
"}\n"
"\n"
"/*QHeaderView { \n"
"qproper"
                        "ty-defaultAlignment: AlignHCenter, AlignVCenter;\n"
"qproperty-iconSize: 60p 60px;\n"
"\n"
" }*/\n"
"\n"
"/*\n"
"QFrame#frame_courses{\n"
"image: url(file:///../UI/images/benchmark/list_frame2.png) ;\n"
"\n"
"}*/\n"
"\n"
"QFrame#frame_bottom{\n"
"	border: 4px solid #5C3C92;\n"
"	border-radius: 10px;\n"
"	background-color:#b7cab9;\n"
"\n"
"}\n"
"\n"
"QFrame#frame_details{\n"
"	border: 4px solid #5C3C92;\n"
"	border-radius: 10px;\n"
"	/*background-color:#A2D5C6;*/\n"
"\n"
"}\n"
"\n"
"QFrame#frame_new_recipe{\n"
"	border: 4px solid #d72631;\n"
"	border-radius: 10px;\n"
"	/*background-color:#A2D5C6;*/\n"
"\n"
"}\n"
"\n"
"QFrame#frame_add_ingredient{\n"
"	border: 1px solid #077b8a;\n"
"	border-radius: 3px;\n"
"	/*background-color:#A2D5C6;*/\n"
"\n"
"}\n"
"\n"
"QFrame#frame_confirm {\n"
"    background-color: #A2D5C6;\n"
"	border: 4px solid #D72631;\n"
"    /*border-bottom-color: #077B8A;  same as the pane color */\n"
"    /*border-top-left-radius: 5px;*/\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QLabel#label_confi"
                        "rm, QLabel#label_warning {\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QToolTip {\n"
"opacity: 300;\n"
"	border: 2px solid #5C3C92;\n"
"    border-radius: 4px;\n"
"    padding: 2px;\n"
"    background-color: #CCC1AE;\n"
"\n"
"}\n"
"\n"
"QScrollBar:vertical, QScrollBar:horizontal {\n"
"	border: 1px solid #077B8A;\n"
"	background:#CCC1AE;\n"
"	width:10px; \n"
"	margin: 0px 0px 0px 0px;\n"
"  }\n"
" QScrollBar::handle:vertical, QScrollBar::handle:horizontal {\n"
"	background: #5C3C92;\n"
"	min-height: 0px;\n"
"}\n"
"QScrollBar::add-line:vertical, QScrollBar::add-line:horizontal {\n"
"	background: #5C3C92;\n"
"	height: 0px;\n"
"	subcontrol-position: bottom;\n"
"	subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical, QScrollBar::sub-line:horizontal {\n"
"	background: #5C3C92;\n"
"	height: 0 px;\n"
"	subcontrol-position: top;\n"
"	subcontrol-origin: margin;\n"
"}\n"
"\n"
"QTextBrowser{\n"
"white-space: pre-line;\n"
"}\n"
"\n"
"QTextBrowser#tB_ingredients, QTextBrowser#tB_preparation{\n"
"backgroun"
                        "d: #a2d5c6;\n"
"border: 1px solid #077b8a;\n"
"}\n"
"\n"
"/**\n"
"CheckBox icons for new recipe\n"
"**/\n"
"\n"
"QCheckBox#cB_tagdouble::indicator:unchecked {\n"
"    image: url(file:///../UI/images/tag_double_black_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagdouble::indicator:checked {\n"
"    image: url(file:///../UI/images/tag_double_color_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagdouble::indicator:hover {\n"
"	width:45px;\n"
"	height:45px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagkids::indicator:unchecked {\n"
"    image: url(file:///../UI/images/tag_kids_black_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagkids::indicator:checked {\n"
"    image: url(file:///../UI/images/tag_kids_color_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagkids::indicator:hover {\n"
"	width:45px;\n"
"	height:45px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagvegan::indicator:unchecked {\n"
"    image: url(file:///../UI/images/tag_vegan"
                        "_black_LD.png);\n"
"	width:60px;\n"
"	height:60px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagvegan::indicator:checked {\n"
"    image: url(file:///../UI/images/tag_vegan_color_LD.png);\n"
"	width:60px;\n"
"	height:560px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagvegan::indicator:hover {\n"
"	width:55px;\n"
"	height:55px;\n"
"}\n"
"\n"
"QCheckBox#cB_taglunch::indicator:unchecked {\n"
"    image: url(file:///../UI/images/tag_lunch_black_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_taglunch::indicator:checked {\n"
"    image: url(file:///../UI/images/tag_lunch_color_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_taglunch::indicator:hover {\n"
"	width:45px;\n"
"	height:45px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagdinner::indicator:unchecked {\n"
"    image: url(file:///../UI/images/tag_dinner_black_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagdinner::indicator:checked {\n"
"    image: url(file:///../UI/images/tag_dinner_color_LD.png);\n"
"	width:50px;\n"
"	height"
                        ":50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagdinner::indicator:hover {\n"
"	width:45px;\n"
"	height:45px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagtips::indicator:unchecked {\n"
"    image: url(file:///../UI/images/tag_tips_black_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagtips::indicator:checked {\n"
"    image: url(file:///../UI/images/tag_tips_color_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagtips::indicator:hover {\n"
"	width:45px;\n"
"	height:45px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagsummer::indicator:unchecked {\n"
"    image: url(file:///../UI/images/tag_ete_black_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagsummer::indicator:checked {\n"
"    image: url(file:///../UI/images/tag_ete_color_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagsummer::indicator:hover {\n"
"	width:45px;\n"
"	height:45px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagwinter::indicator:unchecked {\n"
"    image: url(file:///../UI/images/tag_hiver_bla"
                        "ck_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagwinter::indicator:checked {\n"
"    image: url(file:///../UI/images/tag_hiver_color_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagwinter::indicator:hover {\n"
"	width:45px;\n"
"	height:45px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagdessert::indicator:unchecked {\n"
"    image: url(file:///../UI/images/tag_dessert_black_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagdessert::indicator:checked {\n"
"    image: url(file:///../UI/images/tag_dessert_color_LD.png);\n"
"	width:50px;\n"
"	height:50px;\n"
"}\n"
"\n"
"QCheckBox#cB_tagdessert::indicator:hover {\n"
"	width:45px;\n"
"	height:45px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        font1 = QFont()
        font1.setFamily(u"Poiret One")
        font1.setPointSize(26)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setWeight(75)
        self.tabWidget.setFont(font1)
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setIconSize(QSize(50, 50))
        self.tab_menus = QWidget()
        self.tab_menus.setObjectName(u"tab_menus")
        self.gridLayout_3 = QGridLayout(self.tab_menus)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.toolBox = QToolBox(self.tab_menus)
        self.toolBox.setObjectName(u"toolBox")
        font2 = QFont()
        font2.setFamily(u"Poiret One")
        font2.setPointSize(18)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(75)
        self.toolBox.setFont(font2)
        self.toolBox.setStyleSheet(u"QToolBox {\n"
"icon-size: 40px;\n"
"}")
        self.toolBox.setFrameShape(QFrame.NoFrame)
        self.page_carte = QWidget()
        self.page_carte.setObjectName(u"page_carte")
        self.page_carte.setGeometry(QRect(0, 0, 1135, 599))
        self.gridLayout_9 = QGridLayout(self.page_carte)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.frame_carte = QFrame(self.page_carte)
        self.frame_carte.setObjectName(u"frame_carte")
        self.frame_carte.setFrameShape(QFrame.NoFrame)
        self.frame_carte.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_carte)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.tW_menu = QTableWidget(self.frame_carte)
        if (self.tW_menu.rowCount() < 3):
            self.tW_menu.setRowCount(3)
        font3 = QFont()
        font3.setFamily(u"Poiret One")
        font3.setBold(True)
        font3.setWeight(75)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem.setFont(font3);
        self.tW_menu.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem1.setFont(font3);
        self.tW_menu.setVerticalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.tW_menu.setVerticalHeaderItem(2, __qtablewidgetitem2)
        self.tW_menu.setObjectName(u"tW_menu")
        font4 = QFont()
        font4.setFamily(u"Poiret One")
        font4.setPointSize(13)
        font4.setBold(True)
        font4.setItalic(False)
        font4.setWeight(75)
        self.tW_menu.setFont(font4)
        self.tW_menu.setMouseTracking(True)
        self.tW_menu.setFrameShape(QFrame.NoFrame)
        self.tW_menu.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.EditKeyPressed)
        self.tW_menu.setDragEnabled(True)
        self.tW_menu.setDragDropOverwriteMode(False)
        self.tW_menu.setDragDropMode(QAbstractItemView.InternalMove)
        self.tW_menu.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tW_menu.setIconSize(QSize(60, 60))
        self.tW_menu.setTextElideMode(Qt.ElideMiddle)

        self.gridLayout_10.addWidget(self.tW_menu, 1, 0, 1, 1)

        self.frame_2 = QFrame(self.frame_carte)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.cB_restes_2 = QCheckBox(self.frame_2)
        self.cB_restes_2.setObjectName(u"cB_restes_2")
        font5 = QFont()
        font5.setFamily(u"Poiret One")
        font5.setPointSize(14)
        font5.setBold(True)
        font5.setItalic(False)
        font5.setWeight(75)
        self.cB_restes_2.setFont(font5)
        self.cB_restes_2.setChecked(True)

        self.gridLayout_13.addWidget(self.cB_restes_2, 0, 5, 1, 1)

        self.label_dessert = QLabel(self.frame_2)
        self.label_dessert.setObjectName(u"label_dessert")
        self.label_dessert.setFont(font5)
        self.label_dessert.setPixmap(QPixmap(u"images/icon_cupcake_t.png"))

        self.gridLayout_13.addWidget(self.label_dessert, 0, 6, 1, 1)

        self.pB_new_menu_2 = QPushButton(self.frame_2)
        self.pB_new_menu_2.setObjectName(u"pB_new_menu_2")
        font6 = QFont()
        font6.setFamily(u"Poiret One")
        font6.setBold(True)
        font6.setItalic(False)
        font6.setWeight(75)
        self.pB_new_menu_2.setFont(font6)
        self.pB_new_menu_2.setIconSize(QSize(40, 40))

        self.gridLayout_13.addWidget(self.pB_new_menu_2, 0, 0, 1, 1)

        self.dateEdit_2 = QDateEdit(self.frame_2)
        self.dateEdit_2.setObjectName(u"dateEdit_2")
        self.dateEdit_2.setMinimumSize(QSize(170, 50))
        self.dateEdit_2.setFont(font6)
        self.dateEdit_2.setStyleSheet(u"")
        self.dateEdit_2.setWrapping(True)
        self.dateEdit_2.setAlignment(Qt.AlignCenter)
        self.dateEdit_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.dateEdit_2.setCalendarPopup(True)

        self.gridLayout_13.addWidget(self.dateEdit_2, 0, 2, 1, 1)

        self.label_date = QLabel(self.frame_2)
        self.label_date.setObjectName(u"label_date")
        self.label_date.setPixmap(QPixmap(u"images/icon_date_3colors_t_LD.png"))
        self.label_date.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout_13.addWidget(self.label_date, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_3, 0, 10, 1, 1)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font5)

        self.gridLayout_13.addWidget(self.label_9, 0, 3, 1, 1)

        self.sB_days_2 = QSpinBox(self.frame_2)
        self.sB_days_2.setObjectName(u"sB_days_2")
        self.sB_days_2.setMinimumSize(QSize(0, 50))
        self.sB_days_2.setFont(font6)
        self.sB_days_2.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.sB_days_2.setValue(7)

        self.gridLayout_13.addWidget(self.sB_days_2, 0, 4, 1, 1)

        self.sB_desserts_2 = QSpinBox(self.frame_2)
        self.sB_desserts_2.setObjectName(u"sB_desserts_2")
        self.sB_desserts_2.setMinimumSize(QSize(0, 50))
        self.sB_desserts_2.setFont(font6)
        self.sB_desserts_2.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout_13.addWidget(self.sB_desserts_2, 0, 7, 1, 1)

        self.pB_modif = QPushButton(self.frame_2)
        self.pB_modif.setObjectName(u"pB_modif")
        self.pB_modif.setFont(font6)
        self.pB_modif.setIconSize(QSize(40, 40))
        self.pB_modif.setCheckable(True)

        self.gridLayout_13.addWidget(self.pB_modif, 0, 11, 1, 1)


        self.gridLayout_10.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_button_2 = QFrame(self.frame_carte)
        self.frame_button_2.setObjectName(u"frame_button_2")
        self.frame_button_2.setFrameShape(QFrame.NoFrame)
        self.frame_button_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_button_2)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.pB_save = QPushButton(self.frame_button_2)
        self.pB_save.setObjectName(u"pB_save")
        self.pB_save.setFont(font6)
        self.pB_save.setIconSize(QSize(40, 40))

        self.gridLayout_14.addWidget(self.pB_save, 0, 3, 1, 1)

        self.frame_score = QFrame(self.frame_button_2)
        self.frame_score.setObjectName(u"frame_score")
        self.frame_score.setFrameShape(QFrame.NoFrame)
        self.frame_score.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_score)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_s_vegan = QLabel(self.frame_score)
        self.label_s_vegan.setObjectName(u"label_s_vegan")

        self.gridLayout_11.addWidget(self.label_s_vegan, 0, 2, 1, 1)

        self.label_s_hiver = QLabel(self.frame_score)
        self.label_s_hiver.setObjectName(u"label_s_hiver")

        self.gridLayout_11.addWidget(self.label_s_hiver, 0, 4, 1, 1)

        self.label_s_ete = QLabel(self.frame_score)
        self.label_s_ete.setObjectName(u"label_s_ete")

        self.gridLayout_11.addWidget(self.label_s_ete, 0, 3, 1, 1)

        self.label_s_double = QLabel(self.frame_score)
        self.label_s_double.setObjectName(u"label_s_double")

        self.gridLayout_11.addWidget(self.label_s_double, 0, 0, 1, 1)

        self.label_s_kids = QLabel(self.frame_score)
        self.label_s_kids.setObjectName(u"label_s_kids")

        self.gridLayout_11.addWidget(self.label_s_kids, 0, 1, 1, 1)


        self.gridLayout_14.addWidget(self.frame_score, 0, 1, 1, 1, Qt.AlignHCenter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.frame_button_2, 2, 0, 1, 2)


        self.gridLayout_9.addWidget(self.frame_carte, 0, 0, 1, 1)

        self.toolBox.addItem(self.page_carte, u"Carte")
        self.page_liste = QWidget()
        self.page_liste.setObjectName(u"page_liste")
        self.page_liste.setGeometry(QRect(0, 0, 407, 177))
        self.gridLayout_21 = QGridLayout(self.page_liste)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.frame_liste_courses = QFrame(self.page_liste)
        self.frame_liste_courses.setObjectName(u"frame_liste_courses")
        self.frame_liste_courses.setFrameShape(QFrame.NoFrame)
        self.frame_liste_courses.setFrameShadow(QFrame.Raised)
        self.gridLayout_22 = QGridLayout(self.frame_liste_courses)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.frame_shopping = QFrame(self.frame_liste_courses)
        self.frame_shopping.setObjectName(u"frame_shopping")
        self.frame_shopping.setFrameShape(QFrame.NoFrame)
        self.frame_shopping.setFrameShadow(QFrame.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_shopping)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.frame_bottom = QFrame(self.frame_shopping)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setFrameShape(QFrame.StyledPanel)
        self.frame_bottom.setFrameShadow(QFrame.Raised)
        self.gridLayout_24 = QGridLayout(self.frame_bottom)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.lW_courses = QListWidget(self.frame_bottom)
        self.lW_courses.setObjectName(u"lW_courses")
        self.lW_courses.setFont(font4)
        self.lW_courses.setFrameShape(QFrame.NoFrame)

        self.gridLayout_24.addWidget(self.lW_courses, 0, 0, 1, 4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_24.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.pB_send = QPushButton(self.frame_bottom)
        self.pB_send.setObjectName(u"pB_send")
        self.pB_send.setIconSize(QSize(40, 40))

        self.gridLayout_24.addWidget(self.pB_send, 1, 2, 1, 1)

        self.pB_print = QPushButton(self.frame_bottom)
        self.pB_print.setObjectName(u"pB_print")
        self.pB_print.setIconSize(QSize(40, 40))

        self.gridLayout_24.addWidget(self.pB_print, 1, 3, 1, 1)

        self.pB_copy = QPushButton(self.frame_bottom)
        self.pB_copy.setObjectName(u"pB_copy")
        self.pB_copy.setIconSize(QSize(40, 40))

        self.gridLayout_24.addWidget(self.pB_copy, 1, 1, 1, 1)


        self.gridLayout_19.addWidget(self.frame_bottom, 1, 0, 1, 1)

        self.label_top = QLabel(self.frame_shopping)
        self.label_top.setObjectName(u"label_top")
        self.label_top.setAlignment(Qt.AlignCenter)

        self.gridLayout_19.addWidget(self.label_top, 0, 0, 1, 1)


        self.gridLayout_22.addWidget(self.frame_shopping, 0, 0, 1, 1)

        self.frame_menus = QFrame(self.frame_liste_courses)
        self.frame_menus.setObjectName(u"frame_menus")
        self.frame_menus.setFrameShape(QFrame.NoFrame)
        self.frame_menus.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_menus)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.lW_menu = QListWidget(self.frame_menus)
        self.lW_menu.setObjectName(u"lW_menu")
        self.lW_menu.setFont(font4)
        self.lW_menu.setFrameShape(QFrame.NoFrame)
        self.lW_menu.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lW_menu.setSelectionMode(QAbstractItemView.NoSelection)
        self.lW_menu.setSpacing(6)
        self.lW_menu.setWordWrap(True)
        self.lW_menu.setItemAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lW_menu, 1, 0, 1, 1)

        self.label_icon_carte = QLabel(self.frame_menus)
        self.label_icon_carte.setObjectName(u"label_icon_carte")
        self.label_icon_carte.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.label_icon_carte, 0, 0, 1, 1)


        self.gridLayout_22.addWidget(self.frame_menus, 0, 2, 1, 1)

        self.label_cocktail = QLabel(self.frame_liste_courses)
        self.label_cocktail.setObjectName(u"label_cocktail")

        self.gridLayout_22.addWidget(self.label_cocktail, 0, 1, 1, 1)


        self.gridLayout_21.addWidget(self.frame_liste_courses, 0, 0, 1, 1)

        self.toolBox.addItem(self.page_liste, u"Liste de courses")

        self.gridLayout_3.addWidget(self.toolBox, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_menus, "")
        self.tab_recettes = QWidget()
        self.tab_recettes.setObjectName(u"tab_recettes")
        self.gridLayout_6 = QGridLayout(self.tab_recettes)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.frame_searchedit = QFrame(self.tab_recettes)
        self.frame_searchedit.setObjectName(u"frame_searchedit")
        self.frame_searchedit.setFrameShape(QFrame.NoFrame)
        self.frame_searchedit.setFrameShadow(QFrame.Raised)
        self.gridLayout_27 = QGridLayout(self.frame_searchedit)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_27.addItem(self.horizontalSpacer_11, 0, 1, 1, 1)

        self.pB_new_recipe = QPushButton(self.frame_searchedit)
        self.pB_new_recipe.setObjectName(u"pB_new_recipe")
        self.pB_new_recipe.setIconSize(QSize(40, 40))
        self.pB_new_recipe.setCheckable(True)

        self.gridLayout_27.addWidget(self.pB_new_recipe, 0, 4, 1, 1)

        self.cB_recherche = QCheckBox(self.frame_searchedit)
        self.cB_recherche.setObjectName(u"cB_recherche")
        self.cB_recherche.setFont(font5)

        self.gridLayout_27.addWidget(self.cB_recherche, 0, 0, 1, 1)

        self.pB_modif_2 = QPushButton(self.frame_searchedit)
        self.pB_modif_2.setObjectName(u"pB_modif_2")
        self.pB_modif_2.setIconSize(QSize(40, 40))
        self.pB_modif_2.setCheckable(True)

        self.gridLayout_27.addWidget(self.pB_modif_2, 0, 3, 1, 1)

        self.pB_delete = QPushButton(self.frame_searchedit)
        self.pB_delete.setObjectName(u"pB_delete")
        self.pB_delete.setIconSize(QSize(40, 40))

        self.gridLayout_27.addWidget(self.pB_delete, 0, 2, 1, 1)


        self.gridLayout_6.addWidget(self.frame_searchedit, 2, 0, 1, 1)

        self.frame_recettes = QFrame(self.tab_recettes)
        self.frame_recettes.setObjectName(u"frame_recettes")
        self.frame_recettes.setFrameShape(QFrame.NoFrame)
        self.frame_recettes.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_recettes)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.frame_edit_recipe = QFrame(self.frame_recettes)
        self.frame_edit_recipe.setObjectName(u"frame_edit_recipe")
        self.frame_edit_recipe.setFrameShape(QFrame.NoFrame)
        self.frame_edit_recipe.setFrameShadow(QFrame.Raised)
        self.gridLayout_31 = QGridLayout(self.frame_edit_recipe)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.frame_new_recipe = QFrame(self.frame_edit_recipe)
        self.frame_new_recipe.setObjectName(u"frame_new_recipe")
        self.frame_new_recipe.setFrameShape(QFrame.NoFrame)
        self.frame_new_recipe.setFrameShadow(QFrame.Raised)
        self.gridLayout_28 = QGridLayout(self.frame_new_recipe)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.label_newedit = QLabel(self.frame_new_recipe)
        self.label_newedit.setObjectName(u"label_newedit")
        font7 = QFont()
        font7.setFamily(u"Poiret One")
        font7.setPointSize(16)
        font7.setBold(True)
        font7.setItalic(False)
        font7.setWeight(75)
        self.label_newedit.setFont(font7)
        self.label_newedit.setAlignment(Qt.AlignCenter)

        self.gridLayout_28.addWidget(self.label_newedit, 0, 0, 1, 3)

        self.frame_8 = QFrame(self.frame_new_recipe)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_30 = QGridLayout(self.frame_8)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_12, 0, 0, 1, 1)

        self.pB_cancel_2 = QPushButton(self.frame_8)
        self.pB_cancel_2.setObjectName(u"pB_cancel_2")
        self.pB_cancel_2.setIconSize(QSize(40, 40))

        self.gridLayout_30.addWidget(self.pB_cancel_2, 0, 1, 1, 1)

        self.pB_ok_2 = QPushButton(self.frame_8)
        self.pB_ok_2.setObjectName(u"pB_ok_2")
        self.pB_ok_2.setIconSize(QSize(40, 40))

        self.gridLayout_30.addWidget(self.pB_ok_2, 0, 2, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_13, 0, 3, 1, 1)


        self.gridLayout_28.addWidget(self.frame_8, 7, 0, 1, 4)

        self.frame_7 = QFrame(self.frame_new_recipe)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_34 = QGridLayout(self.frame_7)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.frame_ingredients = QFrame(self.frame_7)
        self.frame_ingredients.setObjectName(u"frame_ingredients")
        self.frame_ingredients.setFrameShape(QFrame.NoFrame)
        self.frame_ingredients.setFrameShadow(QFrame.Raised)
        self.gridLayout_36 = QGridLayout(self.frame_ingredients)
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.frame_add_ingredient = QFrame(self.frame_ingredients)
        self.frame_add_ingredient.setObjectName(u"frame_add_ingredient")
        self.frame_add_ingredient.setFrameShape(QFrame.StyledPanel)
        self.frame_add_ingredient.setFrameShadow(QFrame.Raised)
        self.gridLayout_37 = QGridLayout(self.frame_add_ingredient)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.label_8 = QLabel(self.frame_add_ingredient)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_37.addWidget(self.label_8, 0, 4, 1, 1)

        self.pB_option = QPushButton(self.frame_add_ingredient)
        self.pB_option.setObjectName(u"pB_option")
        self.pB_option.setMaximumSize(QSize(30, 30))
        self.pB_option.setCheckable(True)

        self.gridLayout_37.addWidget(self.pB_option, 0, 1, 1, 1)

        self.lE_qty = QLineEdit(self.frame_add_ingredient)
        self.lE_qty.setObjectName(u"lE_qty")
        self.lE_qty.setAlignment(Qt.AlignCenter)

        self.gridLayout_37.addWidget(self.lE_qty, 0, 5, 1, 1)

        self.pB_add = QPushButton(self.frame_add_ingredient)
        self.pB_add.setObjectName(u"pB_add")
        self.pB_add.setMaximumSize(QSize(30, 30))

        self.gridLayout_37.addWidget(self.pB_add, 0, 8, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.cB_ingredient = QComboBox(self.frame_add_ingredient)
        self.cB_ingredient.setObjectName(u"cB_ingredient")
        self.cB_ingredient.setEditable(True)

        self.gridLayout_37.addWidget(self.cB_ingredient, 0, 2, 1, 1)

        self.label = QLabel(self.frame_add_ingredient)
        self.label.setObjectName(u"label")

        self.gridLayout_37.addWidget(self.label, 0, 0, 1, 1)

        self.cB_unit = QComboBox(self.frame_add_ingredient)
        self.cB_unit.setObjectName(u"cB_unit")
        self.cB_unit.setEditable(True)

        self.gridLayout_37.addWidget(self.cB_unit, 0, 6, 1, 1)

        self.pB_option_2 = QPushButton(self.frame_add_ingredient)
        self.pB_option_2.setObjectName(u"pB_option_2")
        self.pB_option_2.setMaximumSize(QSize(30, 30))
        self.pB_option_2.setCheckable(True)

        self.gridLayout_37.addWidget(self.pB_option_2, 0, 3, 1, 1)


        self.gridLayout_36.addWidget(self.frame_add_ingredient, 1, 0, 1, 1, Qt.AlignTop)

        self.tW_ingredients = QTableWidget(self.frame_ingredients)
        self.tW_ingredients.setObjectName(u"tW_ingredients")
        self.tW_ingredients.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tW_ingredients.setSelectionMode(QAbstractItemView.NoSelection)
        self.tW_ingredients.setIconSize(QSize(18, 18))
        self.tW_ingredients.setShowGrid(False)
        self.tW_ingredients.horizontalHeader().setVisible(False)
        self.tW_ingredients.verticalHeader().setVisible(False)

        self.gridLayout_36.addWidget(self.tW_ingredients, 0, 0, 1, 1)


        self.gridLayout_34.addWidget(self.frame_ingredients, 2, 0, 1, 3, Qt.AlignTop)

        self.label_2 = QLabel(self.frame_7)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font7)

        self.gridLayout_34.addWidget(self.label_2, 1, 0, 1, 3, Qt.AlignBottom)

        self.pB_photo = QPushButton(self.frame_7)
        self.pB_photo.setObjectName(u"pB_photo")
        self.pB_photo.setIconSize(QSize(40, 40))

        self.gridLayout_34.addWidget(self.pB_photo, 0, 2, 1, 1, Qt.AlignLeft)

        self.label_image_2 = QLabel(self.frame_7)
        self.label_image_2.setObjectName(u"label_image_2")

        self.gridLayout_34.addWidget(self.label_image_2, 0, 0, 1, 2, Qt.AlignHCenter)

        self.label_10 = QLabel(self.frame_7)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_34.addWidget(self.label_10, 3, 0, 1, 1, Qt.AlignRight)

        self.sB_time = QSpinBox(self.frame_7)
        self.sB_time.setObjectName(u"sB_time")
        self.sB_time.setAlignment(Qt.AlignCenter)
        self.sB_time.setMaximum(1000)
        self.sB_time.setSingleStep(5)

        self.gridLayout_34.addWidget(self.sB_time, 3, 1, 1, 1)

        self.label_11 = QLabel(self.frame_7)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_34.addWidget(self.label_11, 3, 2, 1, 1, Qt.AlignLeft)


        self.gridLayout_28.addWidget(self.frame_7, 4, 0, 1, 1)

        self.frame_10 = QFrame(self.frame_new_recipe)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_35 = QGridLayout(self.frame_10)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.tB_preparation = QTextBrowser(self.frame_10)
        self.tB_preparation.setObjectName(u"tB_preparation")
        self.tB_preparation.setFrameShape(QFrame.NoFrame)
        self.tB_preparation.setReadOnly(False)

        self.gridLayout_35.addWidget(self.tB_preparation, 1, 0, 1, 1)

        self.label_7 = QLabel(self.frame_10)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font7)

        self.gridLayout_35.addWidget(self.label_7, 0, 0, 1, 1)


        self.gridLayout_28.addWidget(self.frame_10, 4, 1, 1, 2)

        self.lE_titre = QLineEdit(self.frame_new_recipe)
        self.lE_titre.setObjectName(u"lE_titre")
        font8 = QFont()
        font8.setFamily(u"Poiret One")
        font8.setPointSize(20)
        font8.setBold(True)
        font8.setItalic(False)
        font8.setWeight(75)
        self.lE_titre.setFont(font8)

        self.gridLayout_28.addWidget(self.lE_titre, 1, 0, 1, 3)

        self.frame_tags_2 = QFrame(self.frame_new_recipe)
        self.frame_tags_2.setObjectName(u"frame_tags_2")
        self.frame_tags_2.setFrameShape(QFrame.StyledPanel)
        self.frame_tags_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_29 = QGridLayout(self.frame_tags_2)
        self.gridLayout_29.setSpacing(3)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.cB_tagvegan = QCheckBox(self.frame_tags_2)
        self.cB_tagvegan.setObjectName(u"cB_tagvegan")

        self.gridLayout_29.addWidget(self.cB_tagvegan, 2, 3, 1, 1)

        self.cB_tagwinter = QCheckBox(self.frame_tags_2)
        self.cB_tagwinter.setObjectName(u"cB_tagwinter")

        self.gridLayout_29.addWidget(self.cB_tagwinter, 2, 5, 1, 1)

        self.cB_tagkids = QCheckBox(self.frame_tags_2)
        self.cB_tagkids.setObjectName(u"cB_tagkids")

        self.gridLayout_29.addWidget(self.cB_tagkids, 2, 2, 1, 1)

        self.cB_tagdinner = QCheckBox(self.frame_tags_2)
        self.cB_tagdinner.setObjectName(u"cB_tagdinner")

        self.gridLayout_29.addWidget(self.cB_tagdinner, 2, 8, 1, 1)

        self.cB_tagsummer = QCheckBox(self.frame_tags_2)
        self.cB_tagsummer.setObjectName(u"cB_tagsummer")

        self.gridLayout_29.addWidget(self.cB_tagsummer, 2, 4, 1, 1)

        self.cB_tagdouble = QCheckBox(self.frame_tags_2)
        self.cB_tagdouble.setObjectName(u"cB_tagdouble")

        self.gridLayout_29.addWidget(self.cB_tagdouble, 2, 1, 1, 1)

        self.cB_tagdessert = QCheckBox(self.frame_tags_2)
        self.cB_tagdessert.setObjectName(u"cB_tagdessert")

        self.gridLayout_29.addWidget(self.cB_tagdessert, 2, 6, 1, 1)

        self.cB_taglunch = QCheckBox(self.frame_tags_2)
        self.cB_taglunch.setObjectName(u"cB_taglunch")

        self.gridLayout_29.addWidget(self.cB_taglunch, 2, 7, 1, 1)

        self.cB_tagtips = QCheckBox(self.frame_tags_2)
        self.cB_tagtips.setObjectName(u"cB_tagtips")

        self.gridLayout_29.addWidget(self.cB_tagtips, 2, 9, 1, 1)


        self.gridLayout_28.addWidget(self.frame_tags_2, 6, 0, 1, 3, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_31.addWidget(self.frame_new_recipe, 0, 1, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_14, 0, 0, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_15, 0, 2, 1, 1)


        self.gridLayout_7.addWidget(self.frame_edit_recipe, 0, 2, 1, 1)

        self.frame_details = QFrame(self.frame_recettes)
        self.frame_details.setObjectName(u"frame_details")
        self.frame_details.setFrameShape(QFrame.NoFrame)
        self.frame_details.setFrameShadow(QFrame.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_details)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.frame_9 = QFrame(self.frame_details)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_33 = QGridLayout(self.frame_9)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.label_6 = QLabel(self.frame_9)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font7)

        self.gridLayout_33.addWidget(self.label_6, 1, 0, 1, 1)

        self.tE_recette = QTextEdit(self.frame_9)
        self.tE_recette.setObjectName(u"tE_recette")
        self.tE_recette.setFrameShape(QFrame.NoFrame)
        self.tE_recette.setReadOnly(True)

        self.gridLayout_33.addWidget(self.tE_recette, 2, 0, 1, 1)

        self.frame_tags = QFrame(self.frame_9)
        self.frame_tags.setObjectName(u"frame_tags")
        self.frame_tags.setFrameShape(QFrame.NoFrame)
        self.frame_tags.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_tags)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_summer = QLabel(self.frame_tags)
        self.label_summer.setObjectName(u"label_summer")

        self.gridLayout_8.addWidget(self.label_summer, 1, 0, 1, 1)

        self.label_dessert_2 = QLabel(self.frame_tags)
        self.label_dessert_2.setObjectName(u"label_dessert_2")

        self.gridLayout_8.addWidget(self.label_dessert_2, 1, 2, 1, 1)

        self.label_winter = QLabel(self.frame_tags)
        self.label_winter.setObjectName(u"label_winter")

        self.gridLayout_8.addWidget(self.label_winter, 1, 1, 1, 1)

        self.label_double = QLabel(self.frame_tags)
        self.label_double.setObjectName(u"label_double")

        self.gridLayout_8.addWidget(self.label_double, 0, 0, 1, 1)

        self.label_tips = QLabel(self.frame_tags)
        self.label_tips.setObjectName(u"label_tips")

        self.gridLayout_8.addWidget(self.label_tips, 1, 3, 1, 1)

        self.label_kids = QLabel(self.frame_tags)
        self.label_kids.setObjectName(u"label_kids")

        self.gridLayout_8.addWidget(self.label_kids, 0, 1, 1, 1)

        self.label_lunchdinner = QLabel(self.frame_tags)
        self.label_lunchdinner.setObjectName(u"label_lunchdinner")

        self.gridLayout_8.addWidget(self.label_lunchdinner, 0, 2, 1, 1)

        self.label_vegan = QLabel(self.frame_tags)
        self.label_vegan.setObjectName(u"label_vegan")

        self.gridLayout_8.addWidget(self.label_vegan, 0, 3, 1, 1)


        self.gridLayout_33.addWidget(self.frame_tags, 0, 0, 1, 1, Qt.AlignHCenter)


        self.gridLayout_20.addWidget(self.frame_9, 0, 1, 6, 1)

        self.frame_4 = QFrame(self.frame_details)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_26 = QGridLayout(self.frame_4)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.pB_back = QPushButton(self.frame_4)
        self.pB_back.setObjectName(u"pB_back")
        self.pB_back.setIconSize(QSize(40, 40))

        self.gridLayout_26.addWidget(self.pB_back, 0, 1, 1, 1, Qt.AlignLeft)

        self.pB_send_2 = QPushButton(self.frame_4)
        self.pB_send_2.setObjectName(u"pB_send_2")
        self.pB_send_2.setIconSize(QSize(40, 40))

        self.gridLayout_26.addWidget(self.pB_send_2, 0, 2, 1, 1, Qt.AlignLeft)

        self.pB_print_2 = QPushButton(self.frame_4)
        self.pB_print_2.setObjectName(u"pB_print_2")
        self.pB_print_2.setIconSize(QSize(40, 40))

        self.gridLayout_26.addWidget(self.pB_print_2, 0, 3, 1, 1, Qt.AlignLeft)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_26.addItem(self.horizontalSpacer_10, 0, 0, 1, 1)


        self.gridLayout_20.addWidget(self.frame_4, 6, 1, 1, 1)

        self.frame_6 = QFrame(self.frame_details)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_32 = QGridLayout(self.frame_6)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.label_titre = QLabel(self.frame_6)
        self.label_titre.setObjectName(u"label_titre")
        self.label_titre.setFont(font8)
        self.label_titre.setAlignment(Qt.AlignCenter)
        self.label_titre.setWordWrap(True)
        self.label_titre.setMargin(3)

        self.gridLayout_32.addWidget(self.label_titre, 0, 0, 1, 1)

        self.label_image = QLabel(self.frame_6)
        self.label_image.setObjectName(u"label_image")

        self.gridLayout_32.addWidget(self.label_image, 1, 0, 1, 1, Qt.AlignHCenter)

        self.label_5 = QLabel(self.frame_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font7)

        self.gridLayout_32.addWidget(self.label_5, 2, 0, 1, 1)

        self.tE_ingredients = QTextBrowser(self.frame_6)
        self.tE_ingredients.setObjectName(u"tE_ingredients")
        self.tE_ingredients.setFrameShape(QFrame.NoFrame)
        self.tE_ingredients.setReadOnly(True)
        self.tE_ingredients.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.tE_ingredients.setOpenExternalLinks(True)

        self.gridLayout_32.addWidget(self.tE_ingredients, 3, 0, 1, 1)


        self.gridLayout_20.addWidget(self.frame_6, 0, 0, 7, 1)


        self.gridLayout_7.addWidget(self.frame_details, 0, 1, 1, 1)

        self.lW_recettes = QListWidget(self.frame_recettes)
        self.lW_recettes.setObjectName(u"lW_recettes")
        self.lW_recettes.setFont(font4)
        self.lW_recettes.setFrameShape(QFrame.NoFrame)
        self.lW_recettes.setAlternatingRowColors(True)
        self.lW_recettes.setWordWrap(True)
        self.lW_recettes.setSortingEnabled(True)

        self.gridLayout_7.addWidget(self.lW_recettes, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_recettes, 1, 0, 1, 1)

        self.frame_recherche = QFrame(self.tab_recettes)
        self.frame_recherche.setObjectName(u"frame_recherche")
        self.frame_recherche.setFont(font5)
        self.frame_recherche.setFrameShape(QFrame.NoFrame)
        self.frame_recherche.setFrameShadow(QFrame.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_recherche)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.label_4 = QLabel(self.frame_recherche)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_18.addWidget(self.label_4, 3, 0, 1, 1)

        self.lE_without = QLineEdit(self.frame_recherche)
        self.lE_without.setObjectName(u"lE_without")

        self.gridLayout_18.addWidget(self.lE_without, 3, 1, 1, 1)

        self.label_3 = QLabel(self.frame_recherche)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_18.addWidget(self.label_3, 2, 0, 1, 1)

        self.pB_filter = QPushButton(self.frame_recherche)
        self.pB_filter.setObjectName(u"pB_filter")
        self.pB_filter.setMaximumSize(QSize(90, 90))
        self.pB_filter.setIconSize(QSize(50, 50))
        self.pB_filter.setCheckable(True)
        self.pB_filter.setChecked(False)

        self.gridLayout_18.addWidget(self.pB_filter, 2, 2, 2, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.lE_with = QLineEdit(self.frame_recherche)
        self.lE_with.setObjectName(u"lE_with")

        self.gridLayout_18.addWidget(self.lE_with, 2, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_8, 3, 3, 1, 1)


        self.gridLayout_6.addWidget(self.frame_recherche, 4, 0, 1, 1)

        self.tabWidget.addTab(self.tab_recettes, "")
        self.tab_historique = QWidget()
        self.tab_historique.setObjectName(u"tab_historique")
        self.gridLayout_4 = QGridLayout(self.tab_historique)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_historique = QFrame(self.tab_historique)
        self.frame_historique.setObjectName(u"frame_historique")
        self.frame_historique.setFrameShape(QFrame.NoFrame)
        self.frame_historique.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_historique)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.frame_deco = QFrame(self.frame_historique)
        self.frame_deco.setObjectName(u"frame_deco")
        self.frame_deco.setFrameShape(QFrame.NoFrame)
        self.frame_deco.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_deco)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.label_deco_1 = QLabel(self.frame_deco)
        self.label_deco_1.setObjectName(u"label_deco_1")

        self.gridLayout_12.addWidget(self.label_deco_1, 0, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.label_deco_8 = QLabel(self.frame_deco)
        self.label_deco_8.setObjectName(u"label_deco_8")

        self.gridLayout_12.addWidget(self.label_deco_8, 0, 8, 1, 1)

        self.label_deco_2 = QLabel(self.frame_deco)
        self.label_deco_2.setObjectName(u"label_deco_2")

        self.gridLayout_12.addWidget(self.label_deco_2, 0, 2, 1, 1)

        self.label_deco_3 = QLabel(self.frame_deco)
        self.label_deco_3.setObjectName(u"label_deco_3")

        self.gridLayout_12.addWidget(self.label_deco_3, 0, 3, 1, 1)

        self.label_deco_7 = QLabel(self.frame_deco)
        self.label_deco_7.setObjectName(u"label_deco_7")

        self.gridLayout_12.addWidget(self.label_deco_7, 0, 7, 1, 1)

        self.label_deco_5 = QLabel(self.frame_deco)
        self.label_deco_5.setObjectName(u"label_deco_5")

        self.gridLayout_12.addWidget(self.label_deco_5, 0, 5, 1, 1)

        self.label_deco_6 = QLabel(self.frame_deco)
        self.label_deco_6.setObjectName(u"label_deco_6")

        self.gridLayout_12.addWidget(self.label_deco_6, 0, 6, 1, 1)


        self.gridLayout_5.addWidget(self.frame_deco, 0, 0, 1, 2)

        self.frame_deco_2 = QFrame(self.frame_historique)
        self.frame_deco_2.setObjectName(u"frame_deco_2")
        self.frame_deco_2.setFrameShape(QFrame.NoFrame)
        self.frame_deco_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_deco_2)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.label_deco_11 = QLabel(self.frame_deco_2)
        self.label_deco_11.setObjectName(u"label_deco_11")

        self.gridLayout_16.addWidget(self.label_deco_11, 2, 0, 1, 1)

        self.label_deco_12 = QLabel(self.frame_deco_2)
        self.label_deco_12.setObjectName(u"label_deco_12")

        self.gridLayout_16.addWidget(self.label_deco_12, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_16.addItem(self.verticalSpacer, 10, 0, 1, 1)

        self.label_deco_13 = QLabel(self.frame_deco_2)
        self.label_deco_13.setObjectName(u"label_deco_13")

        self.gridLayout_16.addWidget(self.label_deco_13, 4, 0, 1, 1)

        self.label_deco_15 = QLabel(self.frame_deco_2)
        self.label_deco_15.setObjectName(u"label_deco_15")

        self.gridLayout_16.addWidget(self.label_deco_15, 7, 0, 1, 1)

        self.label_deco_10 = QLabel(self.frame_deco_2)
        self.label_deco_10.setObjectName(u"label_deco_10")

        self.gridLayout_16.addWidget(self.label_deco_10, 1, 0, 1, 1)

        self.label_deco_14 = QLabel(self.frame_deco_2)
        self.label_deco_14.setObjectName(u"label_deco_14")

        self.gridLayout_16.addWidget(self.label_deco_14, 5, 0, 1, 1)

        self.label_deco_4 = QLabel(self.frame_deco_2)
        self.label_deco_4.setObjectName(u"label_deco_4")

        self.gridLayout_16.addWidget(self.label_deco_4, 6, 0, 1, 1)

        self.label_deco_16 = QLabel(self.frame_deco_2)
        self.label_deco_16.setObjectName(u"label_deco_16")

        self.gridLayout_16.addWidget(self.label_deco_16, 8, 0, 1, 1)

        self.label_deco_9 = QLabel(self.frame_deco_2)
        self.label_deco_9.setObjectName(u"label_deco_9")

        self.gridLayout_16.addWidget(self.label_deco_9, 9, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_deco_2, 0, 2, 3, 1)

        self.frame_table = QFrame(self.frame_historique)
        self.frame_table.setObjectName(u"frame_table")
        self.frame_table.setFrameShape(QFrame.NoFrame)
        self.frame_table.setFrameShadow(QFrame.Raised)
        self.gridLayout_23 = QGridLayout(self.frame_table)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.tW_historique = QTableWidget(self.frame_table)
        self.tW_historique.setObjectName(u"tW_historique")
        self.tW_historique.setFont(font4)
        self.tW_historique.setFrameShape(QFrame.NoFrame)
        self.tW_historique.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tW_historique.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tW_historique.setAlternatingRowColors(True)
        self.tW_historique.setSortingEnabled(False)

        self.gridLayout_23.addWidget(self.tW_historique, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_table, 1, 0, 1, 2)

        self.frame_3 = QFrame(self.frame_historique)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_25 = QGridLayout(self.frame_3)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.frame_confirm = QFrame(self.frame_3)
        self.frame_confirm.setObjectName(u"frame_confirm")
        self.frame_confirm.setFrameShape(QFrame.NoFrame)
        self.frame_confirm.setFrameShadow(QFrame.Raised)
        self.gridLayout_17 = QGridLayout(self.frame_confirm)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.pB_ok = QPushButton(self.frame_confirm)
        self.pB_ok.setObjectName(u"pB_ok")
        self.pB_ok.setIconSize(QSize(40, 40))

        self.gridLayout_17.addWidget(self.pB_ok, 1, 4, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_6, 1, 0, 1, 3)

        self.label_warning = QLabel(self.frame_confirm)
        self.label_warning.setObjectName(u"label_warning")

        self.gridLayout_17.addWidget(self.label_warning, 0, 1, 1, 1)

        self.label_confirm = QLabel(self.frame_confirm)
        self.label_confirm.setObjectName(u"label_confirm")
        self.label_confirm.setFont(font4)
        self.label_confirm.setAlignment(Qt.AlignCenter)
        self.label_confirm.setWordWrap(True)

        self.gridLayout_17.addWidget(self.label_confirm, 0, 2, 1, 3)

        self.pB_cancel = QPushButton(self.frame_confirm)
        self.pB_cancel.setObjectName(u"pB_cancel")
        self.pB_cancel.setIconSize(QSize(40, 40))

        self.gridLayout_17.addWidget(self.pB_cancel, 1, 3, 1, 1)


        self.gridLayout_25.addWidget(self.frame_confirm, 0, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_9, 0, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 3, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_historique, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_historique, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.cB_recherche.toggled.connect(self.frame_recherche.setVisible)
        self.pB_modif_2.toggled.connect(self.frame_edit_recipe.setVisible)
        self.pB_modif_2.toggled.connect(self.frame_details.setHidden)
        self.pB_modif_2.toggled.connect(self.pB_new_recipe.setDisabled)
        self.pB_new_recipe.toggled.connect(self.frame_edit_recipe.setVisible)
        self.pB_new_recipe.toggled.connect(self.frame_details.setHidden)
        self.pB_new_recipe.toggled.connect(self.pB_modif_2.setDisabled)
        self.pB_new_recipe.toggled.connect(self.lW_recettes.setHidden)
        self.pB_modif_2.toggled.connect(self.lW_recettes.setHidden)
        self.cB_tagtips.toggled.connect(self.cB_tagdessert.setDisabled)
        self.cB_tagtips.toggled.connect(self.cB_tagdinner.setDisabled)
        self.cB_tagtips.toggled.connect(self.cB_tagdouble.setDisabled)
        self.cB_tagtips.toggled.connect(self.cB_tagkids.setDisabled)
        self.cB_tagtips.toggled.connect(self.cB_taglunch.setDisabled)
        self.cB_tagtips.toggled.connect(self.cB_tagsummer.setDisabled)
        self.cB_tagtips.toggled.connect(self.cB_tagvegan.setDisabled)
        self.cB_tagtips.toggled.connect(self.cB_tagwinter.setDisabled)
        self.pB_option.toggled.connect(self.pB_option_2.setChecked)
        self.pB_option_2.toggled.connect(self.pB_option.setChecked)

        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u00c0 Table !", None))
        ___qtablewidgetitem = self.tW_menu.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Midi", None));
        ___qtablewidgetitem1 = self.tW_menu.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Soir", None));
#if QT_CONFIG(tooltip)
        self.cB_restes_2.setToolTip(QCoreApplication.translate("MainWindow", u"Le dernier repas, c'est les restes!", None))
#endif // QT_CONFIG(tooltip)
        self.cB_restes_2.setText(QCoreApplication.translate("MainWindow", u"Restes", None))
#if QT_CONFIG(tooltip)
        self.label_dessert.setToolTip(QCoreApplication.translate("MainWindow", u"Desserts", None))
#endif // QT_CONFIG(tooltip)
        self.label_dessert.setText("")
#if QT_CONFIG(tooltip)
        self.pB_new_menu_2.setToolTip(QCoreApplication.translate("MainWindow", u"Nouvelle carte", None))
#endif // QT_CONFIG(tooltip)
        self.pB_new_menu_2.setText("")
        self.dateEdit_2.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd-MM-yyyy", None))
        self.label_date.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"pour", None))
        self.sB_days_2.setSuffix(QCoreApplication.translate("MainWindow", u" jours", None))
#if QT_CONFIG(tooltip)
        self.pB_modif.setToolTip(QCoreApplication.translate("MainWindow", u"Modifier", None))
#endif // QT_CONFIG(tooltip)
        self.pB_modif.setText("")
#if QT_CONFIG(tooltip)
        self.pB_save.setToolTip(QCoreApplication.translate("MainWindow", u"Enregistrer dans l'Historique", None))
#endif // QT_CONFIG(tooltip)
        self.pB_save.setText("")
#if QT_CONFIG(tooltip)
        self.label_s_vegan.setToolTip(QCoreApplication.translate("MainWindow", u"Plats vegan", None))
#endif // QT_CONFIG(tooltip)
        self.label_s_vegan.setText(QCoreApplication.translate("MainWindow", u"s_vegan", None))
#if QT_CONFIG(tooltip)
        self.label_s_hiver.setToolTip(QCoreApplication.translate("MainWindow", u"Plats d'hiver", None))
#endif // QT_CONFIG(tooltip)
        self.label_s_hiver.setText(QCoreApplication.translate("MainWindow", u"s_winter", None))
#if QT_CONFIG(tooltip)
        self.label_s_ete.setToolTip(QCoreApplication.translate("MainWindow", u"Plats d'\u00e9t\u00e9", None))
#endif // QT_CONFIG(tooltip)
        self.label_s_ete.setText(QCoreApplication.translate("MainWindow", u"s_sum", None))
#if QT_CONFIG(tooltip)
        self.label_s_double.setToolTip(QCoreApplication.translate("MainWindow", u"Plats en double", None))
#endif // QT_CONFIG(tooltip)
        self.label_s_double.setText(QCoreApplication.translate("MainWindow", u"s_double", None))
#if QT_CONFIG(tooltip)
        self.label_s_kids.setToolTip(QCoreApplication.translate("MainWindow", u"Plats enfants", None))
#endif // QT_CONFIG(tooltip)
        self.label_s_kids.setText(QCoreApplication.translate("MainWindow", u"s_kids", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_carte), QCoreApplication.translate("MainWindow", u"Carte", None))
#if QT_CONFIG(tooltip)
        self.pB_send.setToolTip(QCoreApplication.translate("MainWindow", u"Envoyer", None))
#endif // QT_CONFIG(tooltip)
        self.pB_send.setText("")
#if QT_CONFIG(tooltip)
        self.pB_print.setToolTip(QCoreApplication.translate("MainWindow", u"Imprimer", None))
#endif // QT_CONFIG(tooltip)
        self.pB_print.setText("")
#if QT_CONFIG(tooltip)
        self.pB_copy.setToolTip(QCoreApplication.translate("MainWindow", u"Copier", None))
#endif // QT_CONFIG(tooltip)
        self.pB_copy.setText("")
        self.label_top.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_icon_carte.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_cocktail.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_liste), QCoreApplication.translate("MainWindow", u"Liste de courses", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_menus), QCoreApplication.translate("MainWindow", u"Menus", None))
#if QT_CONFIG(tooltip)
        self.pB_new_recipe.setToolTip(QCoreApplication.translate("MainWindow", u"Nouvelle recette", None))
#endif // QT_CONFIG(tooltip)
        self.pB_new_recipe.setText("")
#if QT_CONFIG(tooltip)
        self.cB_recherche.setToolTip(QCoreApplication.translate("MainWindow", u"Filtrer la liste de recettes", None))
#endif // QT_CONFIG(tooltip)
        self.cB_recherche.setText(QCoreApplication.translate("MainWindow", u"Recherche", None))
#if QT_CONFIG(tooltip)
        self.pB_modif_2.setToolTip(QCoreApplication.translate("MainWindow", u"Modifier cette recette", None))
#endif // QT_CONFIG(tooltip)
        self.pB_modif_2.setText("")
        self.pB_delete.setText("")
        self.label_newedit.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
#if QT_CONFIG(tooltip)
        self.pB_cancel_2.setToolTip(QCoreApplication.translate("MainWindow", u"Annuler", None))
#endif // QT_CONFIG(tooltip)
        self.pB_cancel_2.setText("")
#if QT_CONFIG(tooltip)
        self.pB_ok_2.setToolTip(QCoreApplication.translate("MainWindow", u"Enregistrer", None))
#endif // QT_CONFIG(tooltip)
        self.pB_ok_2.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.pB_option.setToolTip(QCoreApplication.translate("MainWindow", u"Optionnel", None))
#endif // QT_CONFIG(tooltip)
        self.pB_option.setText(QCoreApplication.translate("MainWindow", u"[", None))
#if QT_CONFIG(tooltip)
        self.lE_qty.setToolTip(QCoreApplication.translate("MainWindow", u"Quantit\u00e9", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pB_add.setToolTip(QCoreApplication.translate("MainWindow", u"Ajouter cet ingr\u00e9dient", None))
#endif // QT_CONFIG(tooltip)
        self.pB_add.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.cB_ingredient.setToolTip(QCoreApplication.translate("MainWindow", u"Choix d'ingr\u00e9dient", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.cB_unit.setToolTip(QCoreApplication.translate("MainWindow", u"Choix d'unit\u00e9", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pB_option_2.setToolTip(QCoreApplication.translate("MainWindow", u"Optionnel", None))
#endif // QT_CONFIG(tooltip)
        self.pB_option_2.setText(QCoreApplication.translate("MainWindow", u"]", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Ingr\u00e9dients :", None))
#if QT_CONFIG(tooltip)
        self.pB_photo.setToolTip(QCoreApplication.translate("MainWindow", u"Choisir une image", None))
#endif // QT_CONFIG(tooltip)
        self.pB_photo.setText("")
        self.label_image_2.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Temps de pr\u00e9paration :", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"minutes", None))
#if QT_CONFIG(tooltip)
        self.tB_preparation.setToolTip(QCoreApplication.translate("MainWindow", u"Instructions pour la pr\u00e9paration", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Pr\u00e9paration :", None))
#if QT_CONFIG(tooltip)
        self.lE_titre.setToolTip(QCoreApplication.translate("MainWindow", u"Titre de la recette", None))
#endif // QT_CONFIG(tooltip)
        self.lE_titre.setText(QCoreApplication.translate("MainWindow", u"Titre", None))
#if QT_CONFIG(tooltip)
        self.cB_tagvegan.setToolTip(QCoreApplication.translate("MainWindow", u"Vegan", None))
#endif // QT_CONFIG(tooltip)
        self.cB_tagvegan.setText("")
#if QT_CONFIG(tooltip)
        self.cB_tagwinter.setToolTip(QCoreApplication.translate("MainWindow", u"Plat d'hiver", None))
#endif // QT_CONFIG(tooltip)
        self.cB_tagwinter.setText("")
#if QT_CONFIG(tooltip)
        self.cB_tagkids.setToolTip(QCoreApplication.translate("MainWindow", u"Les enfants aiment", None))
#endif // QT_CONFIG(tooltip)
        self.cB_tagkids.setText("")
#if QT_CONFIG(tooltip)
        self.cB_tagdinner.setToolTip(QCoreApplication.translate("MainWindow", u"Soir", None))
#endif // QT_CONFIG(tooltip)
        self.cB_tagdinner.setText("")
#if QT_CONFIG(tooltip)
        self.cB_tagsummer.setToolTip(QCoreApplication.translate("MainWindow", u"Plat d'\u00e9t\u00e9", None))
#endif // QT_CONFIG(tooltip)
        self.cB_tagsummer.setText("")
#if QT_CONFIG(tooltip)
        self.cB_tagdouble.setToolTip(QCoreApplication.translate("MainWindow", u"Peut servir pour 2 repas", None))
#endif // QT_CONFIG(tooltip)
        self.cB_tagdouble.setText("")
#if QT_CONFIG(tooltip)
        self.cB_tagdessert.setToolTip(QCoreApplication.translate("MainWindow", u"Dessert", None))
#endif // QT_CONFIG(tooltip)
        self.cB_tagdessert.setText("")
#if QT_CONFIG(tooltip)
        self.cB_taglunch.setToolTip(QCoreApplication.translate("MainWindow", u"Midi", None))
#endif // QT_CONFIG(tooltip)
        self.cB_taglunch.setText("")
#if QT_CONFIG(tooltip)
        self.cB_tagtips.setToolTip(QCoreApplication.translate("MainWindow", u"Pr\u00e9paration (uniquement)", None))
#endif // QT_CONFIG(tooltip)
        self.cB_tagtips.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Pr\u00e9paration :", None))
        self.tE_recette.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Poiret One'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Ubuntu'; font-weight:400;\"><br /></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.label_summer.setToolTip(QCoreApplication.translate("MainWindow", u"Plat d'\u00e9t\u00e9", None))
#endif // QT_CONFIG(tooltip)
        self.label_summer.setText(QCoreApplication.translate("MainWindow", u"tagsum", None))
#if QT_CONFIG(tooltip)
        self.label_dessert_2.setToolTip(QCoreApplication.translate("MainWindow", u"Dessert", None))
#endif // QT_CONFIG(tooltip)
        self.label_dessert_2.setText(QCoreApplication.translate("MainWindow", u"tagdesser", None))
#if QT_CONFIG(tooltip)
        self.label_winter.setToolTip(QCoreApplication.translate("MainWindow", u"Plat d'hiver", None))
#endif // QT_CONFIG(tooltip)
        self.label_winter.setText(QCoreApplication.translate("MainWindow", u"tagwinter", None))
#if QT_CONFIG(tooltip)
        self.label_double.setToolTip(QCoreApplication.translate("MainWindow", u"Peut servir pour 2 repas", None))
#endif // QT_CONFIG(tooltip)
        self.label_double.setText(QCoreApplication.translate("MainWindow", u"tagdouble", None))
#if QT_CONFIG(tooltip)
        self.label_tips.setToolTip(QCoreApplication.translate("MainWindow", u"Pr\u00e9paration", None))
#endif // QT_CONFIG(tooltip)
        self.label_tips.setText(QCoreApplication.translate("MainWindow", u"tagtips", None))
#if QT_CONFIG(tooltip)
        self.label_kids.setToolTip(QCoreApplication.translate("MainWindow", u"Les enfants aiment", None))
#endif // QT_CONFIG(tooltip)
        self.label_kids.setText(QCoreApplication.translate("MainWindow", u"tagkids", None))
#if QT_CONFIG(tooltip)
        self.label_lunchdinner.setToolTip(QCoreApplication.translate("MainWindow", u"Midi/Soir", None))
#endif // QT_CONFIG(tooltip)
        self.label_lunchdinner.setText(QCoreApplication.translate("MainWindow", u"tagld", None))
#if QT_CONFIG(tooltip)
        self.label_vegan.setToolTip(QCoreApplication.translate("MainWindow", u"Vegan", None))
#endif // QT_CONFIG(tooltip)
        self.label_vegan.setText(QCoreApplication.translate("MainWindow", u"tagvegan", None))
#if QT_CONFIG(tooltip)
        self.pB_back.setToolTip(QCoreApplication.translate("MainWindow", u"Revenir \u00e0 la recette pr\u00e9c\u00e9dente", None))
#endif // QT_CONFIG(tooltip)
        self.pB_back.setText("")
#if QT_CONFIG(tooltip)
        self.pB_send_2.setToolTip(QCoreApplication.translate("MainWindow", u"Envoyer", None))
#endif // QT_CONFIG(tooltip)
        self.pB_send_2.setText("")
#if QT_CONFIG(tooltip)
        self.pB_print_2.setToolTip(QCoreApplication.translate("MainWindow", u"Imprimer", None))
#endif // QT_CONFIG(tooltip)
        self.pB_print_2.setText("")
        self.label_titre.setText(QCoreApplication.translate("MainWindow", u"Titre", None))
        self.label_image.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Ingr\u00e9dients :", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"sans", None))
#if QT_CONFIG(tooltip)
        self.lE_without.setToolTip(QCoreApplication.translate("MainWindow", u"mots cl\u00e9s, s\u00e9par\u00e9s par une virgule (ex: vegan,farine,...)", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"avec", None))
#if QT_CONFIG(tooltip)
        self.pB_filter.setToolTip(QCoreApplication.translate("MainWindow", u"Filtrer", None))
#endif // QT_CONFIG(tooltip)
        self.pB_filter.setText("")
#if QT_CONFIG(tooltip)
        self.lE_with.setToolTip(QCoreApplication.translate("MainWindow", u"mots cl\u00e9s, s\u00e9par\u00e9s par une virgule (ex: vegan,farine,...)", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_recettes), QCoreApplication.translate("MainWindow", u"Recettes", None))
        self.label_deco_1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_8.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_7.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_6.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_11.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_12.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_13.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_15.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_10.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_14.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_16.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_deco_9.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
#if QT_CONFIG(tooltip)
        self.pB_ok.setToolTip(QCoreApplication.translate("MainWindow", u"OK", None))
#endif // QT_CONFIG(tooltip)
        self.pB_ok.setText("")
        self.label_warning.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_confirm.setText(QCoreApplication.translate("MainWindow", u"Confirmer la mise \u00e0 jour de ces menus ?", None))
#if QT_CONFIG(tooltip)
        self.pB_cancel.setToolTip(QCoreApplication.translate("MainWindow", u"Annuler", None))
#endif // QT_CONFIG(tooltip)
        self.pB_cancel.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_historique), QCoreApplication.translate("MainWindow", u"Historique", None))
    # retranslateUi

