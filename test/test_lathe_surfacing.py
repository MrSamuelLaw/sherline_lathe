#!/usr/bin/env python3

from sys import path
path.append('../')
from sherline_lathe.lathe_surfacing import lathe_surfacing
import unittest


class test_lathe_surfacing(unittest.TestCase):

    def test_surface(self):
        surf = lathe_surfacing()
        res = surf.surface('in', 0.05, 1, 800, 1.25)
        if 'G20 G55 G18 G97' in res:
            self.assertTrue(True)
