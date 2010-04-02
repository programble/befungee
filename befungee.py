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

import random
import sys
import time

from optparse import OptionParser
from StringIO import StringIO

__version__ = "0.1.3"

class Stack:
    """A basic LIFO stack"""
    def __init__(self):
        self._list = []
    def push(self, item):
        """Push an item onto the top of the stack"""
        self._list = [item] + self._list
    def pop(self):
        """Remove and return the top item on the stack"""
        if self.length() == 0:
            return 0
        item = self._list[0]
        self._list = self._list[1:]
        return item
    def peek(self):
        """Return the top item on the stack without removing it"""
        if self.length() == 0:
            return 0
        return self._list[0]
    def length(self):
        """Return the number of items on the stack"""
        return len(self._list)

class Pointer:
    """A Befunge pointer"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 0
    def move(self):
        self.x += self.dx
        self.y += self.dy

class Board:
    """A Befunge board"""
    def __init__(self, width, height, debug=False, debug_delay=-1):
        self.stack = Stack()
        self.pointer = Pointer()
        self._list = []
        # Fill board with whitespace
        for y in range(height):
            self._list.append([' '] * width)
        self.width = width
        self.height = height
        self.stringmode = False
        
        self.debug = debug
        self.debug_delay = debug_delay
        self.debugstream = StringIO()
    
    def get(self, x, y):
        return self._list[y][x]
    
    def put(self, x, y, value):
        self._list[y][x] = value
    
    def step(self):
        if self.debug:
            # Redirect output for debugging
            sys.stdout = self.debugstream
        
        c = self.get(self.pointer.x, self.pointer.y)
        if c == '"':
            self.stringmode = not self.stringmode
        elif self.stringmode:
            self.stack.push(ord(c))
        elif c in "0123456789":
            self.stack.push(int(c))
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
            self.stack.push(self.stack.pop() + self.stack.pop())
        elif c == '*':
            self.stack.push(self.stack.pop() * self.stack.pop())
        elif c == '-':
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push(b - a)
        elif c == '/':
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push(b / a)
        elif c == '%':
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push(b % a)
        elif c == '!':
            x = self.stack.pop()
            if x == 0:
                self.stack.push(1)
            else:
                self.stack.push(0)
        elif c == '`':
            a = self.stack.pop()
            b = self.stack.pop()
            if b > a:
                self.stack.push(1)
            else:
                self.stack.push(0)
        elif c == '_':
            x = self.stack.pop()
            if x == 0:
                self.pointer.dx = 1
                self.pointer.dy = 0
            else:
                self.pointer.dx = -1
                self.pointer.dy = 0
        elif c == '|':
            x = self.stack.pop()
            if x == 0:
                self.pointer.dx = 0
                self.pointer.dy = 1
            else:
                self.pointer.dx = 0
                self.pointer.dy = -1
        elif c == ':':
            x = self.stack.pop()
            self.stack.push(x)
            self.stack.push(x)
        elif c == '\\':
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push(a)
            self.stack.push(b)
        elif c == '$':
            self.stack.pop()
        elif c == '.':
            x = self.stack.pop()
            sys.stdout.write(str(x))
        elif c == ',':
            x = self.stack.pop()
            sys.stdout.write(chr(x))
        elif c == '#':
            self.pointer.move()
        elif c == 'p':
            y = self.stack.pop()
            x = self.stack.pop()
            v = self.stack.pop()
            self.put(x, y, chr(v))
        elif c == 'g':
            y = self.stack.pop()
            x = self.stack.pop()
            self.stack.push(ord(self.get(x, y)))
        elif c == '&':
            x = raw_input()
            try:
                self.stack.push(int(x))
            except ValueError:
                self.stack.push(0)
        elif c == '~':
            x = sys.stdin.read(1)
            self.stack.push(ord(x))
        elif c == '@':
            self.pointer.dx = 0
            self.pointer.dy = 0
        
        # Advance pointer
        self.pointer.move()
        
        # Wrap-around
        if self.pointer.x == self.width:
            self.pointer.x = 0
        elif self.pointer.x == -1:
            self.pointer.x = self.width - 1
        elif self.pointer.y == self.height:
            self.pointer.y = 0
        elif self.pointer.y == -1:
            self.pointer.y = self.height -1
        
        # Print debugging information
        if self.debug:
            # Reset debugging output redirection
            sys.stdout = sys.__stdout__
            # Clear screen
            sys.stdout.write("\x1b[H\x1b[2J")
            print "Pointer: x=%d y=%d dx=%d dy=%d" % (self.pointer.x, self.pointer.y, self.pointer.dx, self.pointer.dy)
            print "Board:"
            for y in range(self.height):
                for x in range(self.width):
                    c = self.get(x, y)
                    if x == self.pointer.x and y == self.pointer.y:
                        sys.stdout.write("\033[41m")
                    sys.stdout.write(c)
                    sys.stdout.write("\033[0m")
                sys.stdout.write('\n')
            print "Stack:"
            print self.stack._list
            print "Output:"
            self.debugstream.seek(0)
            print self.debugstream.read()
            if self.debug_delay == -1:
                sys.stdin.read(1)
            else:
                time.sleep(self.debug_delay / 1000.0)


def main():
    parser = OptionParser(usage="%prog [options] [file]")
    parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Turn on debugging mode")
    parser.add_option("--delay", dest="debugdelay", action="store", type="int", default=-1, help="Delay in milliseconds between each step in debugging mode, or -1 to wait for input")
    parser.add_option("--width", dest="width", action="store", type="int", default=80, help="Board width")
    parser.add_option("--height", dest="height", action="store", type="int", default=25, help="Board height")
    parser.add_option("-x", "--x", dest="x", action="store", type="int", default=0, help="Initial X coordinate")
    parser.add_option("-y", "--y", dest="y", action="store", type="int", default=0, help="Initial Y coordinate")
    (options, args) = parser.parse_args()
    
    board = Board(options.width, options.height, options.debug, options.debugdelay)
    board.pointer.x, board.pointer.y = options.x, options.y
    
    # Default to reading from stdin
    if len(args) == 0:
        args = ["--"]
    
    # Read in file
    if args[0] == "--":
        # Read from stdin
        infile = sys.stdin
    else:
        try:
            infile = open(args[0], 'r')
        except IOError:
            print "Could not open file"
            return 1
    
    x = y = 0
    while True:
        c = infile.read(1)
        if c == '':
            # EOF
            break
        if c == '\n':
            y += 1
            x = 0
            continue
        if x >= options.width or y >= options.height:
            print "File too large"
            return 1
        board.put(x, y, c)
        x += 1
    
    # Close the file (but don't close stdin!)
    if infile != sys.stdin:
        infile.close()
    
    # Run the program
    while not (board.pointer.dx == 0 and board.pointer.dy == 0):
        board.step()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
