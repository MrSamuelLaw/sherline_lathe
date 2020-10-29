# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'surfacing_dialog.ui'
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

class Ui_surfacing_Dialog(object):
    def setupUi(self, surfacing_Dialog):
        if surfacing_Dialog.objectName():
            surfacing_Dialog.setObjectName(u"surfacing_Dialog")
        surfacing_Dialog.resize(288, 324)
        self.gridLayout = QGridLayout(surfacing_Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.depth_label = QLabel(surfacing_Dialog)
        self.depth_label.setObjectName(u"depth_label")
        self.depth_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.depth_label, 0, 0, 1, 1)

        self.depth_lineEdit = QLineEdit(surfacing_Dialog)
        self.depth_lineEdit.setObjectName(u"depth_lineEdit")

        self.gridLayout.addWidget(self.depth_lineEdit, 0, 1, 1, 1)

        self.length_label = QLabel(surfacing_Dialog)
        self.length_label.setObjectName(u"length_label")
        self.length_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.length_label, 1, 0, 1, 1)

        self.length_lineEdit = QLineEdit(surfacing_Dialog)
        self.length_lineEdit.setObjectName(u"length_lineEdit")

        self.gridLayout.addWidget(self.length_lineEdit, 1, 1, 1, 1)

        self.feed_label = QLabel(surfacing_Dialog)
        self.feed_label.setObjectName(u"feed_label")
        self.feed_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.feed_label, 2, 0, 1, 1)

        self.feed_lineEdit = QLineEdit(surfacing_Dialog)
        self.feed_lineEdit.setObjectName(u"feed_lineEdit")

        self.gridLayout.addWidget(self.feed_lineEdit, 2, 1, 1, 1)

        self.rpm_label = QLabel(surfacing_Dialog)
        self.rpm_label.setObjectName(u"rpm_label")
        self.rpm_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.rpm_label, 3, 0, 1, 1)

        self.rpm_lineEdit = QLineEdit(surfacing_Dialog)
        self.rpm_lineEdit.setObjectName(u"rpm_lineEdit")

        self.gridLayout.addWidget(self.rpm_lineEdit, 3, 1, 1, 1)

        self.unit_label = QLabel(surfacing_Dialog)
        self.unit_label.setObjectName(u"unit_label")
        self.unit_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.unit_label, 4, 0, 1, 1)

        self.unit_comboBox = QComboBox(surfacing_Dialog)
        self.unit_comboBox.setObjectName(u"unit_comboBox")

        self.gridLayout.addWidget(self.unit_comboBox, 4, 1, 1, 1)

        self.create_pushButton = QPushButton(surfacing_Dialog)
        self.create_pushButton.setObjectName(u"create_pushButton")

        self.gridLayout.addWidget(self.create_pushButton, 5, 1, 1, 1)


        self.retranslateUi(surfacing_Dialog)

        QMetaObject.connectSlotsByName(surfacing_Dialog)
    # setupUi

    def retranslateUi(self, surfacing_Dialog):
        surfacing_Dialog.setWindowTitle(QCoreApplication.translate("surfacing_Dialog", u"Surfacing_Dialog", None))
        self.depth_label.setText(QCoreApplication.translate("surfacing_Dialog", u"depth\n"
"[units]", None))
        self.length_label.setText(QCoreApplication.translate("surfacing_Dialog", u"length\n"
"[units]", None))
        self.feed_label.setText(QCoreApplication.translate("surfacing_Dialog", u"feed rate\n"
"[units/min]", None))
        self.rpm_label.setText(QCoreApplication.translate("surfacing_Dialog", u"rpm", None))
        self.unit_label.setText(QCoreApplication.translate("surfacing_Dialog", u"units", None))
        self.create_pushButton.setText(QCoreApplication.translate("surfacing_Dialog", u"create gcode", None))
    # retranslateUi

