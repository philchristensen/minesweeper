from google.appengine.ext import db

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
	author = db.UserProperty(required=True)
	width = db.IntegerProperty(required=True)
	height = db.IntegerProperty(required=True)
	mines = db.StringListProperty(default=[])
	exposures = db.StringListProperty(default=[])
	finished = db.BooleanProperty(default=False)
	
	def mine(self, x, y):
		mine = '%s,%s' % (x,y)
		if(mine in self.mines):
			return
		self.mines.append(mine)
	
	def reveal(self, x, y):
		position = '%s,%s' % (x,y)
		if(position in self.exposures):
			return
		self.exposures.append(position)
	
	def hide(self, x, y):
		position = '%s,%s' % (x,y)
		if(position not in self.exposures):
			return
		self.exposures.remove(position)
	
	def reset(self):
		self.exposures = []
		self.finished = False
	
	def getState(self, x, y):
		position = '%s,%s' % (x,y)
		if(position in self.mines):
			return -1
		
		state = 0
		for point in adjacent(x,y):
			if not(-1 < point[0] < self.width):
				continue
			elif not(-1 < point[1] < self.height):
				continue
			elif('%s,%s' % point in self.mines):
				state += 1
		
		return state
	
	def isRevealed(self, x, y):
		if(self.finished):
			return True
		return '%s,%s' % (x,y) in self.exposures
	
	def render(self):
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