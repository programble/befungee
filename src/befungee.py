#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       befungee.py
#       
#       Copyright 2010 Curtis (Programble) <programble@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

__version__ = "0.2.0a"

from optparse import OptionParser
import sys

import board
from pointer import InstructionPointer
from dialects import *

def version_info():
    # GNU Coding guidelines suggests:
    # GNU hello 2.3
    # Copyright (C) 2007 Free Software Foundation, Inc.
    # License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
    # This is free software: you are free to change and redistribute it.
    # There is NO WARRANTY, to the extent permitted by law.
    print "Befungee", __version__
    print "Copyright (C) 2010 Curtis (Programble) <programble@gmail.com>"
    print "License GPLv3: GNU GPL version 3 <http://gnu.org/licenses/gpl.html>"
    print "This is free software: you are free to change and redistribute it."
    print "There is NO WARRANTY, to the extent permitted by law."

def main():
    # Parse command line options
    parser = OptionParser(usage="%prog [options] [file]")
    parser.add_option("--version", dest="version", action="store_true", default=False, help="Print version info and exit")
    parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Run with debugger")
    parser.add_option("--b93", "--befunge-93", dest="dialect", action="store_const", const=befunge93.Befunge93Dialect, default=befunge93.Befunge93Dialect, help="Use the Befunge-93 dialect (Default)")
    parser.add_option("-w", "--width", "-c", "--columns", dest="width", action="store", type="int", default=80, help="Width of board (Default 80)")
    parser.add_option("--height", "-r", "--rows", dest="height", action="store", type="int", default=25, help="Height of board (Default 25)")
    (options, args) = parser.parse_args()
    
    if options.version:
        version_info()
        sys.exit()
    
    # Initialize board
    main_board = board.BefungeBoard(options.dialect(), options.width, options.height, options.debug)
    # Initialze pointer
    main_board.pointers.append(InstructionPointer())
    
    # Load up file
    if len(args) >= 1:
        f = open(args[0], 'r')
        data = f.read()
        f.close()
        main_board.populate(data)
    else:
        # Read from stdin
        data = ""
        while True:
            x = sys.stdin.read(1)
            if x == '':
                break
            else:
                data += x
        main_board.populate(data)
    
    # Main execution loop
    while True:
        # Process all pointers
        main_board.step()
        
        # If all pointers are dead, exit
        mass_murder = True
        for pointer in main_board.pointers:
            if pointer.dx != 0 or pointer.dy != 0:
                mass_murder = False
        if mass_murder:
            sys.exit()
        

if __name__ == '__main__':
	main()
