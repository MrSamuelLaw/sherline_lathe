# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sherline_lathe_wb.ui'
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

class Ui_sherline_lathe_workbench(object):
    def setupUi(self, sherline_lathe_workbench):
        if sherline_lathe_workbench.objectName():
            sherline_lathe_workbench.setObjectName(u"sherline_lathe_workbench")
        sherline_lathe_workbench.resize(921, 118)
        self.gridLayout_2 = QGridLayout(sherline_lathe_workbench)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.parting_pushButton = QPushButton(sherline_lathe_workbench)
        self.parting_pushButton.setObjectName(u"parting_pushButton")
        self.parting_pushButton.setMinimumSize(QSize(100, 0))

        self.gridLayout_2.addWidget(self.parting_pushButton, 0, 6, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 8, 1, 1)

        self.surfacing_pushButton = QPushButton(sherline_lathe_workbench)
        self.surfacing_pushButton.setObjectName(u"surfacing_pushButton")
        self.surfacing_pushButton.setMinimumSize(QSize(100, 0))

        self.gridLayout_2.addWidget(self.surfacing_pushButton, 0, 7, 1, 1)

        self.line = QFrame(sherline_lathe_workbench)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line, 0, 4, 1, 1)

        self.offset_field = QLineEdit(sherline_lathe_workbench)
        self.offset_field.setObjectName(u"offset_field")
        self.offset_field.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_2.addWidget(self.offset_field, 0, 2, 1, 1)

        self.tool_table_pushButton = QPushButton(sherline_lathe_workbench)
        self.tool_table_pushButton.setObjectName(u"tool_table_pushButton")
        self.tool_table_pushButton.setMinimumSize(QSize(100, 0))

        self.gridLayout_2.addWidget(self.tool_table_pushButton, 0, 5, 1, 1)

        self.widget = QWidget(sherline_lathe_workbench)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.in_radiobutton = QRadioButton(self.widget)
        self.in_radiobutton.setObjectName(u"in_radiobutton")
        self.in_radiobutton.setChecked(True)

        self.gridLayout.addWidget(self.in_radiobutton, 0, 1, 1, 1)

        self.number_checkbox = QCheckBox(self.widget)
        self.number_checkbox.setObjectName(u"number_checkbox")
        self.number_checkbox.setChecked(True)

        self.gridLayout.addWidget(self.number_checkbox, 0, 3, 1, 1)

        self.mm_radiobutton = QRadioButton(self.widget)
        self.mm_radiobutton.setObjectName(u"mm_radiobutton")

        self.gridLayout.addWidget(self.mm_radiobutton, 0, 2, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)

        self.label = QLabel(sherline_lathe_workbench)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 3, 1, 1)

        self.format_button = QPushButton(sherline_lathe_workbench)
        self.format_button.setObjectName(u"format_button")
        self.format_button.setMaximumSize(QSize(125, 16777215))

        self.gridLayout_2.addWidget(self.format_button, 0, 1, 1, 1)


        self.retranslateUi(sherline_lathe_workbench)

        QMetaObject.connectSlotsByName(sherline_lathe_workbench)
    # setupUi

    def retranslateUi(self, sherline_lathe_workbench):
        sherline_lathe_workbench.setWindowTitle(QCoreApplication.translate("sherline_lathe_workbench", u"Form", None))
        self.parting_pushButton.setText(QCoreApplication.translate("sherline_lathe_workbench", u"parting", None))
        self.surfacing_pushButton.setText(QCoreApplication.translate("sherline_lathe_workbench", u"surfacing", None))
        self.offset_field.setText(QCoreApplication.translate("sherline_lathe_workbench", u"G54", None))
        self.offset_field.setPlaceholderText("")
        self.tool_table_pushButton.setText(QCoreApplication.translate("sherline_lathe_workbench", u"make tool table", None))
        self.label_2.setText(QCoreApplication.translate("sherline_lathe_workbench", u"units", None))
        self.in_radiobutton.setText(QCoreApplication.translate("sherline_lathe_workbench", u"in", None))
        self.number_checkbox.setText(QCoreApplication.translate("sherline_lathe_workbench", u"numbered\n"
"    lines", None))
        self.mm_radiobutton.setText(QCoreApplication.translate("sherline_lathe_workbench", u"mm", None))
        self.label.setText(QCoreApplication.translate("sherline_lathe_workbench", u"offset\n"
"(defaults to G54)", None))
        self.format_button.setText(QCoreApplication.translate("sherline_lathe_workbench", u"format", None))
    # retranslateUi

