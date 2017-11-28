#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: cfg.py
# @Created:   2017-11-27 23:26:09  seo (simon.seo@nyu.edu) 
# @Updated:   2017-11-28 15:13:43  Simon Seo (simon.seo@nyu.edu)

from util import Random, Timekeeper

random = Random('random-numbers.txt')
tk = Timekeeper()
M = 0 #machine size in words. All available for page frames
P = 0 #page size in words.
S = 0 #size of each process, i.e., the references are to virtual addresses 0..S-1.
J = 0 #job mix, which determines A, B, and C, as described below.
N = 0 #number of references for each process.
R = '' #replacement algorithm, LIFO (NOT FIFO), RANDOM, or LRU.'''
