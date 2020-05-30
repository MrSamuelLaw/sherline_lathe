#!/usr/bin/env python3


import logging
import matplotlib.pyplot as plt
from math import floor, pi, log
from inspect import cleandoc


class LathePartingV2():
    """
    General overview:
        Parting on a lathe is one of the most difficult operations
        when using a cnc lathe. The difficulty of parting is compounded if using
        an extremely small or low powered lathe.
        With lower powered lathes, the motor can be over torqed as the reduction
        in diameter as the parting knife advances causes the surface speed to
        go down, this in turn increases the chip thickness if the feed rate is held
        constant. Once the chip thickness reaches a critical value, the motor will
        no longer be able to maintain the specified rpms and can throw the piece
        or lock up. To accomidate this, the LathePartingV2 class provides
        two methods for reducing feed rate as a function of radius.

        linear_calc() holds the ratio of surface speed to feed rate constant
            this works, however it does take a long time to complete, and
            causes tool rubbing toward the end of the parting.
        log_calc() uses a logarithmic reduction in feed rate in an attempt to
            match the torque of the motor through the entire parting opertion.
            This method is much faster, and prevents tool rub.

        Both methods use the initial feedrate and surface speed to calibrate off of.
        It other words, they use those initial conditions to account for both the tool
        capabilities and the material machinability.

    inputs:
        units: in or mm
        diameter: float or int
        initial surface speed: float or int
        inital feed rate: float or int
        segments per inch: int
        offset: must be in offset list

    outputs:
        gcode based on data points

    todo:
        -capture C values for testing conditions that work
        -capture product of initial_feed*initial_sim
        -use the above values to only require sim, diameter, and material
         in order to provide usable gcode.
    """

    __offset_list = 'G54, G55, G56, G57, G58, G59, G59.1, G59.2, G59.3'


    def __init__(self):
        self.logger = logging.getLogger('log')
        self.logger.debug("lathe_parting initialized")

        # these properties can be overridden as needed
        self.start_point = 0.05  # start 0.05 inches from the part
        self.overcut = 0.05  # cut past by this much

    def set_units(self, unit):
        """set unit measurements"""
        if unit.lower() == 'in':
            self._units = 'G20'
            self.logger.debug('units set to inches')
        elif unit.lower() == 'mm':
            self._units = 'G21'
            self.logger.debug('units set to millimeters')
        else:
            raise ValueError(f'{unit} is not mm or in...')

    def set_offset(self, offset='G55'):
        if offset in self.__offset_list.split(', '):
            self._offset = offset
            self.logger.debug(f'offset set to {offset}')
        else:
            raise ValueError(f'{offset} is not valid\noptions are {self.__offset_list}')

    def set_diameter(self, diameter):
        """set stock diameter"""
        if hasattr(self, '_units'):  # check if units are set
            self.diameter = float(diameter)
            if self._units == 'G21':
                self.diameter = self.diameter/25.4
            self.logger.debug(f'diameter set to {self.diameter}')
        else:
            raise ValueError('units are not set')

    def set_surf_speed(self, speed):
        """set surface inches per minute"""
        if hasattr(self, '_units'):
            self._sim = float(speed)
            if self._units == 'G21':
                self._sim = speed/25.4
            self.logger.debug(f'surface ipm set to {self._sim}')
        else:
            raise ValueError('units not set')

    def set_init_feed(self, feed):
        """set initial feed rate"""
        if hasattr(self, '_units'):
            self._feed = float(feed)
            if self._units == 'G21':
                self._feed = feed/25.4
            self.logger.debug(f'initial feedrate set to {self._feed} in/min')
        else:
            raise ValueError('units not set')

    def set_spi(self, spi):
        """
        takes an integer number to define segments per inch
        """
        if isinstance(spi, int):
            self.spi = spi
            self.logger.debug(f'spi set to {spi}')
        else:
            raise TypeError("spi must be integer value")

    def calibrate(self):
        """
        uses the inital conditions to calculate the value of C,
        a coefficient that takes material properties into account
        when generating parting script
        """
        try:
            Fo = self._feed
            Ro = self.diameter/2
            x = 1/self.spi  # intersection point
            self.C = ((1-(x/Ro))*(x - Ro))/log(x/Ro)
            self.logger.debug(f'C = {self.C}')
        except AttributeError:
            raise ValueError('initial feed or diameter not set')

    def discretize(self, x, y, first='x'):
        """
        takes a list with a vector of x points, and
        vector of y points and generates points to produce
        flat lane links between points
        if first = x, it interpolates the points by moving x
        first, y second.
        example:
        x, y = [0, 1], [0, -1]
        return [<x>[0,1,1],<y>[0, 0, -1]]
        the number of points will always return
        6*(n_given per vector -1)
        """

        if len(x) != len(y):
            raise ValueError('x and y vector lengths do not match')

        x_vals, y_vals = [], []
        if first == 'x':
            for x1, x2, y1, y2 in zip(x, x[1:], y, y[1:]):
                x_vals.extend([x1, x2, x2])
                y_vals.extend([y1, y1, y2])
        else:
            for x1, x2, y1, y2 in zip(x, x[1:], y, y[1:]):
                x_vals.extend([x1, x1, x2])
                y_vals.extend([y1, y2, y2])

        # fig, ax = plt.subplots()
        # ax.plot(x_vals, y_vals)
        return x_vals, y_vals

    def linear_calc(self):
        """linear equation calculator"""
        # general form F = Fo(1 - R/Ro)

        # define
        Fo = self._feed
        Ro = self.diameter/2
        slices = floor(Ro*self.spi)

        rad_vals, feed_vals = [], []
        for i in range(slices+1):
            R = i/self.spi
            rad_vals.append(R)
            F = Fo*(1-(R/Ro))
            feed_vals.append(F)

        return rad_vals, feed_vals

    def log_calc(self):
        """
        calculates the data points necessary for a logarithmic
        reduction in feed rate.
        returns (rad_values, feed_values)
        """
        # define constants
        Fo = self._feed
        C = self.C  # constant from initial conditions
        Ro = self.diameter/2
        slices = floor(Ro*self.spi)  # total number of slices

        r_vals, feed_vals = [0], [Fo] # starting feed
        for i in range(1, (slices)):
            # calculate radius and feed
            radius = i/self.spi
            feed = self.get_feed(radius)
            r_vals.append(radius)
            feed_vals.append(feed)

        return r_vals, feed_vals

    def get_feed(self, R):
        """
        takes a float value or radius R and
        returns feedrate using logmarithmic formula
        """
        # genearl form F = [C*ln(Ro/R)/(Ro - R)]
        try:
            log_feed = (self.C*self._feed*log(R/(self.diameter/2)))/(R - (self.diameter/2))
            return log_feed
        except ZeroDivisionError:
            return self._feed

    def generate_gcode(self, r_vals, f_vals):
        """
        takes two equal length vectors, one of the cut radius
        one of the feed at which to cut and returns lathe gcode
        to perform specified operation
        """

        # calculate operation total time
        total_time = []
        last_point = self.start_point  # account for approach time
        for R, F in zip(r_vals, f_vals):
            time_delta = (abs(last_point - R))/F
            total_time.append(time_delta)
            last_point = R
        total_time.append(  # account for for overcut time
            abs(last_point - self.overcut)/f_vals[-1]
        )
        total_time = sum(total_time)

        # create gcode header
        header = cleandoc(f"""
            (auto generated parting script using...)
            (slices per inch: {self.spi})
            (inital feed: {self._feed:0.4f} ipm)
            (surface speed: {self._sim:0.1f} surface inches/min)
            (nominal diameter: {self.diameter:0.4f} in)
        """)

        gcode = [header]

        # insert time estimate
        gcode.append(f'\n(total parting time = {total_time:0.2f} min)\n')

        # safety line => units, offset, spindlemode, feedmode, workplane
        gcode.append(f'{self._units} {self._offset} G97 G94 G18')

        # move to starting position
        gcode.append(f'G01 X{self.start_point}')

        # force user to set rpms before continuing
        rpm = self._sim/(pi*self.diameter)
        gcode.append(f'(MSG, please set speed to {int(rpm)} RPM)')
        gcode.append(f'S{int(rpm)} M0')  # M0 is forced pause

        # generate gcode from data points
        for R, F in zip(r_vals, f_vals):
            gcode.append(
                f'G01 X-{R:0.2f} F{F:0.4f}, (t = {1/(self.spi*F):0.2f})'
            )

        # add an overcut to ensure it cuts nub
        gcode.append(f'G01 X-{(r_vals[-1]+self.overcut):.2f}')

        # retract back and end the program
        gcode.append('G01 X0.05 F30')
        gcode.append('M30')
        gcode.append('%')

        # return gcode to calling program
        return '\n'.join(gcode)



