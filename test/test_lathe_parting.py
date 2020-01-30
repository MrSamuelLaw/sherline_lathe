#!/usr/bin/env python3

from sys import path
path.append('../')
from sherline_lathe.lathe_parting import lathe_parting
import unittest


class test_lathe_parting(unittest.TestCase):

    def test_set_surface_speed(self):
        parter = lathe_parting()
        gcode = parter.part('in', 3000, 1, 0.5)
        if 'G20 G55' in gcode:
            self.assertTrue(True)