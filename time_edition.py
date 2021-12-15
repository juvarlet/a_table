import PySide2
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QBrush, QFont, QPixmap, QIcon, QPainter, QFontMetrics, QPen


import os, sys
import custom_widgets as cw
from datetime import date

from stylesheet_update import COLORS


UI_FILE = cw.dirname() + '/UI/time_edition.ui'

class TimeEdition(QWidget):
    
    on_start_date_changed = Signal(date)
    on_nb_days_changed = Signal(int)
    
    def __init__(self, default_nb_days, parent=None):
        super(TimeEdition, self).__init__(parent)
        
        self.default_nb_days = default_nb_days
        
        self.loadUI()
        self.saveComponents()
        self.initial_state()
        self.connect_actions()
        self.update_modif()
            
    def loadUI(self):
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        widget = QUiLoader().load(UI_FILE)
        vlayout.addWidget(widget)
        self.setLayout(vlayout)
        self.pW = widget
    
    def saveComponents(self):
        self.dirname = cw.dirname()
        self.date_from: QDateEdit
        self.date_from = self.pW.date_from
        self.date_to: QDateEdit
        self.date_to = self.pW.date_to
        self.slider: QSlider
        self.slider = self.pW.slider
        self.pB_from: QPushButton
        self.pB_from = self.pW.pB_from
        # self.sB_days: QSpinBox
        # self.sB_days = self.pW.sB_days
    
    def initial_state(self):
        # new_sB_days = cw.SpinBoxCustom(self.pW)
        # new_sB_days.setMinimumHeight(30)
        # new_sB_days.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        # new_sB_days.setSuffix(' jours')
        # new_sB_days.setValue(self.default_nb_days)
        # new_sB_days.setMinimum(1)
        # new_sB_days.setMaximum(14)
        # self.pW.gridLayout_4.replaceWidget(self.sB_days, new_sB_days)
        # # self.pW.horizontalLayout.insertWidget(5,new_sB_days)
        # self.sB_days = new_sB_days
        # self.pW.sB_days.setParent(None)
        
        new_slider = cw.SliderWithValue(Qt.Horizontal)
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
        
        self.pW.gridLayout_3.replaceWidget(self.slider, new_slider)
        self.slider = new_slider
        self.pW.slider.setParent(None)
        
        self.pB_from.setIcon(QIcon(self.dirname + '/UI/images/icon_date_2.png'))
        
        self.date_from.setDate(QDate().currentDate().addDays(1))
        self.date_to.setDate(self.date_from.date().addDays(self.default_nb_days - 1))
        
        
        
    def connect_actions(self):
        self.pushMenu = QMenu(self.pB_from)
        self.pushCalendar = QCalendarWidget(self.pushMenu)
        self.pushCalendar.setSelectedDate(self.date_from.date())
        self.pushCalendar.setFirstDayOfWeek(Qt.Monday)
        format = self.pushCalendar.weekdayTextFormat(Qt.Saturday)
        format.setForeground(QBrush(COLORS['#color2_bright#'], Qt.SolidPattern))
        self.pushCalendar.setWeekdayTextFormat(Qt.Saturday, format)
        self.pushCalendar.setWeekdayTextFormat(Qt.Sunday, format)
        self.pushAction = QWidgetAction(self.pushMenu)
        self.pushAction.setDefaultWidget(self.pushCalendar)
        self.pushMenu.addAction(self.pushAction)
        self.pB_from.setMenu(self.pushMenu)
        # self.pB_from.clicked.connect(self.calendar_popup)
    
    def update_modif(self):
        # self.sB_days.valueChanged.connect(self.slider.setValue)
        # self.slider.valueChanged.connect(self.sB_days.setValue)
        # self.sB_days.valueChanged.connect(self.handle_dates_change)
        self.slider.valueChanged.connect(self.handle_nb_days_change)
        # self.date_from.dateChanged.connect(self.handle_dates_change)
        self.pushCalendar.selectionChanged.connect(self.handle_date_change)
        self.pushCalendar.selectionChanged.connect(self.pushMenu.close)
    
    def handle_date_change(self):
        # Qdate_from = self.date_from.date()
        QDate_selected = self.pushCalendar.selectedDate()
        nb_days = self.slider.value()
        self.date_from.setDate(QDate_selected)
        self.date_to.setDate(QDate_selected.addDays(nb_days - 1))
        self.on_start_date_changed.emit(QDate_selected)
    
    def handle_nb_days_change(self):
        QDate_selected = self.pushCalendar.selectedDate()
        nb_days = self.slider.value()
        self.date_to.setDate(QDate_selected.addDays(nb_days - 1))
        self.on_nb_days_changed.emit(nb_days)
    
    # def calendar_popup(self):
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    toolButton = QToolButton(window)
    toolButton.setText('QToolButton')
    pushButton = QPushButton('QPushButton', window)
    layout = QHBoxLayout(window)
    layout.addWidget(toolButton)
    layout.addWidget(pushButton)
    window.show()
    
    toolMenu = QMenu(toolButton)
    toolCalendar = QCalendarWidget(toolMenu)
    toolAction = QWidgetAction(toolMenu)
    toolAction.setDefaultWidget(toolCalendar)
    toolMenu.addAction(toolAction)
    toolButton.setMenu(toolMenu)
    
    pushMenu = QMenu(pushButton)
    pushCalendar = QCalendarWidget(pushMenu)
    pushAction = QWidgetAction(pushMenu)
    pushAction.setDefaultWidget(pushCalendar)
    pushMenu.addAction(pushAction)
    pushButton.setMenu(pushMenu)
    
    toolCalendar.currentPageChanged.connect(pushCalendar.setCurrentPage)
    pushCalendar.currentPageChanged.connect(toolCalendar.setCurrentPage)
    toolCalendar.clicked.connect(pushCalendar.setSelectedDate)
    pushCalendar.clicked.connect(toolCalendar.setSelectedDate)
    pushCalendar.selectionChanged.connect(pushMenu.close)
    pushCalendar.selectionChanged.connect(lambda: print(pushCalendar.selectedDate()))
    
    sys.exit(app.exec_())
    