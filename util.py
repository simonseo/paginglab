#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: util.py
# @Created:   2017-11-27 23:26:33  seo (simon.seo@nyu.edu) 
# @Updated:   2017-11-28 17:48:46  Simon Seo (simon.seo@nyu.edu)
class Timekeeper():
	"""Tracks time for all processes"""
	def __init__(self):
		self.now = 0
	def tick(self):
		self.now += 1
	def getNow(self):
		return self.now
	def reset(self):
		self.__init__()

class Random():
	"""Random variable generator"""
	def __init__(self, filename):
		import os
		if not os.path.isfile(filename):
			raise Exception('The input file does not exist.')
		self.filename = filename
		self.file = open(filename,'r')
		self.RAND_MAX = 2147483647
	def randInt(self):
		return int(self.file.readline().strip())
	def randomOS(self, U):
		randInt = self.randInt()
		return 1 + randInt % U
	def randY(self):
		'''generates random number between 0 and 1'''
		randInt = self.randInt()
		return randInt / (self.RAND_MAX + 1)
	def reset(self):
		self.__init__(self.filename)
