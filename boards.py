#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       boards.py
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

import os
import random
import sys
import time

from StringIO import StringIO

from funge import Pointer

class Befunge93Board:
    """A Befunge-93 board"""
    def __init__(self, width, height, debug=False, debug_delay=-1):
        self.pointer = Pointer()
        self._list = []
        # Fill board with whitespace
        for y in range(height):
            self._list.append([' '] * width)
        self.width = width
        self.height = height
        
        self.debug = debug
        self.debug_delay = debug_delay
        self.debugstream = StringIO()
    
    def get(self, x, y):
        # Return space if out of bounds
        if x >= self.width or y >= self.height or x < 0 or y < 0:
            return ' '
        return self._list[y][x]
    
    def put(self, x, y, value):
        # Ignore if out of bounds
        if x >= self.width or y >= self.height or x < 0 or y < 0:
            return
        self._list[y][x] = value
    
    def step(self):
        if self.debug:
            # Redirect output for debugging
            sys.stdout = self.debugstream
        
        c = self.get(self.pointer.x, self.pointer.y)
        if c == '"':
            self.pointer.stringmode = not self.pointer.stringmode
        elif self.pointer.stringmode:
            self.pointer.stack.push(ord(c))
        elif c in "0123456789":
            self.pointer.stack.push(int(c))
        elif c == '>':
            self.pointer.dx = 1
            self.pointer.dy = 0
        elif c == '<':
            self.pointer.dx = -1
            self.pointer.dy = 0
        elif c == '^':
            self.pointer.dx = 0
            self.pointer.dy = -1
        elif c == 'v':
            self.pointer.dx = 0
            self.pointer.dy = 1
        elif c == '?':
            dir = ['>', 'v', '<', '^'][random.randint(0, 3)]
            if dir == '>':
                self.pointer.dx = 1
                self.pointer.dy = 0
            elif dir == '<':
                self.pointer.dx = -1
                self.pointer.dy = 0
            elif dir == '^':
                self.pointer.dx = 0
                self.pointer.dy = -1
            elif dir == 'v':
                self.pointer.dx = 0
                self.pointer.dy = 1
        elif c == '+':
            self.pointer.stack.push(self.pointer.stack.pop() + self.pointer.stack.pop())
        elif c == '*':
            self.pointer.stack.push(self.pointer.stack.pop() * self.pointer.stack.pop())
        elif c == '-':
            a = self.pointer.stack.pop()
            b = self.pointer.stack.pop()
            self.pointer.stack.push(b - a)
        elif c == '/':
            a = self.pointer.stack.pop()
            b = self.pointer.stack.pop()
            self.pointer.stack.push(b / a)
        elif c == '%':
            a = self.pointer.stack.pop()
            b = self.pointer.stack.pop()
            self.pointer.stack.push(b % a)
        elif c == '!':
            x = self.pointer.stack.pop()
            if x == 0:
                self.pointer.stack.push(1)
            else:
                self.pointer.stack.push(0)
        elif c == '`':
            a = self.pointer.stack.pop()
            b = self.pointer.stack.pop()
            if b > a:
                self.pointer.stack.push(1)
            else:
                self.pointer.stack.push(0)
        elif c == '_':
            x = self.pointer.stack.pop()
            if x == 0:
                self.pointer.dx = 1
                self.pointer.dy = 0
            else:
                self.pointer.dx = -1
                self.pointer.dy = 0
        elif c == '|':
            x = self.pointer.stack.pop()
            if x == 0:
                self.pointer.dx = 0
                self.pointer.dy = 1
            else:
                self.pointer.dx = 0
                self.pointer.dy = -1
        elif c == ':':
            x = self.pointer.stack.pop()
            self.pointer.stack.push(x)
            self.pointer.stack.push(x)
        elif c == '\\':
            a = self.pointer.stack.pop()
            b = self.pointer.stack.pop()
            self.pointer.stack.push(a)
            self.pointer.stack.push(b)
        elif c == '$':
            self.pointer.stack.pop()
        elif c == '.':
            x = self.pointer.stack.pop()
            sys.stdout.write(str(x) + ' ')
        elif c == ',':
            x = self.pointer.stack.pop()
            sys.stdout.write(chr(x))
        elif c == '#':
            self.pointer.move()
        elif c == 'p':
            y = self.pointer.stack.pop()
            x = self.pointer.stack.pop()
            v = self.pointer.stack.pop()
            # Simulate unsigned 8-bit integer
            # Also guarantees value is in ASCII range
            while v > 255:
                v = 255 - v
            while v < 0:
                v += 255
            self.put(x, y, chr(v))
        elif c == 'g':
            y = self.pointer.stack.pop()
            x = self.pointer.stack.pop()
            self.pointer.stack.push(ord(self.get(x, y)))
        elif c == '&':
            x = raw_input()
            try:
                self.pointer.stack.push(int(x))
            except ValueError:
                self.pointer.stack.push(0)
        elif c == '~':
            x = sys.stdin.read(1)
            self.pointer.stack.push(ord(x))
        elif c == '@':
            self.pointer.dx = 0
            self.pointer.dy = 0
        
        # Advance pointer
        self.pointer.move()
        
        # Wrap-around
        if self.pointer.x >= self.width:
            self.pointer.x -= self.width
        elif self.pointer.x <= -1:
            self.pointer.x += self.width
        elif self.pointer.y >= self.height:
            self.pointer.y -= self.height
        elif self.pointer.y <= -1:
            self.pointer.y += self.height
        
        # Print debugging information
        if self.debug:
            # Reset debugging output redirection
            sys.stdout = sys.__stdout__
            # Clear screen
            if os.name == "posix":
                sys.stdout.write("\x1b[H\x1b[2J")
            print "Pointer: x=%d y=%d dx=%d dy=%d stringmode=%s" % (self.pointer.x, self.pointer.y, self.pointer.dx, self.pointer.dy, self.pointer.stringmode)
            print "Board:"
            for y in range(self.height):
                for x in range(self.width):
                    c = self.get(x, y)
                    if x == self.pointer.x and y == self.pointer.y:
                        if os.name == "posix":
                            sys.stdout.write("\033[41m")
                    sys.stdout.write(c)
                    if os.name == "posix":
                        sys.stdout.write("\033[0m")
                sys.stdout.write('\n')
            print "Stack:"
            print self.pointer.stack._list
            print "Output:"
            self.debugstream.seek(0)
            print self.debugstream.read()
            if self.debug_delay == -1:
                sys.stdin.read(1)
            else:
                time.sleep(self.debug_delay / 1000.0)

