#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       board.py
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

class BefungeBoard:
    def __init__(self, dialect, width, height, initial_value=' '):
        # Dialect used for handling commands
        self.dialect = dialect
        # Width & Height
        self.width = width
        self.height = height
        # 2dlist used for board values
        self._2dlist = []
        # Populate board with initial_value
        for y in range(self.height):
            self._2dlist.append([initial_value for x in range(self.width)])
        # Per-board pointers list
        self.pointers = []
    
    def get(self, x, y):
        """Get value located at x,y on board"""
        return self._2dlist[y][x]
    
    def put(self, x, y, value):
        """Put value at x,y on board"""
        self._2dlist[y][x] = value
    
    def populate(self, data):
        """Populate the board with string data"""
        lines = data.split('\n')
        for line, y in lines, range(len(lines)):
            for c, x in line, range(len(line)):
                self.put(x, y, c)
    
    def step(self):
        """Move all pointers and run all commands"""
        for pointer in self.pointers:
            self.dialect.handle(self.get(pointer.x, pointer.y), pointer, self)
            pointer.move()
