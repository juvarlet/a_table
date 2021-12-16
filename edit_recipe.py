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
from stylesheet_update import COLORS
from web_browser import WebBrowser

UI_FILE = cw.dirname('UI') + 'edit_recipe.ui'

class EditRecipe(QWidget):
    
    on_ok = Signal(list)
    on_cancel = Signal()
    on_error = Signal(str)
    on_message = Signal(str, str)
    
    def __init__(self, user_settings, recipe_db, parent=None):
        super(EditRecipe, self).__init__(parent)

        self.colors = COLORS
        self.recipe_image_path = ''
        self.mode = 0 #0:new ; 1:edit
        self.user_settings = user_settings
        self.recipe_db = recipe_db
        
        self.loadUI()
        self.saveComponents()
        
        self.initial_state()
        self.connect_actions()
        self.update_modif()
    
    def loadUI(self):
        self.pW = cw.loadUI(self, UI_FILE)
    
    def saveComponents(self):
        self.label_newedit: QLabel
        self.label_newedit = self.pW.label_newedit
        self.pB_photo: QPushButton
        self.pB_photo = self.pW.pB_photo
        self.frame_new_recipe: QFrame
        self.frame_new_recipe = self.pW.frame_new_recipe
        self.lE_title: QLineEdit
        self.lE_title = self.pW.lE_titre
        self.img_dish: QLabel
        self.img_dish = self.pW.img_dish
        self.lw_ingredients: QListWidget
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
        self.pB_ok_2: QPushButton
        self.pB_ok_2 = self.pW.pB_ok_2
        self.pB_cancel_2: QPushButton
        self.pB_cancel_2 = self.pW.pB_cancel_2
        self.frame_wB: QFrame
        self.frame_wB = self.pW.frame_wB
        self.cB_web: QCheckBox
        self.cB_web = self.pW.cB_web
        self.vL_web_browser: QVBoxLayout
        self.vL_web_browser = self.pW.vL_web_browser
        
    def initial_state(self):
        self.pB_cancel_2.setIcon(QIcon(cw.dirname('UI/images') + 'icon_cancel.png'))
        self.pB_ok_2.setIcon(QIcon(cw.dirname('UI/images') + 'icon_ok.png'))
        self.pB_photo.setIcon(QIcon(cw.dirname('UI/images') + 'icon_photo.png'))
        
        self.lw_ingredients.setMouseTracking(True)
        
        self.frame_wB.hide()
        self.init_web_browser()
        
    def connect_actions(self):
        self.pB_ok_2.clicked.connect(self.on_confirm_recipe)
        self.pB_cancel_2.clicked.connect(self.on_cancel_recipe)
        self.pB_photo.clicked.connect(self.on_add_photo)
        self.cB_web.stateChanged.connect(self.on_show_web)
    
    def update_modif(self):
        self.lE_title.textChanged.connect(self.on_title_changed)
        self.selectable_tags = [self.cB_tagdinner, self.cB_tagdessert, self.cB_tagdouble, self.cB_tagkids,
                                self.cB_taglunch, self.cB_tagwinter, self.cB_tagsummer, self.cB_tagvegan, self.cB_tagtips]
        for tag in self.selectable_tags:
            tag.toggled.connect(lambda _, cB=tag: self.on_tag_selected(cB))
        
        # self.wV.urlChanged.connect(self.update_urlbar)

    def on_title_changed(self):
        title_ok = self.lE_title.text() != ''
        self.pB_ok_2.setEnabled(title_ok)
        self.pB_ok_2.setToolTip(['Il manque un titre pour la recette', 'Enregistrer'][title_ok])

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
                    
    def reset_fields(self):
        # self.img_dish.setPixmap(QPixmap())
        cw.load_pic(self.img_dish, cw.dirname('images') + 'placeholder_dish_icon.jpg')

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
    
    def new_mode(self):
        self.reset_fields()
        self.label_newedit.setText('Nouvelle Recette')
        self.lE_title.setText('Nouveau Titre')
        
        self.add_new_ingredient_to_list(Ingredient()) #Add empty ing for input
        
        self.mode = 0
        
    def edit_mode(self, recipe:Recipe):
        self.reset_fields()
        self.label_newedit.setText('Modifier la recette')
        self.lE_title.setText(recipe.name)
        cw.display_image(recipe, cw.dirname(''), self.img_dish, icon=False)
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
        
        self.mode = 1
        
    def add_new_ingredient_to_list(self, ingredient:Ingredient):
        #TODO : handle the case were the ingredient is already in the list
        ing_item = IngredientItem(ingredient)
        ing_item.on_btn_confirm_changes_clicked.connect(self.on_btn_confirm_changes_clicked)
        ing_item.on_btn_rm_item_clicked.connect(self.rm_ing_item_from_list)
        if ingredient.name == "" and ingredient.qty_unit == "" and ingredient.qty == -1:
            ing_item.selectWidgetMode(IngredientItem.WIDGET_EDIT_ING_MODE)

        list_widget_item = QListWidgetItem()
        list_widget_item.setSizeHint(QSize(0,30))
        self.lw_ingredients.addItem(list_widget_item)
        self.lw_ingredients.setItemWidget(list_widget_item,ing_item)
    
    def populate_ing_list(self, recipe:Recipe): #OK but can be improved
        if self.lw_ingredients.count : #vider la liste si elle n'est pas deja vide
            self.lw_ingredients.clear()
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
        # ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(self.lw_ingredients.count()-1)).findChild(IngredientItem)
        ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(self.lw_ingredients.count()-1))
        if ing_item.getUID() == ing_item_id:
            self.add_new_ingredient_to_list(Ingredient())

    def rm_ing_item_from_list(self, ing_item_id):
        for i in range(0, self.lw_ingredients.count()):
            ing_item:IngredientItem
            # ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(i)).findChild(IngredientItem)
            ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(i))
            if ing_item_id == ing_item.getUID():
                self.lw_ingredients.takeItem(i)
                break
    
    def on_confirm_recipe(self):
        #init output
        title = self.lE_title.text()
        image_cell = ''
        ing_dict = {}
        preparation_cell = ''
        time = None
        tag_checked_list = []
        auto_switch = ''
        
        #if not ok to save -> warning message
        if self.label_newedit.text() == 'Nouvelle Recette' and self.recipe_db.contains(title):#recipe already exists
            self.on_error.emit('Cette recette existe déjà, vous pouvez la modifier')
            
            #enable swicth to edit mode
            auto_switch = 'edit'
        else:
            #case with/without picture to be saved (filename = new_title.jpg and new_title_icon.jpg)
            if self.recipe_image_path != '':
                image_cell = title.lower().replace(' ', '_') #to be written in cell
                filepath = cw.dirname('images') + '%s.jpg' % image_cell #to be saved
                filpath_icon = cw.dirname('images') + '%s_icon.jpg' % image_cell #to be saved
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
                
            # print(self.lw_ingredients.count())
            for ing_index in range(self.lw_ingredients.count()-1): # "-1 in order to ignore the last 'input' line"
                ing_item:IngredientItem
                # ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(ing_index)).findChild(IngredientItem)
                ing_item = self.lw_ingredients.itemWidget(self.lw_ingredients.item(ing_index))
                # print(ing_item)
                ing_dict[ing_item.lbl_ing_name.text()] = [float(ing_item.lbl_ing_qty.text()), ing_item.lbl_ing_qty_unit.text()]

            #combine tags to string
            tags = [self.cB_tagdessert, self.cB_tagdinner, self.cB_tagdouble, self.cB_tagkids, self.cB_taglunch,
                    self.cB_tagsummer, self.cB_tagwinter, self.cB_tagvegan, self.cB_tagtips]
            tag_names = ['dessert', 'soir', 'double', 'kids', 'midi', 'ete', 'hiver', 'vegan', 'tips']
            tag_checked_list = [tag_name for tag, tag_name in zip(tags, tag_names) if tag.isChecked()]

            #case with preparation not empty -> combine preparation to string
            preparation_cell = web.with_clickable_links(self.tB_preparation.toPlainText())
            #case with preparation time not 0
            time_cell = ''
            if self.sB_time.text() != '0':
                time_cell = self.sB_time.text()
            
            if time_cell != '':
                time = time_cell

        self.reset_fields()
        
        self.on_ok.emit([title,
                         image_cell,
                         ing_dict,
                         preparation_cell,
                         time,
                         tag_checked_list,
                         self.mode,
                         auto_switch])
    
    def on_cancel_recipe(self):
        self.reset_fields()
        self.on_cancel.emit()
    
    def on_add_photo(self):
        self.recipe_image_path, filter = QFileDialog.getOpenFileName(self, 'Choisir une image', cw.dirname(''), 'Images (*.png *.jpg)')
        # print(image_path=='')
        cw.display_new_image(self.recipe_image_path, self.img_dish)
    
    def init_web_browser(self):
        self.wB = WebBrowser(self.user_settings)
        self.wB.title.connect(self.setTitle)
        self.wB.recipe.connect(self.populate_ing_list)
        self.wB.preparation.connect(self.setPreparation)
        self.wB.message.connect(self.sendMessage)
        self.wB.reset.connect(self.resetObject)
        self.vL_web_browser.addWidget(self.wB)
    
    def on_show_web(self):
        if self.cB_web.isChecked():
            if self.lE_title.text() != 'Nouveau Titre':
                new_search = QUrl("https://www.google.com/search?q=%s" %
                                  self.lE_title.text().replace(' ', '+'))
                self.wB.wV.setUrl(new_search)
        else:
            self.wB.wV.setUrl(self.user_settings.homepage)
    
    def setTitle(self, text):
        self.lE_title.setText(text)
    
    def setPreparation(self, text, reset):
        if reset:
            self.tB_preparation.setText(text)
        else:
            self.tB_preparation.append(text)
    
    def sendMessage(self, info, error):
        if error:
            message = info[0]
            self.on_error.emit(message)
        else:
            message, icon_path = info
            self.on_message.emit(message, icon_path)
    
    def resetObject(self, object):
        if object == 'ingredients':
            self.lw_ingredients.clear()
        elif object == 'preparation':
            self.tB_preparation.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    myGUI = EditRecipe()
    myGUI.show()
    
    sys.exit(app.exec_())