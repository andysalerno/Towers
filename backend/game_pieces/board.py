class Board:

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.tiles = [[0 for x in range(width)] for x in range(height)] ##initialize a 2d array that will be the board tiles
		self.goal = (width - 1, height - 1)   							##set goal node to final tile of the board
		self.start = (0, 0)												##set start node to first tile of the board
		self.tilePaths = {}

	def get_width():
		return self.width

	def get_height():
		return self.height

	def get_tiles():
		return self.tiles

	def get_neighbors(xCoord, yCoord):									##returns an array of tuples that are the coordinates of the neighboring tiles of the passed tile
		neighbors = []
		if(xCoord == 0):
			if(yCoord == 0):
				neighbors.append((xCoord + 1, yCoord))
				neighbors.append((xCoord, yCoord + 1))
			elif(yCoord == self.height-1):
				neighbors.append((xCoord, yCoord - 1))
				neighbors.append((xCoord + 1, yCoord))
			else:
				neighbors.append((xCoord, yCoord - 1))
				neighbors.append((xCoord + 1, yCoord))
				neighbors.append((xCoord, yCoord + 1))
		elif(xCoord == width - 1):
			if(yCoord == 0):
				neighbors.append((xCoord, yCoord + 1))
				neighbors.append((xCoord - 1, yCoord))
			elif(yCoord == self.height - 1):
				neighbors.append((xCoord, yCoord - 1))
				neighbors.append((xCoord - 1, yCoord))
			else:
				neighbors.append((xCoord, yCoord - 1))
				neighbors.append((xCoord, yCoord + 1))
				neighbors.append((xCoord - 1, yCoord))
		else:
			neighbors.append((xCoord, yCoord - 1))
			neighbors.append((xCoord + 1, yCoord))
			neighbors.append((xCoord, yCoord + 1))
			neighbors.append((xCoord - 1, yCoord))

		return neighbors


	def build_tower(xCoord, yCoord, tower):							##if a tower can be built in the desired location, do so. else return false

		if(can_build(xCoord, yCoord)):
			self.tiles[xCoord][yCoord] = tower
			self.tilePaths = get_path(self.tiles)
			return true
		else:
			return false

	def get_path(all_tiles):										##return an array of that represents the tile to move to from any other tile
		frontier = Queue()
		frontier.put(self.goal)
		came_from = {}
		came_from[self.goal] = None

		while not frontier.empty():
			current = frontier.get()
			for next in get_neighbors(*current):
				if(all_tiles[next[0]][next[1]] == 0):				##check to make sure the tile is empty
					if next not in came_from:
						frontier.put(next)
						came_from[next] = current

		return came_from

	def can_build(xCoord, yCoord):
		if((xCoord, yCoord) == self.goal):							##cant build on the goal
			return false

		if(self.tiles[xCoord][yCoord] != 0):						##cant build where there is already a tower
			return false

		copy_board = self.tiles 									##create a copy of the current came board

		copy_board[xCoord][yCoord] = 1 								##place a tower in the desired location

		copy_path = get_path(copy_board)							##calculate the paths of the new board						

		for x in range(self.width):
			for y in range(self.height):
				if(copy_board[x][y] == 0 && (x,y) not in copy_path):	##if a tile in the new board is empty but does not have a path, the build does not work
					return false

		return true													##otherwise return true