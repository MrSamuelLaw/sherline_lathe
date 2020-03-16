#!/usr/bin/env python
'''known issues
has leading spaces

'''


from wb.sherline_lathe.gui.sherline_lathe_wb import *
from wb.sherline_lathe.gui.surfacing_dialog import *
from wb.sherline_lathe.gui.parting_dialog import *
from wb.sherline_lathe.sw_2_linuxCNC_formatter import sw_2_linuxCNC_formatter
from wb.sherline_lathe.lathe_surfacing import lathe_surfacing
from wb.sherline_lathe.lathe_parting import lathe_parting
from PySide2.QtWidgets import QFileDialog

import pyperclip
import logging


class my_sherline_lathe_wb(Ui_sherline_lathe_workbench):

    def __init__(self):
        """
        set logger
        """

        self._logger = logging.getLogger('log')
        self._logger.info('my_sherline_lathe_wb instantiated')

    def __del__(self):
        """
        notify when self is deleted
        """

        self._logger.info('my_sherline_lathe_wb deleted')

    def run_integrated(self, parent):
        """
        load frame to run inside parent
        """

        self._logger.info('getting sherline lathe wb ready for parent')
        self.load_parent_elments(parent)
        self.setupUi(self.frame)

        # put functions here
        self.text_area.appendPlainText(self.text_area.toPlainText())
        self.format_button.clicked.connect(self.format_file)
        self.surfacing_pushButton.clicked.connect(self.surface_script)
        self.parting_pushButton.clicked.connect(self.parting_script)
        self.tool_table_pushButton.clicked.connect(self.generate_tool_table)

        # return instance to parent so that the
        # parent can keep it alive, otherwise it dies immediatly
        return self

    def format_file(self):
        """
        implement sw_to_linuxCNC_formatter
        """

        self._logger.info('formatting gcode to run on linuxCNC')
        # definition is from the sw2linuxcnc module
        contents = self.text_area.toPlainText()
        offset = str(self.offset_field.text()).rstrip()
        if self.mm_radiobutton.isChecked():
            units = 'mm'
        else:
            units = 'in'
        formatter = sw_2_linuxCNC_formatter()
        contents = formatter.format(contents, units, offset)
        if not self.number_checkbox.isChecked():
            contents = formatter.remove_line_numbers()
        self.text_area.clearText()
        self.text_area.insertPlainText(contents.lstrip())

    def surface_script(self):
        """
        implement surfacing script using dialog box
        """

        self._logger.debug('launching surfacing dialog')
        # set up the form
        s = lathe_surfacing()
        dialog = QtWidgets.QDialog()
        form = Ui_surfacing_Dialog()
        form.setupUi(dialog)
        units = ['in', 'mm']
        for u in units:
            form.unit_comboBox.addItem(u)

        # add functions to the forms buttons
        form.create_pushButton.clicked.connect(dialog.accept)
        if dialog.exec_():
            try:
                unit = form.unit_comboBox.currentText()
                depth = float(form.depth_lineEdit.text())
                length = float(form.length_lineEdit.text())
                feed = float(form.feed_lineEdit.text())
                rpm = float(form.rpm_lineEdit.text())
                output = s.surface(unit, depth, length, rpm, feed)
            except Exception as e:
                output = str(e)
            pyperclip.copy(output)

    def parting_script(self):
        """
        implement parting script using dialog box
        """

        self._logger.debug('launching parting dialog')
        # set up the form
        p = lathe_parting()
        dialog = QtWidgets.QDialog()
        form = Ui_parting_dialog()
        form.setupUi(dialog)
        units = ['in', 'mm']
        for u in units:
            form.unit_comboBox.addItem(u)

        # add functions to the forms buttons
        form.generate_button.clicked.connect(dialog.accept)
        if dialog.exec_():
            try:
                unit = form.unit_comboBox.currentText()
                feed = float(form.feed_lineEdit.text())
                speed = float(form.speed_lineEdit.text())
                diameter = float(form.diameter_lineEdit.text())
                output = p.part(unit, speed, diameter, feed)
            except Exception as e:
                output = str(e)
            pyperclip.copy(output)

    def generate_tool_table(self, text):
        """
        generate linuxCNC tool table from gcode
        """

        self._logger.info('generating tool table')
        contents = self.text_area.toPlainText()
        formatter = sw_2_linuxCNC_formatter()
        formatter.load_contents(contents)
        crib = formatter.make_tool_tbl()
        file_name = 'tool.tbl'
       	browser = QFileDialog()
        browser.setFileMode(QFileDialog.DirectoryOnly)
        if browser.exec_():
            folder = browser.selectedFiles()[0]
            path = str(folder)+'/'+file_name
            print(path)
            with open(path, 'w') as f:
                f.write(crib)

    def load_parent_elments(self, parent):
        """
        get text_area and frame main window
        """

        self._logger.debug('loading pointers to parent elements')
        self.text_area = parent.text_area
        self.frame = parent.frame
