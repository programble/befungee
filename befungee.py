#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pybefunge.py
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

__version__ = "0.1.2"

import sys
from optparse import OptionParser
import random
import time

parser = OptionParser(usage="%prog [options] [file]")
parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Turn on debugging")
parser.add_option("--delay", dest="delay", action="store", type="int", default=-1, help="Debugging step delay, ot -1 to wait for input")
parser.add_option("-m", "--mode", dest="mode", action="store", default="93", help="Befunge mode (not implemented)")
parser.add_option("--width", dest="width", action="store", type="int", default=80, help="Board width")
parser.add_option("--height", dest="height", action="store", type="int", default=25, help="Board height")
parser.add_option("-x", "--x", dest="x", action="store", type="int", default=0, help="Initial X coordinate")
parser.add_option("-y", "--y", dest="y", action="store", type="int", default=0, help="Initial Y coordinate")
(options, args) = parser.parse_args()

BOARD_WIDTH = options.width
BOARD_HEIGHT = options.height
DEBUG = options.debug
DEBUG_DELAY = options.delay
FILE = sys.stdin
if len(args) > 0:
    if args[0] != "--":
        FILE = open(args[0], 'r')

# Teh board
board = []
for i in range(BOARD_HEIGHT):
    board.append([" "] * BOARD_WIDTH)

# Teh Stack
class Stack:
    def __init__(self):
        self._list = []
    def push(self, item):
        self._list = [item] + self._list
    def pop(self):
        if self.length() == 0:
            return 0
        item = self._list[0]
        self._list = self._list[1:]
        return item
    def peek(self):
        if self.length() == 0:
            return 0
        return self._list[0]
    def length(self):
        return len(self._list)

stack = Stack()

# Teh pointer
pointer = {'x': options.x, 'y': options.y, 'dx': 1, 'dy': 0}

# string mode
strmode = False

# Load file into board
x=y=0
while 1:
    c = FILE.read(1)
    if c == '':
        break
    if c == '\n':
        y += 1
        x = 0
        continue
    if y >= BOARD_HEIGHT or x >= BOARD_WIDTH:
        print "File too large"
        sys.exit(1)
    board[y][x] = c
    x += 1
if FILE != sys.stdin:
    FILE.close()

# Interpret time
while 1:
    c = board[pointer['y']][pointer['x']]
    if c == '"':
        strmode = not strmode
    elif strmode:
        stack.push(ord(c))
    elif c in "0123456789":
        stack.push(int(c))
    elif c == '>':
        pointer['dx'] = 1
        pointer['dy'] = 0
    elif c == '<':
        pointer['dx'] = -1
        pointer['dy'] = 0
    elif c == '^':
        pointer['dx'] = 0
        pointer['dy'] = -1
    elif c == 'v':
        pointer['dx'] = 0
        pointer['dy'] = 1
    elif c == ':':
        stack.push(stack.peek())
    elif c == '#':
        pointer['x'] += pointer['dx']
        pointer['y'] += pointer['dy']
    elif c == ',':
        #print chr(stack.pop()),
        sys.stdout.write(chr(stack.pop()))
    elif c == '.':
        print str(stack.pop()),
    elif c == '+':
        stack.push(stack.pop() + stack.pop())
    elif c == '-':
        a = stack.pop()
        b = stack.pop()
        stack.push(b - a)
    elif c == '*':
        stack.push(stack.pop() * stack.pop())
    elif c == '/':
        a = stack.pop()
        b = stack.pop()
        stack.push(b / a)
    elif c == '%':
        a = stack.pop()
        b = stack.pop()
        stack.push(b % a)
    elif c == '`':
        a = stack.pop()
        b = stack.pop()
        if b > a:
            stack.push(1)
        else:
            stack.push(0)
    elif c == '!':
        val = stack.pop()
        if val != 0:
            stack.push(0)
        else:
            stack.push(1)
    elif c == '?':
        dir = ['>', 'v', '<', '^'][random.randint(0, 3)]
        if dir == '>':
            pointer['dx'] = 1
            pointer['dy'] = 0
        elif dir == '<':
            pointer['dx'] = -1
            pointer['dy'] = 0
        elif dir == '^':
            pointer['dx'] = 0
            pointer['dy'] = -1
        elif dir == 'v':
            pointer['dx'] = 0
            pointer['dy'] = 1
    elif c == '_':
        val = stack.pop()
        if val == 0:
            pointer['dx'] = 1
            pointer['dy'] = 0
        else:
            pointer['dx'] = -1
            pointer['dy'] = 0
    elif c == '|':
        val = stack.pop()
        if val == 0:
            pointer['dx'] = 0
            pointer['dy'] = 1
        else:
            pointer['dx'] = 0
            pointer['dy'] = -1
    elif c == '\\':
        a = stack.pop()
        b = stack.pop()
        stack.push(a)
        stack.push(b)
    elif c == '$':
        stack.pop()
    elif c == 'g':
        gy = stack.pop()
        gx = stack.pop()
        stack.push(ord(board[gy][gx]))
    elif c == 'p':
        py = stack.pop()
        px = stack.pop()
        val = chr(stack.pop())
        board[py][px] = val
    elif c == '&':
        stack.push(int(raw_input()))
    elif c == '~':
        stack.push(ord(sys.stdin.read(1)))
    elif c == '@':
        sys.exit()
    
    pointer['x'] += pointer['dx']
    pointer['y'] += pointer['dy']
    
    if pointer['x'] == BOARD_WIDTH:
        pointer['x'] = 0
    elif pointer['y'] == BOARD_HEIGHT:
        pointer['y'] = 0
    elif pointer['x'] == -1:
        pointer['x'] = BOARD_WIDTH - 1
    elif pointer['y'] == -1:
        pointer['y'] = BOARD_HEIGHT - 1
    
    if DEBUG:
        print
        print "x=%d y=%d dx=%s dy=%s strmode=%s" % (pointer['x'], pointer['y'], pointer['dx'], pointer['dy'], strmode)
        print "---BOARD---"
        for py in range(BOARD_HEIGHT):
            for px in range(BOARD_WIDTH):
                c = board[py][px]
                if px == pointer['x'] and py == pointer['y']:
                    sys.stdout.write("\033[41m")
                sys.stdout.write(c)
                sys.stdout.write("\033[0m")
            print
        print "---STACK---"
        print stack._list
        if DEBUG_DELAY == -1:
            sys.stdin.read(1)
        else:
            time.sleep(DEBUG_DELAY / 1000.0)
