"""
Minesweeper AppEngine storage
"""

from google.appengine.ext import db

# a handy function for getting the coordinates
# of the surrounding cells
adjacent = lambda x, y: [
	(x-1, y-1),
	(x,   y-1),
	(x+1, y-1),
	(x-1, y),
	(x+1, y),
	(x-1, y+1),
	(x,   y+1),
	(x+1, y+1),
]

class Minefield(db.Model):
	"""
	Minefield state object.
	"""
	author = db.UserProperty(required=True)
	width = db.IntegerProperty(default=20)
	height = db.IntegerProperty(default=10)
	mines = db.StringListProperty(default=[])
	exposures = db.StringListProperty(default=[])
	finished = db.BooleanProperty(default=False)
	
	def mine(self, x, y):
		"""
		Set a mine at the given coordinates.
		"""
		mine = u'%s,%s' % (x,y)
		if(mine in self.mines):
			return
		self.mines.append(mine)
	
	def reveal(self, x, y):
		"""
		Reveal a cell at the given coordinates.
		"""
		position = u'%s,%s' % (x,y)
		if(position in self.exposures):
			return
		self.exposures.append(position)
	
	def hide(self, x, y):
		"""
		Re-hide a cell at the given coordinates.
		"""
		position = u'%s,%s' % (x,y)
		if(position not in self.exposures):
			return
		self.exposures.remove(position)
	
	def reset(self):
		"""
		Reset the game board, leaving mines intact.
		"""
		self.exposures = []
		self.finished = False
	
	def clear(self):
		"""
		Reset the game board and remove all mines.
		"""
		self.mines = []
		self.reset()
	
	def getState(self, x, y):
		"""
		Return the number of adjacent mines, -1 for a mine.
		"""
		position = u'%s,%s' % (x,y)
		if(position in self.mines):
			return -1
		import logging
		state = 0
		for point in adjacent(x,y):
			if not(-1 < point[0] < self.height):
				continue
			elif not(-1 < point[1] < self.width):
				continue
			elif(u'%s,%s' % point in self.mines):
				state += 1
		
		return state
	
	def isRevealed(self, x, y):
		"""
		Has a given cell been revealed yet?
		"""
		if(self.finished):
			return True
		return u'%s,%s' % (x,y) in self.exposures
	
	def render(self):
		"""
		Return the current state of the board.
		"""
		# example_output = '   111      1*1     \n' +
		#                  ' 112*1   111111     \n' +
		#                  ' 1*211 112*1 111111 \n' +
		#                  '12211111*211 1*11*1 \n' +
		#                  '1*1 1*111211 123321 \n' +
		#                  '111 112111*1  1**1  \n' +
		#                  '  11212*1111  12321 \n' +
		#                  '  1*2*2221 111  1*1 \n' +
		#                  '  112111*1 1*1  111 \n' +
		#                  '       111 111      \n'
		output = ''
		for row in range(self.height):
			for col in range(self.width):
				if(self.isRevealed(row, col)):
					state = self.getState(row, col)
					if(state == -1):
						output += '*'
					elif(state == 0):
						output += ' '
					else:
						output += str(state)
				else:
					output += '#'
			output += '\n'
		return output