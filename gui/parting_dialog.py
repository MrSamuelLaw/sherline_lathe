# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'parting_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

class Ui_parting_dialog(object):
    def setupUi(self, parting_dialog):
        if parting_dialog.objectName():
            parting_dialog.setObjectName(u"parting_dialog")
        parting_dialog.resize(866, 663)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(parting_dialog.sizePolicy().hasHeightForWidth())
        parting_dialog.setSizePolicy(sizePolicy)
        parting_dialog.setSizeGripEnabled(False)
        self.gridLayout = QGridLayout(parting_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.speed_label = QLabel(parting_dialog)
        self.speed_label.setObjectName(u"speed_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.speed_label.sizePolicy().hasHeightForWidth())
        self.speed_label.setSizePolicy(sizePolicy1)
        self.speed_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.speed_label, 1, 0, 1, 1)

        self.feed_lineEdit = QLineEdit(parting_dialog)
        self.feed_lineEdit.setObjectName(u"feed_lineEdit")
        self.feed_lineEdit.setMinimumSize(QSize(100, 0))
        self.feed_lineEdit.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.feed_lineEdit, 0, 1, 1, 1)

        self.openPushButton = QPushButton(parting_dialog)
        self.openPushButton.setObjectName(u"openPushButton")
        self.openPushButton.setMinimumSize(QSize(100, 0))
        self.openPushButton.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.openPushButton, 6, 1, 1, 1)

        self.feed_label = QLabel(parting_dialog)
        self.feed_label.setObjectName(u"feed_label")
        sizePolicy1.setHeightForWidth(self.feed_label.sizePolicy().hasHeightForWidth())
        self.feed_label.setSizePolicy(sizePolicy1)
        self.feed_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.feed_label, 0, 0, 1, 1)

        self.widget = QWidget(parting_dialog)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(150, 150))

        self.gridLayout.addWidget(self.widget, 0, 2, 11, 1)

        self.diameter_label = QLabel(parting_dialog)
        self.diameter_label.setObjectName(u"diameter_label")
        sizePolicy1.setHeightForWidth(self.diameter_label.sizePolicy().hasHeightForWidth())
        self.diameter_label.setSizePolicy(sizePolicy1)
        self.diameter_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.diameter_label, 2, 0, 1, 1)

        self.spi_lineEdit = QLineEdit(parting_dialog)
        self.spi_lineEdit.setObjectName(u"spi_lineEdit")
        self.spi_lineEdit.setMinimumSize(QSize(100, 0))
        self.spi_lineEdit.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.spi_lineEdit, 3, 1, 1, 1)

        self.diameter_label_2 = QLabel(parting_dialog)
        self.diameter_label_2.setObjectName(u"diameter_label_2")
        sizePolicy1.setHeightForWidth(self.diameter_label_2.sizePolicy().hasHeightForWidth())
        self.diameter_label_2.setSizePolicy(sizePolicy1)
        self.diameter_label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.diameter_label_2, 3, 0, 1, 1)

        self.diameter_lineEdit = QLineEdit(parting_dialog)
        self.diameter_lineEdit.setObjectName(u"diameter_lineEdit")
        self.diameter_lineEdit.setMinimumSize(QSize(100, 0))
        self.diameter_lineEdit.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.diameter_lineEdit, 2, 1, 1, 1)

        self.unit_label = QLabel(parting_dialog)
        self.unit_label.setObjectName(u"unit_label")
        sizePolicy1.setHeightForWidth(self.unit_label.sizePolicy().hasHeightForWidth())
        self.unit_label.setSizePolicy(sizePolicy1)
        self.unit_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.unit_label, 4, 0, 1, 1)

        self.generatePushButton = QPushButton(parting_dialog)
        self.generatePushButton.setObjectName(u"generatePushButton")

        self.gridLayout.addWidget(self.generatePushButton, 5, 1, 1, 1)

        self.unit_comboBox = QComboBox(parting_dialog)
        self.unit_comboBox.setObjectName(u"unit_comboBox")
        self.unit_comboBox.setMinimumSize(QSize(100, 0))
        self.unit_comboBox.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.unit_comboBox, 4, 1, 1, 1)

        self.plainTextEdit = QPlainTextEdit(parting_dialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy2)
        self.plainTextEdit.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.plainTextEdit, 11, 2, 1, 1)

        self.speed_lineEdit = QLineEdit(parting_dialog)
        self.speed_lineEdit.setObjectName(u"speed_lineEdit")
        self.speed_lineEdit.setMinimumSize(QSize(100, 0))
        self.speed_lineEdit.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.speed_lineEdit, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 11, 0, 2, 2)

        QWidget.setTabOrder(self.feed_lineEdit, self.speed_lineEdit)
        QWidget.setTabOrder(self.speed_lineEdit, self.diameter_lineEdit)
        QWidget.setTabOrder(self.diameter_lineEdit, self.spi_lineEdit)
        QWidget.setTabOrder(self.spi_lineEdit, self.unit_comboBox)
        QWidget.setTabOrder(self.unit_comboBox, self.generatePushButton)
        QWidget.setTabOrder(self.generatePushButton, self.openPushButton)
        QWidget.setTabOrder(self.openPushButton, self.plainTextEdit)

        self.retranslateUi(parting_dialog)

        QMetaObject.connectSlotsByName(parting_dialog)
    # setupUi

    def retranslateUi(self, parting_dialog):
        parting_dialog.setWindowTitle(QCoreApplication.translate("parting_dialog", u"Parting Dialog", None))
        self.speed_label.setText(QCoreApplication.translate("parting_dialog", u"surface speed\n"
"[units/min]", None))
        self.openPushButton.setText(QCoreApplication.translate("parting_dialog", u"open in new tab", None))
        self.feed_label.setText(QCoreApplication.translate("parting_dialog", u"initial feedrate\n"
"[units/min]", None))
        self.diameter_label.setText(QCoreApplication.translate("parting_dialog", u"nominal diameter\n"
"[units]", None))
        self.diameter_label_2.setText(QCoreApplication.translate("parting_dialog", u"segments \n"
"per inch", None))
        self.unit_label.setText(QCoreApplication.translate("parting_dialog", u"units", None))
        self.generatePushButton.setText(QCoreApplication.translate("parting_dialog", u"generate gcode", None))
    # retranslateUi

