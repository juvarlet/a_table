from re import T
import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont, QPixmap, QIcon


import os
import custom_widgets as cw

UI_FILE = cw.dirname('UI') + 'user_settings.ui'
USER_ID_FILE = cw.dirname('') + '/user.id'
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
        self.saveComponents()
        self.initial_state()
        self.connect_actions()
        self.update_modif()
    
    def loadUI(self):
        self.pW = cw.loadUI(self, UI_FILE)

    def saveComponents(self):
        self.dirname = cw.dirname('')
        self.icon_folder = cw.dirname('UI/images')
        
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
        # self.sB_settings_days: QSpinBox
        # self.sB_settings_days = self.pW.sB_settings_days
        self.slider: QSlider
        self.slider = self.pW.slider
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
    
    def initial_state(self):
        self.default_email = ''
        self.default_nb_days = 7
        self.default_storage = self.dirname + '/Mes_Fiches/'
        self.homepage = QUrl("https://www.google.com/")
        # self.user_id_file = self.dirname + '/user.id'
        
        new_slider = cw.SliderWithValue(Qt.Horizontal, suffix = False)
        new_slider.setStyleSheet(self.slider.styleSheet())
        new_slider.setMinimum(1)
        new_slider.setMaximum(14)
        new_slider.setSingleStep(1)
        new_slider.setPageStep(1)
        new_slider.setValue(self.default_nb_days)
        new_slider.setTracking(True)
        new_slider.setTickPosition(QSlider.NoTicks)
        new_slider.setTickInterval(1)
        new_slider.setMinimumHeight(26)
        
        self.pW.gridLayout_42.replaceWidget(self.slider, new_slider)
        self.slider = new_slider
        self.pW.slider.setParent(None)
        
        self.init_user_settings()
        
        self.label_contact.setOpenExternalLinks(True)
        self.label_contact.setTextFormat(Qt.RichText)
        self.label_contact.setText("<a href='mailto:%s?Subject=Contact'>%s</a>" % (self.contact, self.contact))
        
        self.pB_ok_3.setIcon(QIcon(self.icon_folder + 'icon_ok.png'))
        self.pB_cancel_3.setIcon(QIcon(self.icon_folder + 'icon_cancel.png'))
        self.pB_history.setIcon(QIcon(self.icon_folder + 'icon_plate_3colors.png'))
        self.pB_reset.setIcon(QIcon(self.icon_folder + 'icon_reset.png'))
        
        self.img_settings_email.setPixmap(QPixmap(self.icon_folder + 'icon_send.png').scaled(40,40))
        self.img_settings_days.setPixmap(QPixmap(self.icon_folder + 'icon_date_3colors_t_LD.png').scaled(40,40))
        self.img_settings_storage.setPixmap(QPixmap(self.icon_folder + 'icon_print.png').scaled(40,40))
        self.label_homepage.setPixmap(QPixmap(self.icon_folder + 'icon_web_search_gp.png').scaled(40,40))
        cw.load_pic(self.label_user, self.icon_folder + 'icon_user_color.png')
        
        self.pB_reset.setEnabled(False)
        
    def connect_actions(self):
        self.tB_storage.clicked.connect(lambda : self.openDir(self.lE_storage, u'de sauvegarde des fiches', dirpath = self.default_storage))
        self.pB_ok_3.clicked.connect(self.on_save_settings)
        self.pB_cancel_3.clicked.connect(self.on_quit_settings)
        self.pB_reset.clicked.connect(self.init_user_settings)
        self.pB_history.clicked.connect(self.on_display_history)
    
    def update_modif(self):
        self.lE_email.textChanged.connect(self.highlight_diff)
        self.slider.valueChanged.connect(self.highlight_diff)
        self.lE_storage.textChanged.connect(self.highlight_diff)
        self.lE_homepage.textChanged.connect(self.highlight_diff)
    
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
        self.slider.setValue(self.default_nb_days)
        self.lE_storage.setText(self.default_storage)
        self.lE_homepage.setText(self.homepage.toString())
    
    def highlight_diff(self):
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
        
        email_diff = (self.lE_email.text() != self.default_email)
        days_diff = (self.slider.value() != self.default_nb_days)
        storage_diff = (self.lE_storage.text() != self.default_storage)
        homepage_diff = (self.lE_homepage.text() != self.homepage.toString())

        cw.changeFont(self.lE_email, change = email_diff)
        cw.changeFont(self.slider, change = days_diff)
        cw.changeFont(self.lE_storage, change = storage_diff)
        cw.changeFont(self.lE_homepage, change = homepage_diff)
        
        self.pB_reset.setEnabled(email_diff 
                                  or days_diff 
                                  or storage_diff 
                                  or homepage_diff)
        
    def on_save_settings(self):
        if self.pB_reset.isEnabled():#modification detected
            self.default_email = self.lE_email.text()
            self.default_nb_days = self.slider.value()
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
        else:#no modification, no need to save
            self.on_quit_settings()
        
    def on_quit_settings(self):
        self.on_quit.emit()
        
    def on_display_history(self):
        self.on_history.emit()
        
    def openDir(self, field, titre, dirpath = ''):
        if dirpath == '':
            dirpath = self.dirname
        path = QFileDialog.getExistingDirectory(self, u"Choix de l'emplacement " + titre, directory = dirpath)
        field.setText(str(path).replace('\\', '/'))
