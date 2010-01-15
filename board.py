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
    def __init__(self, width, height, initial_value=' '):
        self.width = width
        self.height = height
        self._2dlist = []
        for y in range(self.height):
            _2dlist.append([initial_value for x in range(self.width)])
    
    def get(self, x, y):
        return self._2dlist[y][x]
    
    def put(self, x, y, value):
        self._2dlist[y][x] = value
