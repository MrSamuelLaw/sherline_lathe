#!/usr/bin/env python

from linuxCNC_formatter import linuxCNCLatheFormatter
import unittest
from os import path
from inspect import cleandoc


class test_linuxCNCLatheFormatter(unittest.TestCase):

    def setUp(self):
        self.lf = linuxCNCLatheFormatter()

    def loadTestFile(self, fname="nc_no_edits.nc"):
        path_ = path.join('./test/nc_test_files', fname)
        with open(path_, 'r') as inFile:
            return inFile.read()

    def test_init(self):
        self.assertTrue(self.lf._comment_flags)

    def test_parse_text(self):
        text = self.loadTestFile()
        self.lf.parse_text(text)
        with self.assertRaises(AttributeError):
            self.lf.parse_text(text)
        self.lf.clear()
        self.lf.parse_text(text)

    def test_find_B_cmds(self):
        with self.assertRaises(AttributeError):
            self.lf.find_B_cmds()
        self.lf.parse_text(self.loadTestFile())
        res = self.lf.find_B_cmds()
        self.assertTrue(res)

    def test_set_units(self):
        with self.assertRaises(ValueError):
            self.lf.set_units('nan')
        self.lf.set_units('IN')
        with self.assertRaises(AttributeError):
            self.lf.set_units('mm')

    def test_set_offset(self):
        with self.assertRaises(ValueError):
            self.lf.set_offset("G59.1")
        self.lf.set_offset('G54')
        with self.assertRaises(AttributeError):
            self.lf.set_offset('G55')

    def test_fix_B_cmds(self):
        # assert it checks for non right angles
        with self.assertRaises(ValueError):
            self.lf.parse_text("B89.")
            self.lf.fix_B_cmds()
        self.lf.clear()
        # assert it recognizes right angles
        okays = cleandoc(
            """
            B0.
            B90.
            B90.
            B180.
            B270.
            """
        )
        self.lf.parse_text(okays)
        self.lf.fix_B_cmds()
        # assert that it can handle empty lists
        self.lf.clear()
        self.lf.parse_text("G59")
        self.lf.fix_B_cmds()

    def test_find_T_cmds(self):
        with self.assertRaises(AttributeError):
            self.lf.find_T_cmds()
        self.lf.parse_text(self.loadTestFile())
        res = self.lf.find_T_cmds()
        self.assertTrue(res)

    def test_fix_T_cmds(self):
        txt = cleandoc(
            """
            T101.8
            T505.5
            """
        )
        self.lf.parse_text(txt)
        self.lf.fix_T_cmds()

    def test_find_T_swap_cmds(self):
        self.lf.parse_text('M6')
        res = self.lf.find_T_swap_cmds()
        self.assertTrue(res)

    def test_find_T_offset_cmds(self):
        self.lf.parse_text('G43')
        res = self.lf.find_T_offset_cmds()
        self.assertTrue(res)

    def test_fix_T_change(self):
        self.lf.parse_text(self.loadTestFile(
            fname='Pin2.nc'
        ))
        self.lf.fix_T_changes()
        len1 = len(self.lf.parsed_text)
        self.lf.fix_T_changes()
        len2 = len(self.lf.parsed_text)
        self.assertEqual(len1, len2)

    def test_find_eof_cmds(self):
        self.lf.parse_text('M2')
        res = self.lf.find_eof_cmds()
        self.assertTrue(res)

    def test_fix_eof_cmds(self):
        self.lf.parse_text(self.loadTestFile())
        self.lf.fix_eof_cmds()

    def test_find_S_cmds(self):
        self.lf.parse_text(self.loadTestFile())
        res = self.lf.find_S_cmds()
        self.assertTrue(res)

    def test_fix_S_cmds(self):
        self.lf.parse_text(self.loadTestFile())
        self.lf.fix_S_changes()
        len1 = len(self.lf.parsed_text)
        self.lf.fix_S_changes()
        len2 = len(self.lf.parsed_text)
        self.assertEqual(len1, len2)

    def test_fix_eof_symbols(self):
        self.lf.parse_text(self.loadTestFile())
        self.lf.fix_eof_symbols()

    def test_next_line_code(self):
        self.lf.parse_text(self.loadTestFile())
        self.lf.next_line_code(5)

    def test_fix_safety_line(self):
        self.lf.parse_text(self.loadTestFile())
        self.lf.set_units('in')
        self.lf.set_offset('G54')
        self.lf.fix_safety_line()

    def test_remove_N_cmds(self):
        self.lf.parse_text(self.loadTestFile())
        self.lf.remove_N_cmds()
        # verify that remove_N_cmds removed all the N_cmds
        self.assertFalse(
            any([x for x in self.lf.parsed_text if (x[1] == 'code') and ('N' in x[0])])
        )

    def test_insert_N_cmds(self):
        self.lf.parse_text(self.loadTestFile())
        self.lf.insert_N_cmds()

    def test_format_file(self):
        formatted = self.lf.auto_format(
                        self.loadTestFile(),
                        'in',
                        'G55'
                    )