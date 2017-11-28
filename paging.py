#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: paging.py
# @Created:   2017-11-27 11:34:36  seo (simon.seo@nyu.edu) 
# @Updated:   2017-11-28 17:53:43  Simon Seo (simon.seo@nyu.edu)

import sys, math
import cfg

class Page():
	"""model for page"""
	def __init__(self, pid, pageNum, p):
		self.pid = pid
		self.pageNum = pageNum
		self.hostProcess = p
		# self.fid = None
		self.residency = 0

	def reference(self):
		self.hostProcess.reference()

	def incrementResidency(self):
		self.residency += 1

	def __eq__(self, other):
		if (self.pid, self.pageNum) == (other.pid, other.pageNum):
			return True
		else:
			return False

class Process():
	"""model for process"""
	def __init__(self, pid, A, B, C):
		super(Process, self).__init__()
		self.pid = pid # process pid
		# A, B, C are frations that model probability of reference locality
		self.A = A
		self.B = B
		self.C = C
		self.faults = 0 # keeps track of number of page faults
		self.evictions = 0 # keeps track of number of page evictions
		self.residencies = 0 # sum of page residencies
		self.references = 0 # keeps track of number of references
		self.w = (111 * pid) % cfg.S # the most recent word that the process referenced
		self.pages = []
		self.populate()

	def populate(self):
		pageNum = int(math.ceil(cfg.S / cfg.P))
		for i in range(pageNum):
			self.pages.append(Page(self.pid, i, self))

	def nextWord(self):
		'''y is a real number between 0 and 1.
		returns next word that will be referenced'''
		y = cfg.random.randY()
		w = self.w
		if y < self.A:
			w = (w + 1) % cfg.S
		elif y < self.A + self.B:
			w = (w - 5 + cfg.S) % cfg.S
		elif y < self.A + self.B + self.C:
			w = (w + 4) % cfg.S
		else:
			w = cfg.random.randInt() % cfg.S
		self.w = w
		return self.w

	def getCurrWord(self):
		'''returns the address of the most recently referenced word'''
		return self.w

	def getCurrPage(self):
		'''returns the page that the most recently referenced word is in'''
		pageNum = int(math.floor(self.w / cfg.P))
		return self.pages[pageNum]

	def isTerminated(self):
		return False if self.references < cfg.N else True

	def incrementResidency(self):
		self.residency += 1

	def reference(self):
		self.references += 1

	def __str__(self):
		return 'Process {}'.format(self.pid)

class ProcessTable(list):
	"""manages all processes"""
	def __init__(self):
		super(ProcessTable, self).__init__()

	def populate(self, J):
		if J == 1:
			# fully sequential and trivial job mix
			self.append(Process(1, 1, 0, 0))
		elif J == 2:
			# fully sequential job mix
			self.append(Process(1, 1, 0, 0))
			self.append(Process(2, 1, 0, 0))
			self.append(Process(3, 1, 0, 0))
			self.append(Process(4, 1, 0, 0))
		elif J == 3:
			# fully random sequences
			self.append(Process(1, 0, 0, 0))
			self.append(Process(2, 0, 0, 0))
			self.append(Process(3, 0, 0, 0))
			self.append(Process(4, 0, 0, 0))
		elif J == 4:
			# arbitrary job mix
			self.append(Process(1, .75, .25,   0))
			self.append(Process(2, .75,  0,   .25))
			self.append(Process(3, .75, .125, .125))
			self.append(Process(4, .5,  .125, .125))
		return self

	def isTerminated(self):
		for p in self:
			if not p.isTerminated():
				return False
		return True

	def printSummary(self):
		faults = 0
		residencies = 0
		evictions = 0

		print()
		for p in self:
			faults += p.faults
			residencies += p.residencies
			evictions += p.evictions
			if p.evictions == 0:
				print('Process {} had {} faults.\n     With no evictions, the average residence is undefined.'.format(p.pid, p.faults))
			else:
				print('Process {} had {} faults and {} average residency.'.format(p.pid, p.faults, p.residencies/p.evictions))

		if evictions == 0:
			print('\nThe total number of faults is {}.\n     With no evictions, the overall average residence is undefined.'.format(faults))
		else:
			print('\nThe total number of faults is {} and the overall average residency is {}.'.format(faults, residencies/evictions))

class Frame():
	"""docstring for Frame"""
	def __init__(self, fid):
		self.fid = fid
		self.page = None
		# self.pid = None
		# self.pageNum = None
		self.lastReferenced = -1
		self.firstReferenced = 2147483648

	def reference(self):
		if self.isEmpty():
			raise Exception('Referred to an empty frame')
		t = cfg.tk.getNow() # current time according to timekeeper
		if t > self.lastReferenced:
			self.lastReferenced = t
		if t < self.firstReferenced:
			self.firstReferenced = t
		self.page.reference()

	def isEmpty(self):
		return self.page is None

	def save(self, page):
		self.page = page

	def reset(self):
		fid = self.fid
		self.__init__(fid)

	def __str__(self):
		if self.page is None:
			return 'Frame {}: Empty'.format(self.fid)
		else:
			return 'Frame {}: Page {} of Process {}'.format(self.fid, self.page.pageNum, self.page.pid)

class FrameTable(list):
	"""docstring for FrameTable"""
	def __init__(self):
		super(FrameTable, self).__init__()

	def populate(self, frameCount):
		'''populates frame table with empty frames'''
		for i in range(frameCount):
			self.append(Frame(i))
		return self

	def get(self, page):
		'''returns frame id if frametable has page, else return false'''
		for frame in self:
			if frame.page is not None and frame.page == page:
				return frame
		return None

	def alloc(self, page):
		'''gives a frame to new page. if there is no free space, evict'''
		self.sort(key=lambda f: -f.fid) #sort by decreasing order for consistency of specs
		# return empty frame and save page in it
		for f in self:
			if f.isEmpty():
				f.save(page)
				return f
		# if there are no empty frames, evict a frame and return it
		f = self.evict()
		f.save(page)
		return f

	def evict(self):
		'''make free space'''
		if cfg.R == 'lifo':
			return self._evictLIFO()
		elif cfg.R == 'random':
			return self._evictRANDOM()
		elif cfg.R == 'lru':
			return self._evictLRU()
		else:
			raise Exception('non-existing replacement algorithm "{}"'.format(cfg.R))

	def _evictLIFO(self):
		f = sorted(self, key=lambda f:f.firstReferenced)[-1]
		page = f.page
		p = page.hostProcess
		p.residencies += page.residency
		page.residency = 0
		p.evictions += 1
		f.reset()
		return f

	def _evictRANDOM(self):
		randInt = cfg.random.randInt()
		frameCount = int(math.ceil(cfg.M / cfg.P))
		randFrame = randInt % frameCount
		f = sorted(self, key=lambda f:f.fid)[randFrame]
		page = f.page
		p = page.hostProcess
		p.residencies += page.residency
		page.residency = 0
		p.evictions += 1
		f.reset()
		return f

	def _evictLRU(self):
		f = sorted(self, key=lambda f: f.lastReferenced)[0]
		page = f.page
		p = page.hostProcess
		p.residencies += page.residency
		page.residency = 0
		p.evictions += 1
		f.reset()
		return f

	def incrementResidencies(self):
		for f in self:
			if not f.isEmpty():
				f.page.incrementResidency()

def main():
	pt = ProcessTable().populate(cfg.J) #create process according to J
	frameCount = int(math.ceil(cfg.M / cfg.P))
	ft = FrameTable().populate(frameCount) #create 'frameCount' number of empty frames

	while not pt.isTerminated():
		for p in pt: # for each process
			q = 3
			for ref in range(q): # reference q times
				if p.isTerminated():
					break
				cfg.tk.tick() # keeps time
				currPage = p.getCurrPage() # the page that the process will reference
				currFrame = ft.get(currPage)
				if currFrame is None: # if the page is not in the frame table (page fault)
					p.faults += 1
					currFrame = ft.alloc(currPage) # give a frame to new page
				currFrame.reference() # reference the page (mostly useful for lru)
				ft.incrementResidencies()
				p.nextWord()
	pt.printSummary()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		args = sys.argv[1:]
	else:
		raise Exception('Requires more arguments')
	cfg.M, cfg.P, cfg.S, cfg.J, cfg.N, cfg.R, _ = [(int(el) if el.isnumeric() else el) for el in args]
	cfg.random.reset()
	cfg.tk.reset()
	print('The machine size is {}.'.format(cfg.M))
	print('The page size is {}.'.format(cfg.P))
	print('The process size is {}.'.format(cfg.S))
	print('The job mix number is {}.'.format(cfg.J))
	print('The number of references per process is {}.'.format(cfg.N))
	print('The replacement algorithm is {}.'.format(cfg.R))
	print('The level of debugging output is {}'.format(_))
	main()


