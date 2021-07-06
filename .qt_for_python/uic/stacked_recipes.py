# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stacked_recipes.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(398, 300)
        Form.setStyleSheet(u"QWidget{\n"
"background-color:#ccc1ae;\n"
"font-family:Poiret One;\n"
"font: bold;\n"
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
"	subcontrol-position: to"
                        "p right;\n"
"	width: 20px;\n"
"\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;\n"
"}\n"
"QComboBox::down-arrow {\n"
"     image: url(file:///../UI/images/icon_down_arrow.png);\n"
"	/*image: url(file:///../UI/images/icon_edit.png);*/\n"
"	width: 20px;\n"
"	height: 20px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView{\n"
"	background-color: #CCC1AE;\n"
"	/*color: #077B8A;*/\n"
" 	\n"
"	selection-background-color: #5C3C92;\n"
"	/*selection-color: #A2D5C6;*/\n"
"}\n"
"\n"
"QToolTip {\n"
"opacity: 300;\n"
"	border: 2px solid #5C3C92;\n"
"    border-radius: 4px;\n"
"    padding: 2px;\n"
"    background-color: #CCC1AE;\n"
"\n"
"}")
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_card = QFrame(self.frame)
        self.frame_card.setObjectName(u"frame_card")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_card.sizePolicy().hasHeightForWidth())
        self.frame_card.setSizePolicy(sizePolicy)
        self.frame_card.setFrameShape(QFrame.NoFrame)
        self.frame_card.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_card)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame_card)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pB_delete = QPushButton(self.frame_2)
        self.pB_delete.setObjectName(u"pB_delete")
        self.pB_delete.setMaximumSize(QSize(25, 25))

        self.gridLayout_3.addWidget(self.pB_delete, 2, 0, 1, 1)

        self.pB_next = QPushButton(self.frame_2)
        self.pB_next.setObjectName(u"pB_next")
        self.pB_next.setMaximumSize(QSize(25, 25))

        self.gridLayout_3.addWidget(self.pB_next, 0, 0, 1, 1)

        self.pB_add = QPushButton(self.frame_2)
        self.pB_add.setObjectName(u"pB_add")
        self.pB_add.setMaximumSize(QSize(25, 25))

        self.gridLayout_3.addWidget(self.pB_add, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_2, 0, 2, 2, 1)

        self.label_image = QLabel(self.frame_card)
        self.label_image.setObjectName(u"label_image")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_image.sizePolicy().hasHeightForWidth())
        self.label_image.setSizePolicy(sizePolicy2)
        self.label_image.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_image, 0, 0, 1, 2)

        self.label_title = QLabel(self.frame_card)
        self.label_title.setObjectName(u"label_title")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy3)
        self.label_title.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.label_title.setWordWrap(True)

        self.gridLayout_5.addWidget(self.label_title, 2, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.frame_3 = QFrame(self.frame_card)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.hL = QHBoxLayout()
        self.hL.setSpacing(0)
        self.hL.setObjectName(u"hL")

        self.gridLayout_4.addLayout(self.hL, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 3, 0, 1, 3)


        self.gridLayout_2.addWidget(self.frame_card, 0, 1, 1, 5)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.pB_delete.setToolTip(QCoreApplication.translate("Form", u"Supprimer cette recette", None))
#endif // QT_CONFIG(tooltip)
        self.pB_delete.setText("")
#if QT_CONFIG(tooltip)
        self.pB_next.setToolTip(QCoreApplication.translate("Form", u"Recette suivante", None))
#endif // QT_CONFIG(tooltip)
        self.pB_next.setText("")
#if QT_CONFIG(tooltip)
        self.pB_add.setToolTip(QCoreApplication.translate("Form", u"Ajouter une recette", None))
#endif // QT_CONFIG(tooltip)
        self.pB_add.setText("")
        self.label_image.setText("")
        self.label_title.setText(QCoreApplication.translate("Form", u"Title", None))
    # retranslateUi

