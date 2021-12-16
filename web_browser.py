import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon, QColor
from PySide2.QtWebEngineWidgets import QWebEngineView

import os
import sys
import custom_widgets as cw
import html_parser as web
from ingredient import Ingredient
from ingredient_item import IngredientItem
from recipe import Recipe
import pyautogui
from stylesheet_update import COLORS
import uuid

UI_FILE = cw.dirname('UI') + 'web_browser.ui'

class WebBrowser(QWidget):
    
    title = Signal(str)
    recipe = Signal(Recipe)
    preparation = Signal(str, bool)
    message = Signal(list, bool)
    reset = Signal(str)
    
    def __init__(self, user_settings, parent=None):
        super(WebBrowser, self).__init__(parent)

        self.colors = COLORS
        self.icon_folder = cw.dirname('UI/images')
        self.user_settings = user_settings
        self.myThreads = []
        
        self.loadUI()
        self.saveComponents()
        
        self.initial_state()
        self.populate_ui()
        self.connect_actions()
        self.update_modif()
        
    def loadUI(self):
        self.pW = cw.loadUI(self, UI_FILE)
    
    def saveComponents(self):
        self.gL_web: QGridLayout
        self.gL_web = self.pW.gL_web
        self.hL_tools: QHBoxLayout
        self.hL_tools = self.pW.hL_tools
        self.frame_wB: QFrame
        self.frame_wB = self.pW.frame_wB
        self.wV = QWebEngineView()
        
    def initial_state(self):
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"
        # self.frame_wB.hide()
        
        page = cw.WebEnginePage(self.wV)
        self.wV.setPage(page)
        
        self.wV.load(self.user_settings.homepage)
        self.gL_web.addWidget(self.wV)
    
    def populate_ui(self):
        self.navtb = QToolBar("Navigation")
        self.navtb.setStyleSheet('QToolBar{background-color:transparent;}QToolButton{background:transparent;}')
        self.navtb.setIconSize( QSize(30,30) )
        self.hL_tools.addWidget(self.navtb)
        
        self.pB_cook = QPushButton('', self.frame_wB)
        self.pB_cook.setFixedSize(60,60)
        self.pB_cook.setIconSize(QSize(40,40))
        self.pB_cook.setIcon(QIcon(self.icon_folder + 'icon_service.png'))
        self.pB_cook.setToolTip('Recopier cette recette')
        self.navtb.addWidget(self.pB_cook)
        
        self.back_btn = QAction( QIcon(self.icon_folder + 'icon_back.png'), "Back", self)
        self.back_btn.setToolTip("Page précédente")
        self.navtb.addAction(self.back_btn)
        
        self.next_btn = QAction( QIcon(self.icon_folder + 'icon_fwd.png'), "Forward", self)
        self.next_btn.setToolTip("Page suivante")
        self.navtb.addAction(self.next_btn)

        self.reload_btn = QAction( QIcon(self.icon_folder + 'icon_reload.png'), "Reload", self)
        self.reload_btn.setToolTip("Recharger la page")
        self.navtb.addAction(self.reload_btn)

        self.home_btn = QAction( QIcon(self.icon_folder + 'icon_chef.png'), "Home", self)
        self.home_btn.setToolTip("Page d'accueil")
        self.navtb.addAction(self.home_btn)
        
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap( QPixmap(self.icon_folder + 'icon_nolock_.png') )
        self.navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.navtb.addWidget(self.urlbar)

        self.stop_btn = QAction( QIcon(self.icon_folder + 'icon_fork_X.png'), "Stop", self)
        self.stop_btn.setToolTip("Interrompre le chargement")
        self.navtb.addAction(self.stop_btn)
        
        self.open_file_action = QAction( QIcon(self.icon_folder + 'icon_open.png'), "Ouvrir une page web...", self)
        self.open_file_action.setToolTip("Ouvrir le fichier HTML")
        self.navtb.addAction(self.open_file_action)

        self.save_file_action = QAction( QIcon(self.icon_folder + 'icon_save.png'), "Enregistrer sous...", self)
        self.save_file_action.setToolTip("Enregistrer la page en cours")
        self.navtb.addAction(self.save_file_action)
        
    def connect_actions(self):
        self.pB_cook.clicked.connect(self.on_parse_html)
        self.back_btn.triggered.connect( self.wV.back )
        self.next_btn.triggered.connect( self.wV.forward )
        self.reload_btn.triggered.connect( self.wV.reload )
        self.home_btn.triggered.connect(lambda: self.wV.setUrl(self.user_settings.homepage))
        self.urlbar.returnPressed.connect( self.navigate_to_url )
        self.stop_btn.triggered.connect( self.wV.stop )
        self.open_file_action.triggered.connect( self.open_html )
        self.save_file_action.triggered.connect( self.save_file )
    
    def update_modif(self):
        self.wV.urlChanged.connect(self.update_urlbar)
        
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
            self.httpsicon.setPixmap( QPixmap(self.icon_folder + 'icon_lock_.png') )

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap( QPixmap(self.icon_folder + 'icon_nolock_.png') )

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
            self.title.emit(recipe_name)
            # self.lE_title.setText(recipe_name)
        else:
            list_failed.append('- Titre')
            self.title.emit('Nouvelle Recette')
            # self.lE_title.setText('Nouvelle Recette')

        if ingredients_list != []:
            ing_dict = {}
            for ing in ingredients_list:
                try:
                    ing_qty, ing_name = ing.split(" ", 1)
                except:
                    ing_name = ing
                    ing_qty = ''
                ing_dict[ing_name] = [ing_qty,""]
            recipe = Recipe(uuid.uuid4(), "", ing_dict)
            self.recipe.emit(recipe)
            # self.populate_ing_list(recipe)
        else:
            list_failed.append('- Liste des ingrédients')
            self.reset.emit('ingredients')
            # self.tW_ingredients.clear()
            # self.tW_ingredients.setColumnCount(1)
            # self.tW_ingredients.setRowCount(1)
            
        if steps != []:
            self.preparation.emit('\n'.join(steps), True)
            # self.tB_preparation.setText('\n'.join(steps))
        else:
            list_failed.append('- Préparation')
            self.reset.emit('preparation')
            # self.tB_preparation.clear()
            
        #TBC to avoid previous settings removal, following lines commented
        # self.sB_time.setValue(0)
        
        # tags = [self.cB_tagdessert, self.cB_tagdinner, self.cB_tagdouble, self.cB_tagkids, self.cB_taglunch,
        #         self.cB_tagsummer, self.cB_tagwinter, self.cB_tagvegan, self.cB_tagtips]
        # tag_names = ['dessert', 'soir', 'double', 'kids', 'midi', 'ete', 'hiver', 'vegan', 'tips']
        # for tag, tag_name in zip(tags, tag_names):
        #     tag.setChecked(False)
        
        self.preparation.emit("<a href='%s'>%s</a>" % (url, url), False)
        # self.tB_preparation.append("<a href='%s'>%s</a>" % (url, url))
        message += 'Le lien vers la recette a été ajouté.'
        
        if len(list_failed) > 0:
            message += "\nLes éléments suivants n'ont pas pu être copiés :\n%s" % '\n'.join(list_failed)
            self.message.emit([message], True)
            # self.display_error(message)
        else:
            message += "<br/>La recette a été correctement importée !"
            self.message.emit([message, self.icon_folder + 'icon_service.png'], False)
            # self.print_thread_function(message, icon_path = self.icon_folder + 'icon_service.png')
       
    def on_new_webpage(self, url, okToParse):
        if url == self.urlbar.text():#make sure url validated matches current url (asynchronous thread treatment)
            icon = QIcon(self.icon_folder + 'icon_service%s.png' % ['_', ''][okToParse])
            self.pB_cook.setIcon(icon)
            self.pB_cook.setToolTip(['Copier le lien', 'Importer la recette'][okToParse])
    