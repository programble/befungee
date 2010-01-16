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

from dialect import Dialect

import random
import sys

class Befunge93Dialect(Dialect):
    
    stringmode = False
    
    # Callbacks
    def left(self, pointer, board):
        if not self.stringmode:
            pointer.dx = -1
            pointer.dy = 0

    def right(self, pointer, board):
        if not self.stringmode:
            pointer.dx = 1
            pointer.dy = 0

    def up(self, pointer, board):
        if not self.stringmode:
            pointer.dy = -1
            pointer.dx = 0

    def down(self, pointer, board):
        if not self.stringmode:
            pointer.dy = 1
            pointer.dx = 0

    def random(self, pointer, board):
        if not self.stringmode:
            [self.left, self.right, self.up, self.down][random.randint(0,3)](pointer, board)

    def toggle_stringmode(self, pointer, board):
        self.stringmode = not self.stringmode

    def char(self, pointer, board):
        if self.stringmode:
            pointer.stack.push(ord(board.get(pointer.x, pointer.y)))

    def int(self, pointer, board):
        if not self.stringmode:
            pointer.stack.push(int(board.get(pointer.x, pointer.y)))

    def dup(self, pointer, board):
        if not self.stringmode:
            pointer.stack.push(pointer.stack.peek())

    def bridge(self, pointer, board):
        if not self.stringmode:
            pointer.move()

    def add(self, pointer, board):
        if not self.stringmode:
            pointer.stack.push(pointer.stack.pop() + pointer.stack.pop())

    def multiply(self, pointer, board):
        if not self.stringmode:
            pointer.stack.push(pointer.stack.pop() * pointer.stack.pop())

    def divide(self, pointer, board):
        if not self.stringmode:
            b = pointer.stack.pop()
            a = pointer.stack.pop()
            pointer.stack.push(a / b)

    def subtract(self, pointer, board):
        if not self.stringmode:
            b = pointer.stack.pop()
            a = pointer.stack.pop()
            pointer.stack.push(a - b)

    def modulo(self, pointer, board):
        if not self.stringmode:
            b = pointer.stack.pop()
            a = pointer.stack.pop()
            pointer.stack.push(a % b)

    def greater_than(self, pointer, board):
        if not self.stringmode:
            a = pointer.stack.pop()
            b = pointer.stack.pop()
            if b > a:
                pointer.stack.push(1)
            else:
                pointer.stack.push(0)

    def not_(self, pointer, board):
        if not self.stringmode:
            val = pointer.stack.pop()
            if val != 0:
                pointer.stack.push(0)
            else:
                pointer.stack.push(1)

    def swap(self, pointer, board):
        if not self.stringmode:
            a = pointer.stack.pop()
            b = pointer.stack.pop()
            pointer.stack.push(a)
            pointer.stack.push(b)

    def pop(self, pointer, board):
        if not self.stringmode:
            pointer.stack.pop()

    def output_int(self, pointer, board):
        if not self.stringmode:
            sys.stdout.write(str(pointer.stack.pop()) + " ")

    def output_char(self, pointer, board):
        if not self.stringmode:
            sys.stdout.write(chr(pointer.stack.pop()))

    def input_int(self, pointer, board):
        if not self.stringmode:
            pointer.stack.push(int(raw_input()))

    def input_char(self, pointer, board):
        if not self.stringmode:
            pointer.stack.push(ord(sys.stdin.read(1)))

    def if_horizontal(self, pointer, board):
        if not self.stringmode:
            val = pointer.stack.pop()
            if val == 0:
                self.right(pointer, board)
            else:
                self.left(pointer, board)

    def if_vertical(self, pointer, board):
        if not self.stringmode:
            val = pointer.stack.pop()
            if val == 0:
                self.down(pointer, board)
            else:
                self.up(pointer, board)

    def get(self, pointer, board):
        if not self.stringmode:
            y = pointer.stack.pop()
            x = pointer.stack.pop()
            pointer.stack.push(ord(board.get(x, y)))

    def put(self, pointer, board):
        if not self.stringmode:
            y = pointer.stack.pop()
            x = pointer.stack.pop()
            val = pointer.stack.pop()
            board.put(x, y, val)

    def exit(self, pointer, board):
        pointer.destroy()
    
    # Commands (Criteria -> Callback)
    commands = {
                lambda x: x == '"'          : toggle_stringmode,
                lambda x: x != '"'          : char,
                lambda x: x in "0123456789" : int,
                lambda x: x == '?'          : random,
                lambda x: x == '>'          : right,
                lambda x: x == '<'          : left,
                lambda x: x == '^'          : up,
                lambda x: x == 'v'          : down,
                lambda x: x == ':'          : dup,
                lambda x: x == '#'          : bridge,
                lambda x: x == '+'          : add,
                lambda x: x == '-'          : subtract,
                lambda x: x == '*'          : multiply,
                lambda x: x == '/'          : divide,
                lambda x: x == '%'          : modulo,
                lambda x: x == '`'          : greater_than,
                lambda x: x == '!'          : not_,
                lambda x: x == '\\'         : swap,
                lambda x: x == '$'          : pop,
                lambda x: x == '.'          : output_int,
                lambda x: x == ','          : output_char,
                lambda x: x == '&'          : input_int,
                lambda x: x == '~'          : input_char,
                lambda x: x == '_'          : if_horizontal,
                lambda x: x == '|'          : if_vertical,
                lambda x: x == 'g'          : get,
                lambda x: x == 'p'          : put,
                lambda x: x == '@'          : exit,
    }
