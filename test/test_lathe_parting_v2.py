#!/usr/bin/env python3

from matplotlib import pyplot as plt
from lathe_parting_v2 import LathePartingV2
import unittest


class test_LathePartingV2(unittest.TestCase):

    def setUp(self):
        self.lp = LathePartingV2()

    def setConditions(self):
        self.lp.set_spi(30)
        self.lp.set_units('in')
        self.lp.set_offset('G55')
        self.lp.set_diameter(1)
        self.lp.set_init_feed(0.055)
        self.lp.set_surf_speed(1500)
        self.lp.calibrate()

    def test_set_units(self):
        with self.assertRaises(ValueError):
            self.lp.set_units('m')
        self.lp.set_units('mm')
        self.assertEqual(self.lp._units, 'G21')

    def test_set_offset(self):
        with self.assertRaises(ValueError):
            self.lp.set_offset('G30')
        self.lp.set_offset('G55')
        self.assertEqual(self.lp._offset, 'G55')

    def test_set_diameter(self):
        with self.assertRaises(ValueError):
            self.lp.set_diameter(1)
        self.lp.set_units('mm')
        self.lp.set_diameter(25.4)

    def test_set_surf_speed(self):
        sim = float(1500)  # rpm
        with self.assertRaises(ValueError):
            self.lp.set_surf_speed(sim)
        self.lp.set_units('mm')
        self.lp.set_surf_speed(sim)
        # test if it handles converting
        # mm -> in
        self.assertEqual(self.lp._sim, sim/25.4)

    def test_set_init_feed(self):
        init_feed = float(0.055)  # in/min
        with self.assertRaises(ValueError):
            self.lp.set_init_feed(init_feed)
        self.lp.set_units('in')
        self.lp.set_init_feed(init_feed)
        self.assertEqual(self.lp._feed, init_feed)

    def test_set_spi(self):
        with self.assertRaises(TypeError):
            self.lp.set_spi(30.1)
        self.lp.set_spi(30)
        self.assertEqual(self.lp.spi, 30)

    def test_calibrate(self):
        self.lp.set_units('in')
        self.lp.set_init_feed(0.055)
        self.lp.set_diameter(1)
        self.lp.set_spi(30)
        self.lp.calibrate()

    def test_discretize(self):
        x, y = [0, 1, 2], [0, -1, -2]
        result = self.lp.discretize(x,y)
        with self.assertRaises(ValueError):
            self.lp.discretize(x, y[1:])

    def test_linear_calc(self):
        self.setConditions()
        x, y = self.lp.linear_calc()
        self.assertEqual(x[-1], 0.5)

    def test_get_feed(self):
        self.setConditions()
        self.lp.get_feed(0.50)

    def test_log_calc(self):
        self.setConditions()
        x, y = self.lp.log_calc()
        x1, y1 = self.lp.linear_calc()
        self.assertEqual(y[0], y1[0])

    def test_generate_gcode(self):
        self.setConditions()
        radi, feeds = self.lp.log_calc()
        gcode = self.lp.generate_gcode(radi, feeds)
        self.assertEqual('%', gcode[-1])