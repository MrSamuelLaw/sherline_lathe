#!/bin/usr/env python

'''
python class that reads in user's nc files from solidworks cam
and edits them to be compatible with linuxCNC
'''


import os.path
import logging
from gscrape import gscrape
from math import floor
from inspect import cleandoc
from itertools import chain


class linuxCNCLatheFormatter(gscrape):

    _unit_dict = {"in": "G20", "mm": "G21"}
    _offset_list = ["G54", "G55", "G56", "G57", "G58", "G59"]
    _work_plane = "G18"  # G18 is the xz plane which is a constant on a lathe
    _eof_list = ["M2", "M30"]  # End Of File identifiers
    _spindle_mode = 'G97'  # G97 is const rpm mode

    def __init__(self):
        """
        set gscrape comment flags
        eof flags are also comments
        """

        super(linuxCNCLatheFormatter, self).__init__()

        self.logger = logging.getLogger('log')
        self.change_log = []

        # set up gscrape
        self.add_comment_flag('round', [('(', -1), (')', 1)])
        self.add_comment_flag('semicolon_left', [(';', -2)])
        self.add_comment_flag('eof', [('%', -2)])

    def auto_format(self, text, units, offset):

        # setup
        self.parse_text(text)
        self.set_units(units)
        self.set_offset(offset)

        # run funcs that may find terminal gcode errors
        self.find_terminal_cmds()
        self.fix_B_cmds()

        # run the rest of the formatting funcs
        self.fix_S_changes()
        self.fix_T_changes()
        self.fix_eof_cmds()
        self.fix_safety_line()
        self.remove_N_cmds()
        self.insert_N_cmds()
        self.fix_eof_symbols()
        return self.to_text(self.parsed_text)

    # ------------------------------------------------
    #    _____          _     _
    #   / ____|        | |   | |
    #  | (___     ___  | |_  | |_    ___   _ __   ___
    #   \___ \   / _ \ | __| | __|  / _ \ | '__| / __|
    #   ____) | |  __/ | |_  | |_  |  __/ | |    \__ \
    #  |_____/   \___|  \__|  \__|  \___| |_|    |___/
    # ------------------------------------------------

    def set_units(self, units: str) -> None:
        if hasattr(self, 'units'):
            raise AttributeError("error, units already set...")
        try:
            self.units = self._unit_dict[units.lower()]
        except KeyError:
            raise ValueError(
                f'{units} is invalid unit, options are "in" or "mm"'
            )

    def set_offset(self, offset: str = 'G54') -> None:
        if hasattr(self, 'offset'):
            raise AttributeError("error, offset already set...")
        if offset in self._offset_list:
            self.offset = offset.upper()
        else:
            raise ValueError(
                f'{offset} is invalid offset, options are {self._offset_list}'
            )

    # -------------------------------------------------
    #   ______   _               _   _
    #  |  ____| (_)             | | (_)
    #  | |__     _   _ __     __| |  _   _ __     __ _
    #  |  __|   | | | '_ \   / _` | | | | '_ \   / _` |
    #  | |      | | | | | | | (_| | | | | | | | | (_| |
    #  |_|      |_| |_| |_|  \__,_| |_| |_| |_|  \__, |
    #                                             __/ |
    #                                            |___/
    # -------------------------------------------------

    def find_terminal_cmds(self):
        # list of cmds the lathe cannot handle
        terminal_cmds = [
            'G96'
        ]
        # list of incompatible B_cmds
        B_cmds = self.find_B_cmds()
        terminal_cmds.extend([x[0] for x in B_cmds if float(x[0][1:]) % 90])

        # create readout of all terminal cmds
        results = [x for x in self.parsed_text if (x[0] in terminal_cmds) and (x[1] == 'code')]
        if results:
            for r in results: r[2] += 1
            results.insert(0, ['CMD', 'TYPE', 'LINE'])
            results = '\n'.join([str(x) for x in results])
            raise ValueError(
            "the following cmds are incompatible with the sherline lathe," +
            "please check the settings used in generating the original gcode\n" +
            f"{results}"
        )

    def find_B_cmds(self):
        if hasattr(self, 'parsed_text'):
            result = [x for x in self.parsed_text if (('B' in x[0]) and (x[1] == 'code'))]
            return result
        else:
            raise AttributeError("no attribute parsed_text")

    def find_S_cmds(self):
        if hasattr(self, 'parsed_text'):
            result = [x for x in self.parsed_text if (('S' in x[0]) and (x[1] == 'code'))]
            return result
        else:
            raise AttributeError("no attribute parsed_text")

    def find_T_cmds(self):
        if hasattr(self, 'parsed_text'):
            result = [x for x in self.parsed_text if (('T' in x[0]) and (x[1] == 'code'))]
            return result
        else:
            raise AttributeError("no attribute parsed_text")

    def find_T_swap_cmds(self):
        if hasattr(self, 'parsed_text'):
            result = [x for x in self.parsed_text if (('M6' in x[0]) and (x[1] == 'code'))]
            return result
        else:
            raise AttributeError("no attribute parsed_text")

    def find_T_offset_cmds(self):
        if hasattr(self, 'parsed_text'):
            result = [x for x in self.parsed_text if (('G43' in x[0]) and (x[1] == 'code'))]
            return result
        else:
            raise AttributeError("no attribute parsed_text")

    def find_eof_cmds(self):
        if hasattr(self, 'parsed_text'):
            result = [x for x in self.parsed_text if x[0] in self._eof_list]
            return result
        else:
            raise AttributeError("no attribute parsed_text")

    def find_move_cmds(self):
        if hasattr(self, 'parsed_text'):
            # generate list of move cmds, w and w/o middle zero
            move_cmds = []
            for i in range(4):
                move_cmds.extend([f'G{i}', f'G0{i}'])

            results = [x for x in self.parsed_text if (x[1] == 'code') and (x[0] in move_cmds)]
            return results
        else:
            raise AttributeError("no attribute parsed_text")

    # ----------------------------------------
    #   ______   _          _
    #  |  ____| (_)        (_)
    #  | |__     _  __  __  _   _ __     __ _
    #  |  __|   | | \ \/ / | | | '_ \   / _` |
    #  | |      | |  >  <  | | | | | | | (_| |
    #  |_|      |_| /_/\_\ |_| |_| |_|  \__, |
    #                                    __/ |
    #                                   |___/
    # ----------------------------------------

    def fix_B_cmds(self):
        """
        Removes B cmds if they are integer multiples of 90
        raises an error if they are not
        """
        results = self.find_B_cmds()
        self.log(f"attepmted to fix the following cmds:\n{results}")
        for r in results:
            num = float(r[0][1:])
            if not num % 90.0:
                # angle is a multiple of 90 deg
                self.parsed_text.remove(r)
            else:
                # angle is not a multiple of 90
                raise ValueError(f"B cmd on line {r[2]} not integer multiple of 90")

    def fix_T_cmds(self):
        """
        Removes decimals from T_cmds
        """
        results = self.find_T_cmds()
        self.log(f"attepmted to fix the following cmds:\n{results}")
        for r in results:
            # convert tool numbers to intergers as linuxCNC
            # cannot do floats
            tool_num = float(r[0][1:])
            tool_num = floor(tool_num)
            tool_code = f'T{tool_num}'
            self.parsed_text[self.parsed_text.index(r)][0] = tool_code

    def fix_S_changes(self):
        """
        ensures that there is a forced pause after
        every spindle speed change cmd, along with
        a dialog box so that users may adjust the speed
        prior to continuing.
        """
        S_cmds = self.find_S_cmds()
        self.log(f"attepmted to fix the following cmds:\n{S_cmds}")
        for S in S_cmds:
            rpm = S[0][1:]
            spd_cmds = [
                "M0",
                f"(MSG, please set rpm to {rpm})"
            ]
            next_line = self.next_line(S[2])
            # check if T_swaps and T_offsets are in next line
            if not all(cmd in [x[0] for x in next_line] for cmd in spd_cmds):
                # insert change_cmds if not found
                self.insert_line(
                    self.parsed_text,
                    ' '.join(spd_cmds),
                    (S[2] + 1)
                )

    def fix_T_changes(self):
        """
        The name implies that it "fixes" tool changes,
        however in reality it unsures that when the
        tool number is changed, the machine one, pauses
        unitl the user can manualy change the tool and
        two, applies the appropriate offset for the tool
        """
        self.fix_T_cmds()  # fix T_cmds first

        T_cmds = self.find_T_cmds()
        self.log(f"attepmted to fix the following cmds:\n{T_cmds}")
        change_cmds = [
            'M6',  # tool swap pause
            'G43'  # tool offset update
        ]

        for T in T_cmds:
            next_line = self.next_line_code(T[2])
            # check if T_swaps and T_offsets are in next line
            if not all(cmd in [x[0] for x in next_line] for cmd in change_cmds):
                # insert change_cmds if not found
                self.insert_line(
                    self.parsed_text,
                    ' '.join(change_cmds),
                    (T[2] + 1)
                )

    def fix_eof_cmds(self):
        """
        Ensures that code that will never be run is chopped
        off of the script
        """
        result = self.find_eof_cmds()
        self.log(f"attepmted to remove everythin past: {result[0]}")
        if result:
            # remove everything past first eof cmd
            i = self.parsed_text.index(result[0]) + 1
            del self.parsed_text[i:]
            return
        raise AttributeError("no end of script cmds")

    def fix_eof_symbols(self):
        """
        checks if the last character is a % symbol
        as required by linuxCNC, and if not, adds it
        """
        self.log('ensuring that "%" sign at end of file')
        if hasattr(self, "parsed_text"):
            # delete trailing blank lines
            while not self.parsed_text[-1][0]:
                del self.parsed_text[-1]
            # ensure correct eof symbol
            last_item = self.parsed_text[-1]
            if last_item[0] != "%":
                self.parsed_text.append([
                    '%',
                    'comment',
                    (last_item[2] + 1)
                ])
        else:
            raise AttributeError("no attribute parsed_text")

    def fix_safety_line(self):
        """
        ensures that all elements of a safety line are
        present, even if not on the exact same line
        """
        # get safety line items
        safety_line = [
            self.units,
            self.offset,
            self._work_plane,
            self._spindle_mode
        ]
        self.log(
            f"ensuring all of the following cmds are before any motor cmds:\n{safety_line}"
        )
        # get line items are already in the script
        results = [x for x in self.parsed_text if (x[1] == 'code') and (x[0] in safety_line)]

        # get first S cmd index
        first_S_index = self.parsed_text.index(
            self.find_S_cmds()[0]
        )

        # prevent unneccessary duplicates
        for r in results:
            if self.parsed_text.index(r) <= first_S_index:
                del safety_line[safety_line.index(r[0])]

        # insert safety line
        lnum = self.parsed_text[first_S_index][2]
        self.insert_line(
            self.parsed_text,
            ' '.join(safety_line),
            (lnum - 1)
        )

    # ------------------------------------------------
    #   _    _          _
    #  | |  | |        | |
    #  | |__| |   ___  | |  _ __     ___   _ __   ___
    #  |  __  |  / _ \ | | | '_ \   / _ \ | '__| / __|
    #  | |  | | |  __/ | | | |_) | |  __/ | |    \__ \
    #  |_|  |_|  \___| |_| | .__/   \___| |_|    |___/
    #                      | |
    #                      |_|
    # ------------------------------------------------

    def parse_text(self, text):
        if hasattr(self, 'parsed_text'):
            raise AttributeError(
                """warning gcode already in memory...
                must call clear() to parse new text"""
            )
        self.parsed_text = self.sort_gcode(text)

    def clear(self):
        """
        deletes the parsed_text in memeory
        """
        del self.parsed_text

    def log(self, msg):
        self.change_log.append(msg)

    def next_line(self, current_line: int):
        if hasattr(self, 'parsed_text'):
            lnum = current_line  # where to start from
            for i in range(1, 5):  # limit to 4 tries
                lnum += 1
                result = [x for x in self.parsed_text if (x[1] != 'blank') and (x[2] == lnum)]
                if result:
                    return result  # exit the function if found
            raise IndexError("""
                could not find next line of code from given index
            """)

        else:
            raise AttributeError("no attribute parsed_text")

    def next_line_code(self, current_line: int):
        """
        takes the current line number
        returns next non blank, non comment,
        line of gcode
        """

        if hasattr(self, 'parsed_text'):
            lnum = current_line  # where to start from
            for i in range(1, 5):  # limit to 4 tries
                lnum += 1
                result = [x for x in self.parsed_text if (x[1] == 'code') and (x[2] == lnum)]
                if result:
                    return result  # exit the function if found
            raise IndexError("""
                could not find next line of code from given index
            """)

        else:
            raise AttributeError("no attribute parsed_text")

    def remove_N_cmds(self):
        if hasattr(self, "parsed_text"):
            N_cmds = [x for x in self.parsed_text if (x[1] == 'code') and ('N' in x[0])]
            for N in N_cmds:
                del self.parsed_text[
                        self.parsed_text.index(N)
                    ]
        else:
            raise AttributeError("no attribute parsed_text")

    def insert_N_cmds(self):
        """
        Inserts N cmds back in to the parsed_text.
        * Make sure to call fix_eof_symbols()
          after calling this function
        """
        if hasattr(self, "parsed_text"):
            # remove all line numbers and sequence the list
            self.remove_N_cmds()
            self.parsed_text = self._sequence(self.parsed_text)

            # loop through adding in line numbers
            lnum, offset = 0, 0
            for x in self.parsed_text:
                if (x[2] == lnum):
                    if (x[1] == 'blank'):
                        offset += 1
                    elif "%" not in x[0]:  # if not blank/eof insert N cmd
                        self.parsed_text.insert(
                            self.parsed_text.index(x),
                            [f'N{lnum-offset}', 'code', lnum]
                        )
                    lnum += 1
        else:
            raise AttributeError("no attribute parsed_text")





