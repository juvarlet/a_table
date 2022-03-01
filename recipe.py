
from ingredient import Ingredient
from PySide2.QtCore import*
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel
import custom_widgets as cw
import os
from stylesheet_update import COLORS

LINE_RECIPE_UI = cw.dirname('UI') + 'line_recipe.ui'

class Recipe:
    def __init__(self, uid, name, ing_list = [], preparation = '', time = 0, tags = [], image = ''):
        self.uid = uid
        self.name = name
        self.ing_list = ing_list  #new implementation using the Ingredient class
        if self.ing_list is None:
            self.ing_list = []
        self.preparation = preparation
        self.time = time
        self.tags = tags
        self.image = image
        
        self.dirname = cw.dirname('')
        # self.init_line_widget()
    
    def __str__(self):
        return self.name
    
    def isTagged(self, tag):
        try:
            return tag in self.tags
        except:
            return False
    
    # def init_ing_list(self):#DEPRECATED
    #     output = []
    #     if self.ingredients_list_qty is not None: 
    #         for ing, qty_unit in self.ingredients_list_qty.items():
    #             if ing[0] == '[' and ing[-1] == ']':
    #                 name = ing[1:-1]
    #                 is_optional = True
    #             else :
    #                 name = ing
    #                 is_optional = False
    #             qty, unit = qty_unit

    #             ingredient = Ingredient(name, qty, unit, is_optional)
    #             output.append(ingredient)
    #     return output

    def get_mandatory_and_optional_ing_lists(self):
        mand_ing_list = []
        opt_ing_list = []
        if len(self.ing_list) == 0:
            return
        for ing in self.ing_list:
            if ing.is_optional:
                opt_ing_list.append(ing)
            else:
                mand_ing_list.append(ing)
        return [mand_ing_list, opt_ing_list]

    def ingredients_string(self, my_recipe_db):
        string = ''
        string_option = '\nOptionnel :\n'
        options = False
        if len(self.ing_list) > 0:
            for ingredient in self.ing_list:
                qty = ingredient.qty
                unit = ingredient.unit
                if ingredient.name != '':
                    if ingredient.is_optional:
                        options = True
                        #include links
                        e_ing = my_recipe_db.find_links(ingredient.name)
                        string_option += '- %s : %s' % (e_ing, qty)
                        if unit != '()':
                            string_option += unit
                        string_option += '\n'
                    else:
                        #include links
                        e_ing = my_recipe_db.find_links(ingredient.name)
                        string += '- %s : %s' % (e_ing, qty)
                        if unit != '()':
                            string += unit
                        string += '\n'
        if options:
            string += string_option
        
        if self.time is not None:
            string += '\nTemps de préparation : %s minutes' % self.time
        return string
    
    def ingredients_string_list(self):
        string_list = []
        string_option_list = ['', 'Optionnel :']

        if len(self.ing_list) > 0:
            for ingredient in self.ing_list:
                qty = ingredient.qty
                unit = ingredient.unit
                if ingredient.name != '':
                    if ingredient.is_optional:
                        string_option = '- %s : %s' % (ingredient.name, qty)
                        if unit != '()':
                            string_option += unit
                        string_option_list.append(string_option)
                    else:
                        string = '- %s : %s' % (ingredient.name, qty)
                        if unit != '()':
                            string += unit
                        string_list.append(string)
        
        if len(string_option_list) > 2:
            string_list += string_option_list
        return string_list
    
    def hasIngredient(self, ingredient: str):
        try:
            if ingredient in [ing.name for ing in self.ing_list]:
                return True
            else:
                return False
        except:
            return False
    
    def meet_with_criteria(self, with_text):
        if with_text == '':
            return True
        else:
            meets = with_text in self.name.lower()
            if self.tags is not None:
                meets += with_text in list(map(str.lower, self.tags))
            if len(self.ing_list) > 0:
                meets += with_text in list(map(str.lower, [ing.name for ing in self.ing_list]))
            if self.preparation is not None:
                meets += with_text in self.preparation.lower()
            return bool(meets)
    
    def meet_without_criteria(self, without_text):
        if without_text == '':
            return True
        return not self.meet_with_criteria(without_text)
    
    def toString_cells(self):
        cells = 7*[None]
        cells[0] = self.uid
        cells[1] = self.name
        if len(self.ing_list) > 0:
            ing_strings = []
            for ingredient in self.ing_list:
                qty = ingredient.qty
                unit = ingredient.unit
                ing_strings.append('%s,%s,%s' % (ingredient, qty, unit))
            cells[2] = '/'.join(ing_strings)
        cells[3] = self.time
        if self.tags is not None:
            cells[4] = '/'.join(self.tags)
        cells[5] = self.image.split('/')[-1]
        cells[6] = self.preparation
        return cells
    
    def render_card(self, label_title: QLabel, label_image: QLabel, scale = 1):
        image_path = self.dirname + self.image + '_icon.jpg'
        qpix = QPixmap(image_path)
        if self.image != '' and self.image != '/images/':
            if qpix.height() < qpix.width():#landscape w:400, h:300
                # p1 = qpix.scaledToHeight(self.height()*1, Qt.SmoothTransformation)
                p1 = qpix.scaledToHeight(int(label_title.screen().geometry().height()*1/5*scale), Qt.SmoothTransformation)
            else:#portrait w:300, h:400
                # p1 = qpix.scaledToWidth(self.width()*1, Qt.SmoothTransformation)
                p1 = qpix.scaledToWidth(int(label_title.screen().geometry().height()*1/5*scale), Qt.SmoothTransformation)
            label_image.setPixmap(p1)
        else:
            label_image.setPixmap(qpix)
        label_title.setText(self.name)