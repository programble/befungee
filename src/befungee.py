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
    (options, args) = parser.parse_args()
    
    if options.version:
        version_info()
        sys.exit()

if __name__ == '__main__':
	main()
