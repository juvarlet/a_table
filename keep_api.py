import gkeepapi
import keyring

from PySide2.QtCore import QThread
from PySide2.QtCore import *

import custom_widgets as cw

class GKeepList(QThread):
    
    color = gkeepapi.node.ColorValue.Green
    pinned = True
    title = 'À Table !'
    on_message = Signal(str, str)
    on_finish = Signal()
    
    def __init__(self, keep, line_ingredient_list):
        QThread.__init__(self)
        self.keep = keep
        self.line_ingredient_list = line_ingredient_list
        self.icon_path = cw.dirname('UI/images') + 'icon_keep.png'
    
    def run(self):
        #create list
        glist = self.keep.createList(
            self.title, 
            to_gkeeplist(self.line_ingredient_list)
        )
        
        glist.pinned = self.pinned
        glist.color = self.color

        #push to Google Keep
        self.keep.sync()

        self.on_message.emit('La liste Google Keep a bien été créée', self.icon_path)

def to_gkeeplist(line_ingredient_list):
    return [(str(line_ingredient.toIngredient()), line_ingredient.checked) for line_ingredient in line_ingredient_list]

def login_with_token(username):#to try, except with password
    keep = gkeepapi.Keep()#case token already stored
    token = keyring.get_password('google-keep-token', username)
    keep.resume(username, token)
    return keep

def login_with_password(username, password):
    keep = gkeepapi.Keep()
    keep.login(username, password)
    #store token
    token = keep.getMasterToken()
    keyring.set_password('google-keep-token', username, token)
    return keep

def debug():
    print('try to create a simple note first')
    keep = gkeepapi.Keep()
    keep.login('varlet.ju@gmail.com', 'Neiluj25')
    
    token = keep.getMasterToken()
    keyring.set_password('google-keep-token', 'varlet.ju@gmail.com', token)
    
    # token = keyring.get_password('google-keep-token', 'varlet.ju@gmail.com')
    # keep.resume('varlet.ju@gmail.com', token)

    glist = keep.createList('À Table !', [
        ('Item 1', False), # Not checked
        ('Item 2', True)  # Checked
    ])

    glist.pinned = True
    glist.color = gkeepapi.node.ColorValue.Green

    keep.sync()
    
    

if __name__ == '__main__':
    # keyring.delete_password('google-keep-token', 'varlet.ju@gmail.com')
    debug()