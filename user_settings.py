from stacked_recipes import UI_FILE


import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QIcon


import os
import custom_widgets as cw
import menu
import recipe_db

UI_FILE = os.path.dirname(__file__) + '/UI/user_settings.ui'
USER_ID_FILE = os.path.dirname(__file__) + '/user.id'
CONTACT = 'notification.a.table@gmail.com'

class UserSettings(QWidget):
    
    on_save = Signal(list)
    on_quit = Signal()
    on_history = Signal()
    on_error = Signal(str)
    
    def __init__(self, user_id_file = USER_ID_FILE, contact = CONTACT, parent=None):
        super(UserSettings, self).__init__(parent)
        
        self.user_id_file = user_id_file
        self.contact = contact
        self.loadUI()
        self.initial_state()
        self.connect_actions()
    
    def loadUI(self):
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        widget = QUiLoader().load(UI_FILE)
        vlayout.addWidget(widget)
        self.setLayout(vlayout)
        self.pW = widget
    
    def initial_state(self):
        self.dirname = os.path.dirname(__file__)
        self.label_user: QLabel
        self.label_user = self.pW.label_user
        self.pB_ok_3: QPushButton
        self.pB_ok_3 = self.pW.pB_ok_3
        self.pB_cancel_3: QPushButton
        self.pB_cancel_3 = self.pW.pB_cancel_3
        self.pB_history: QPushButton
        self.pB_history = self.pW.pB_history
        self.pB_reset: QPushButton
        self.pB_reset = self.pW.pB_reset
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
        
        self.default_email = ''
        self.default_nb_days = 7
        self.default_storage = self.dirname + '/Mes_Fiches/'
        self.homepage = QUrl("https://www.google.com/")
        self.user_id_file = self.dirname + '/user.id'
        self.init_user_settings()
        
        self.label_contact.setOpenExternalLinks(True)
        self.label_contact.setTextFormat(Qt.RichText)
        self.label_contact.setText("<a href='mailto:%s?Subject=Contact'>%s</a>" % (self.contact, self.contact))
        
        self.pB_ok_3.setIcon(QIcon(self.dirname + '/UI/images/icon_ok.png'))
        self.pB_cancel_3.setIcon(QIcon(self.dirname + '/UI/images/icon_cancel.png'))
        self.pB_history.setIcon(QIcon(self.dirname + '/UI/images/icon_plate_3colors.png'))
        self.pB_reset.setIcon(QIcon(self.dirname + '/UI/images/icon_back.png'))
        
        self.img_settings_email.setPixmap(QPixmap(self.dirname + '/UI/images/icon_send.png').scaled(40,40))
        self.img_settings_days.setPixmap(QPixmap(self.dirname + '/UI/images/icon_date_3colors_t_LD.png').scaled(40,40))
        self.img_settings_storage.setPixmap(QPixmap(self.dirname + '/UI/images/icon_print.png').scaled(40,40))
        self.label_homepage.setPixmap(QPixmap(self.dirname + '/UI/images/icon_web_search_gp.png').scaled(40,40))
        cw.load_pic(self.label_user, self.dirname + '/UI/images/icon_user_color.png')
        
    def connect_actions(self):
        self.tB_storage.clicked.connect(lambda : self.openDir(self.lE_storage, u'de sauvegarde des fiches', dirpath = self.default_storage))
        self.pB_ok_3.clicked.connect(self.on_save_settings)
        self.pB_cancel_3.clicked.connect(self.on_quit_settings)
        self.pB_reset.clicked.connect(self.init_user_settings)
        self.pB_history.clicked.connect(self.on_display_history)
    
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
            self.on_error.emit("Le chemin pour l'enregistrement des fiches n'est pas valide," +
                               " l'emplacement par défaut a été sélectionné (%s)" % self.default_storage)
        
        self.homepage = QUrl(self.lE_homepage.text())
        
        output = [self.default_email, 
                              str(self.default_nb_days), 
                              self.default_storage,
                              self.homepage.toString()]
        
        with open(self.user_id_file, 'w') as f:
            f.write(';'.join(output))
        
        self.on_save.emit(output)
        
    def on_quit_settings(self):
        self.on_quit.emit()
        
    def on_display_history(self):
        self.on_history.emit()
        
    def openDir(self, field, titre, dirpath = ''):
        if dirpath == '':
            dirpath = self.dirname
        path = QFileDialog.getExistingDirectory(self, u"Choix de l'emplacement " + titre, directory = dirpath)
        field.setText(str(path).replace('\\', '/'))
        