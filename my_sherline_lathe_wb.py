#!/usr/bin/env python
'''known issues
has leading spaces
'''

import pyperclip
import logging
from os.path import join, dirname
from sys import argv
from json import load


from wb.sherline_lathe.gui.sherline_lathe_wb import *
from wb.sherline_lathe.gui.surfacing_dialog import *
from wb.sherline_lathe.gui.parting_dialog import *
from wb.sherline_lathe.gui.embedded_plot import MplCanvas
from wb.sherline_lathe.linuxCNC_formatter import linuxCNCLatheFormatter
from wb.sherline_lathe.lathe_surfacing import lathe_surfacing
from wb.sherline_lathe.lathe_parting_v2 import LathePartingV2
from PySide2.QtWidgets import QFileDialog, QDialog, QWidget, QVBoxLayout, QMessageBox
from PySide2 import QtCore
from inspect import cleandoc


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
        load widget to run inside parent
        """

        self._logger.info('getting sherline lathe wb ready for parent')
        self.load_parent_elments(parent)
        self.setupUi(self.wb_widget)

        # put functions here
        self.format_button.clicked.connect(self.format_file)
        self.surfacing_pushButton.clicked.connect(self.surface_script)
        self.parting_pushButton.clicked.connect(self.parting_script_v2)
        self.tool_table_pushButton.clicked.connect(self.generate_tool_table)

        # return instance to parent so that the
        # parent can keep it alive, otherwise it dies immediatly
        return self

    def format_file(self):
        """
        implement sw_to_linuxCNC_formatter
        """

        self._logger.info('formatting gcode to run on linuxCNC')
        self.plainTextEdit = self.get_current_plainTextEdit()
        # definition is from the sw2linuxcnc module
        contents = self.plainTextEdit.toPlainText()
        offset = str(self.offset_field.text()).rstrip()
        if self.mm_radiobutton.isChecked():
            units = 'mm'
        else:
            units = 'in'

        formatter = linuxCNCLatheFormatter()
        try:
            contents = formatter.auto_format(
                contents,
                units,
                offset,
                lnums=self.number_checkbox.isChecked()
            )
        except (ValueError, AttributeError) as e:
            QMessageBox.critical(
                None,
                'CRITICAL ERROR',
                str(e)
            )
        except Exception as e:
            QMessageBox.critical(
                None,
                'CRITICAL ERROR',
                str(e)
            )
        else:
            # start edit block, so text document views as single action
            self.plainTextEdit.textCursor().beginEditBlock()
            self.plainTextEdit.clearText(self.plainTextEdit)
            self.plainTextEdit.insertPlainText(contents.lstrip())
            self.plainTextEdit.textCursor().endEditBlock()

            # open a new tab for the change_log
            self.open()
            self.plainTextEdit = self.get_current_plainTextEdit()
            self.plainTextEdit.insertPlainText("=====CHANGE LOG=====")
            self.plainTextEdit.appendPlainText('\n'.join(formatter.change_log))

    def surface_script(self):
        """
        implement surfacing script using dialog box
        """

        self._logger.debug('launching surfacing dialog')
        # set up the form
        s = lathe_surfacing()
        dialog = QDialog()
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
            # pyperclip.copy(output)
            # open in a new tab
            self.open()
            self.plainTextEdit = self.get_current_plainTextEdit()
            self.plainTextEdit.insertPlainText(output)

    def parting_script_v2(self):
        """
        implement parting script V2 using dialog box
        """

        self._logger.debug('launching parting dialog')

        # set up the form
        lp = LathePartingV2()
        dialog = QDialog()
        dialog.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        dialog.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        form = Ui_parting_dialog()
        form.setupUi(dialog)
        units = ['in', 'mm']
        for u in units:
            form.unit_comboBox.addItem(u)
        gcode = None

        # create the plot and toolbar
        plot = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = plot.get_toolbar(plot)
        plot.axes.set_xlabel("radius [in]")
        plot.axes.set_ylabel("feed [in/min]")
        # create layout for graph
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(plot)
        layout.setContentsMargins(0,0,0,0)
        form.widget.setLayout(layout)
        # add plot to dialog
        form.widget.show()

        # HELPER FUNCTIONS
        def generate():
            """
            helper function to create parting generate plot data
            """

            try:
                # get conditions
                unit = form.unit_comboBox.currentText()
                feed = form.feed_lineEdit.text()
                speed = form.speed_lineEdit.text()
                diameter = form.diameter_lineEdit.text()
                spi = form.spi_lineEdit.text()
                # set conditions
                lp.set_units(unit)
                lp.set_init_feed(feed)
                lp.set_surf_speed(speed)
                lp.set_diameter(diameter)
                lp.set_offset(offset='G55')
                lp.set_spi(spi)
                lp.calibrate()

            except ValueError as e:
                # show message in error window
                QMessageBox.critical(
                    dialog,
                    'WARNING',
                    str(e)
                )
            except Exception as e:
                self._logger.debug(e)

            else:
                # generate text results
                nonlocal gcode
                rad_vals, feed_vals = lp.log_calc()
                gcode = lp.generate_gcode(rad_vals, feed_vals)
                header = gcode.splitlines()[:7] # first seven lines are header
                header = '\n'.join(header)
                form.plainTextEdit.setPlainText(header)
                # generate plot data
                rad_vals, feed_vals = lp.discretize(rad_vals, feed_vals)
                plot.axes.cla()  # clear any old data if it exists.
                rad_vals.append(rad_vals[-1]+lp.overcut)
                feed_vals.append(feed_vals[-1])
                plot.axes.plot(rad_vals, feed_vals)
                plot.axes.set_xlabel("radius [in]")
                plot.axes.set_ylabel("feed [in/min]")
                plot.axes.grid()
                # draw data on plot
                plot.fig.canvas.draw_idle()

        # add functions to form
        form.generatePushButton.clicked.connect(generate)
        form.openPushButton.clicked.connect(dialog.accept)

        # run the form
        if dialog.exec_():
            # if accepted open gcode in new tab
            if gcode:
                try:
                    self.open()
                    self.plainTextEdit = self.get_current_plainTextEdit()
                    self.plainTextEdit.insertPlainText(gcode)
                except Exception as e:
                    self._logger.error(e)
                    # print message to user
                    msg = cleandoc("""
                    error generating gcode
                    view log for details
                    """)
                    QMessageBox.critical(self.wb_widget, 'WARNING', msg)
            else:
                # print message to user
                msg = cleandoc("""
                gcode must be generated before
                opening new tab
                """)
                QMessageBox.critical(self.wb_widget, 'WARNING', msg)

    def generate_tool_table(self):
        """
        generates a linux cnc compatible tool
        table file from the gcode and either opens a browser
        or saves to predfined path in text format
        """

        self._logger.info('generating tool table')
        tool_tbl = []
        tool_tbl_path = None
        with open(join(dirname(__file__),'.config'), 'r') as inFile:
            configs = load(inFile)
            tool_tbl_path = configs['toolcrib_path']

        gcode = self.get_current_plainTextEdit().toPlainText()
        gcode = linuxCNCLatheFormatter().parse_gcode(gcode)

        T_cmds = [x for x in gcode if x[1] == 'code' and x[0][0] == 'T']
        # collect unique tools
        tool_list = []
        for T in T_cmds:
            if T[0] not in tool_list:
                tool_list.append(T[0])
        # generate tool table text
        tool_tbl = []
        for i, T in enumerate(tool_list, start=1):
            tool_tbl.append(f'{T} P{i} X+0.0 Z+0.0;')

        if tool_tbl_path:
            with open(tool_tbl_path, 'w') as outFile:
                outFile.write('\n'.join(tool_tbl))
        else:
            self.open(title='tool_table')
            self.plainTextEdit = self.get_current_plainTextEdit()
            self.plainTextEdit.insertPlainText('\n'.join(tool_tbl))

    def load_parent_elments(self, parent):
        """
        get plainTextEdit and wb_widget from main window
        """

        self._logger.debug('loading pointers to parent elements')
        # to open in a new window
        self.open = parent.open
        # to edit existing documents
        self.get_current_plainTextEdit = parent.get_current_plainTextEdit
        self.set_current_document_id = parent.set_current_document_id
        # to put self into parents container
        self.wb_widget = parent.wb_widget
