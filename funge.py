#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Stack:
    """A basic LIFO stack"""
    def __init__(self):
        self._list = []
    
    def push(self, item):
        """Push an item onto the top of the stack"""
        self._list = [item] + self._list
    
    def pop(self):
        """Remove and return the top item on the stack"""
        if len(self) == 0:
            return 0
        item = self._list[0]
        self._list = self._list[1:]
        return item
    
    def peek(self):
        """Return the top item on the stack without removing it"""
        if len(self) == 0:
            return 0
        return self._list[0]
    
    def __len__(self):
        """Return the number of items on the stack"""
        return len(self._list)

class Pointer:
    """A Befunge pointer"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 0
        self.stack = Stack()
        self.stringmode = False
    def move(self):
        self.x += self.dx
        self.y += self.dy

