#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
import os

name = 'pictures\\base\\橙'
myset = {'a':'1', 'b': '2'}

list = os.listdir(name)
for i in list:
    print(os.path.abspath(i))