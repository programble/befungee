#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       befunge93.py
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

import random

#############
# Callbacks #
#############
def left(pointer, board):
    if not pointer.stringmode:
        pointer.dx = -1
        pointer.dy = 0

def right(pointer, board):
    if not pointer.stringmode:
        pointer.dx = 1
        pointer.dy = 0

def up(pointer, board):
    if not pointer.stringmode:
        pointer.dy = -1
        pointer.dx = 0

def down(pointer, board):
    if not pointer.stringmode:
        pointer.dy = 1
        pointer.dx = 0

def random(pointer, board):
    if not pointer.stringmode:
        [left, right, up, down][random.randint(0,3)](pointer, board)

def toggle_stringmode(pointer, board):
    pointer.stringmode = not pointer.stringmode

def char(pointer, board):
    if pointer.stringmode:
        pointer.stack.push(ord(board.get(pointer.x, pointer.y)))

def int(pointer, board):
    if not pointer.stringmode:
        pointer.stack.push(int(board.get(pointer.x, pointer.y)))

############
# Commands #
############

# Criteria -> Callback
commands = {
            lambda x: x == '"'          : toggle_stringmode,
            lambda x: x != '"'          : char,
            lambda x: x in "0123456789" : int,
            lambda x: x == '?'          : random,
            lambda x: x == '>'          : right,
            lambda x: x == '<'          : left,
            lambda x: x == '^'          : up,
            lambda x: x == 'v'          : down,
}
