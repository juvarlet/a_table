import imp
import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon, QColor

import os
import sys
import custom_widgets as cw
from recipe import Recipe

UI_FILE = cw.dirname('UI') + 'card_recipe.ui'

class CardRecipe(QWidget):
    def __init__(self, recipe: Recipe, status=0, parent=None):
        super(CardRecipe, self).__init__(parent)

        self.recipe = recipe
        #status: 0(default), 1(highlighted), 2(no ingredient)
        self.status = status 
        
        self.loadUI()
        self.saveComponents()
        
        self.initial_state()
        self.connect_actions()
        self.update_modif()
    
    def loadUI(self):
        self.pW = cw.loadUI(self, UI_FILE)
    
    def saveComponents(self):
        self.dirname = cw.dirname('UI/images')
        
        self.label_image: QLabel
        self.label_image = self.pW.label_image
        self.label_title: QLabel
        self.label_title = self.pW.label_title
        self.frame_card: QFrame
        self.frame_card = self.pW.frame_card
        
    def initial_state(self):
        self.recipe.render_card(self.label_title, self.label_image, 4/5)
        self.apply_status(self.status)
        
    def connect_actions(self):
        pass
    
    def update_modif(self):
        pass
    
    def apply_status(self, status):
        if status == 0:
            self.reset_status()
        elif status == 1:
            self.highlight()
        elif status == 2:
            self.no_ingredient()
        
    def reset_status(self):
        self.status = 0
        
        self.frame_card.setStyleSheet('''
            QFrame#frame_card{
                border: 5px solid #ffc05c;
                border-radius: 10px;
                background-color:#ffc05c;
            }
            ''')
        self.label_title.setStyleSheet('''
            QLabel#label_title{
                border: 1px solid #ffc05c;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                background-color:#ffc05c;
            }
            ''')
        
        self.label_image.setStyleSheet('''
            QLabel#label_image{
                border: 1px solid #ffc05c;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                background-color:#ffc05c;
            }
            ''')
    
    def highlight(self):
        self.status = 1
        
        self.frame_card.setStyleSheet('''
            QFrame#frame_card{
                border: 5px solid #36a9d3;
                border-radius: 10px;
                background-color:#36a9d3;
            }
            ''')
        self.label_title.setStyleSheet('''
            QLabel#label_title{
                border: 1px solid #36a9d3;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                background-color:#36a9d3;
            }
            ''')
        
        self.label_image.setStyleSheet('''
            QLabel#label_image{
                border: 1px solid #36a9d3;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                background-color:#36a9d3;
            }
            ''')
    
    def no_ingredient(self):
        self.status = 2
        
        self.frame_card.setStyleSheet('''
            QFrame#frame_card{
                border: 5px solid #fdf1d9;
                border-radius: 10px;
                background-color:#fdf1d9;
            }
            ''')
        self.label_title.setStyleSheet('''
            QLabel#label_title{
                border: 1px solid #fdf1d9;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                background-color:#fdf1d9;
            }
            ''')

        self.label_image.setStyleSheet('''
            QLabel#label_image{
                border: 1px solid #fdf1d9;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                background-color:#fdf1d9;
            }
            ''')