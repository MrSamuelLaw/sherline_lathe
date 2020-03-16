#!/usr/bin/env python

'''
macro to create surfacing passes for learners
that zeros at the part surface
'''


import math
import logging


class lathe_surfacing():
    """
    generates gcode for parting stock with lathe
    """

    unit_dict = {"in": "G20", "mm": "G21"}
    _units = None
    _work_plane = "G18"  # G18 is the xz plane which is a constant on a lathe
    _eof_list = ["M2", "M30"]  # End Of File
    _spindle_mode = 'G97'  # G97 is const rpm mode
    _pass_depth = None
    _rpm = None
    _feed = None

    def __init__(self):
        self._logger = logging.getLogger('log')

    def surface(self, units, depth, length, rpm, feed):
        """
        generate parting gcode using input parameters
        """

        self._logger.info('generating surfacing gcode')
        self._set_units(units)
        self._set_rpm(rpm)
        self._set_feed(feed)
        self._set_length(length)
        self._set_depth(depth)
        gcode = self._get_gcode()
        self._logger.info('surfacing gcode generated successfully')
        return gcode

    def _set_units(self, units):
        """
        sets units
        """

        if units.lower() not in self.unit_dict.keys():
            self._logger.debug("unit options are in or mm")
        else:
            self._units = units.lower()
            self._logger.debug("units set to {}".format(self._units))

    def _set_depth(self, depth):
        """
        set surfacing total depth
        """

        if self._units == 'mm':
            self._depth = depth/25.4
        elif self._units == 'in':
            self._depth = depth
        else:
            return "units not set"
        self._logger.debug(f'depth set to {self._depth}')

    def _set_length(self, length):
        """
        set axial length of stock to surface
        """

        if self._units == 'mm':
            self._length = length/25.4
        elif self._units == 'in':
            self._length = length
        else:
            return "units not set"
        self._logger.debug(f'length set to {self._length}')

    def _set_rpm(self, rpm):
        """
        set rpm at which to perform surfacing
        """

        self._rpm = rpm
        self._logger.debug(f'rpm to to {self._rpm}')

    def _set_feed(self, feed):
        """
        set axial feedrate
        """

        if self._units == 'mm':
            self._feed = feed/25.4
        elif self._units == 'in':
            self._feed = feed
        else:
            return "units not set"
        self._logger.debug(f'axial feedrate set to {self._feed}')

    def _get_gcode(self):
        """
        generate gcode based on input parameters
        """

        if self._units and self._length and self._depth is not None:
            # set the safety line for the script
            safty_line = ("{0} G55 {1} {2}".format(self.unit_dict[self._units],
                                                   self._work_plane,
                                                   self._spindle_mode))
        # set a safe return point for each pass
        start_point = 'G00 X0.05 Z0.05\n'
        pass_depth = 0.01  # constant and in inches
        passes = self._depth/pass_depth
        whole_passes = math.floor(passes)  # get int # of passes
        gcode = '(initial surfacing script)\n'
        gcode += safty_line+'\n'
        gcode += '(MSG, load surfacing tool)\nM0\n'  # pause for tool & rpm
        gcode += '(MSG, set rpm to {0:.4f})\nM0\n'.format(self._rpm)
        gcode += start_point
        for i in range(1, whole_passes):  # create gcode for all the passes
            # move in the x
            gcode += 'G01 X{0:.4f} F{1:.4f}\n'.format(
                                              (-i*pass_depth), self._feed)
            # move in the z
            gcode += 'G01 Z{0:.4f} F{1:.4f}\n'.format(
                                              -self._length, self._feed)
            # retract in the z
            gcode += 'G00 X0\n'
            gcode += start_point
        # do the final pass
        gcode += 'G01 X{0:.4f} F{1:.4f}\n'.format((-self._depth), self._feed)
        gcode += 'G01 Z{0:.4f} F{1:.4f}\n'.format(-self._length, self._feed)
        gcode += 'G00 X0\n'
        # retract
        gcode += start_point
        # append the end of file lines
        gcode += self._eof_list[0] + ' (delete if not at end of of script)'
        gcode += '\n% (delete if not at end of script)\n'
        self._logger.debug('surfacing gcode generated successfully')
        return gcode
