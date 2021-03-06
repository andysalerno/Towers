from engine.tile_effects import tile_effects
from engine.effects import *
from queue import *
from heapq import *
import math
import copy


class GridWorld:

    def __init__(self, width, height, spawnpoint, endpoint):
        self.width = width
        self.height = height
        self.spawnpoint = spawnpoint
        self.endpoint = endpoint

        # this grid is a 2d array of bools, where grid[3][4] means
        # x,y position (4,3) is either obstructed (True) or traversable (False)
        self.grid = [[False for x in range(self.width)]
                     for x in range(self.height)]

        self.vertices = []
        for i in range(self.width):
            for j in range(self.height):
                self.vertices.append((i, j))

        self.tilePaths = self.dijkstras_path(self.grid)

        # Creates the tile effects double array. Sets everything as a tile effect (which holds another array of effects).
        # Will need to change tile_effect later so that not everything is on
        # fire.
        self.effects = []
        for i in range(0, width):
            new = []
            for j in range(0, height):
                new.append(tile_effects())
            self.effects.append(new)

    # adds the effect to the effects list on a particular tile
    def add_effect(self, loc, type):
        if(type == "fire"):
            self.effects[loc[0]][loc[1]].append(fire(0.5))
        if(type == "stun"):
            self.effects[loc[0]][loc[1]].append(stun(10))

    # Returns a nice version of the effects triple array for json sending in
    # the format. Grabs the first effect (x,y, string of effect)
    def process_effects(self):
        processed_list = []

        for i in range(0, self.width):
            for k in range(0, self.height):
                if(len(self.effects[i][k].effects) > 0):
                    processed_list.append(
                        (i, k, self.effects[i][k].effects[0].type))

        return processed_list

    def is_blocked(self, x, y):
        return self.grid[y][x]

    def get_width(self):
        return self.width

    def get_grid(self):
        return self.grid

    def get_height(self):
        return self.height

    def get_tiles(self):
        return self.tiles

    # returns an array of tuples that are the coordinates of the neighboring
    # tiles of the passed tile
    def get_neighbors(self, xCoord, yCoord):
        neighbors = []
        if(xCoord == 0):
            if(yCoord == 0):
                neighbors.append((xCoord + 1, yCoord))
                neighbors.append((xCoord, yCoord + 1))
            elif(yCoord == self.height - 1):
                neighbors.append((xCoord, yCoord - 1))
                neighbors.append((xCoord + 1, yCoord))
            else:
                neighbors.append((xCoord, yCoord - 1))
                neighbors.append((xCoord + 1, yCoord))
                neighbors.append((xCoord, yCoord + 1))
        elif(xCoord == self.width - 1):
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
            if(yCoord == 0):
                neighbors.append((xCoord + 1, yCoord))
                neighbors.append((xCoord, yCoord + 1))
                neighbors.append((xCoord - 1, yCoord))
            elif(yCoord == self.height - 1):
                neighbors.append((xCoord, yCoord - 1))
                neighbors.append((xCoord + 1, yCoord))
                neighbors.append((xCoord - 1, yCoord))
            else:
                neighbors.append((xCoord, yCoord - 1))
                neighbors.append((xCoord + 1, yCoord))
                neighbors.append((xCoord, yCoord + 1))
                neighbors.append((xCoord - 1, yCoord))

        return neighbors

    # a get neighbors function that also returns the diagonal neighbors.
    # Default to returning diagonal first.
    def get_neighbors_diagonal(self, xCoord, yCoord):
        neighbors = []
        if(xCoord == 0):
            if(yCoord == 0):
                neighbors.append((xCoord + 1, yCoord + 1))
            elif(yCoord == self.height - 1):
                neighbors.append((xCoord + 1, yCoord - 1))
            else:
                neighbors.append((xCoord + 1, yCoord - 1))
                neighbors.append((xCoord + 1, yCoord + 1))
        elif(xCoord == self.width - 1):
            if(yCoord == 0):
                neighbors.append((xCoord - 1, yCoord + 1))
            elif(yCoord == self.height - 1):
                neighbors.append((xCoord - 1, yCoord - 1))
            else:
                neighbors.append((xCoord - 1, yCoord + 1))
                neighbors.append((xCoord - 1, yCoord - 1))
        else:
            if(yCoord == 0):
                neighbors.append((xCoord + 1, yCoord + 1))
                neighbors.append((xCoord - 1, yCoord + 1))
            elif(yCoord == self.height - 1):
                neighbors.append((xCoord + 1, yCoord - 1))
                neighbors.append((xCoord - 1, yCoord - 1))
            else:
                neighbors.append((xCoord - 1, yCoord + 1))
                neighbors.append((xCoord - 1, yCoord - 1))
                neighbors.append((xCoord + 1, yCoord - 1))
                neighbors.append((xCoord + 1, yCoord + 1))

        return neighbors

    # if a tower can be built in the desired location, do so. else return false
    def build_tower(self, xCoord, yCoord):

        if(xCoord >= self.width or yCoord >= self.height):
            return False

        if(self.can_build(xCoord, yCoord)):
            self.grid[yCoord][xCoord] = True
            self.tilePaths = self.dijkstras_path(self.grid)
            return True
        else:
            return False

    def remove_tower(self, x, y):
        self.grid[y][x] = False
        self.update_pathing()

    def update_pathing(self):
        self.tilePaths = self.dijkstras_path(self.grid)

    # return an array of that represents the tile to move to from any other
    # tile
    def get_path(self, all_tiles):
        frontier = Queue()
        frontier.put(self.endpoint)
        came_from = {}
        came_from[self.endpoint] = None
        distance = {}
        distance[self.endpoint] = 0
        ##heappush(frontier,(0, self.endpoint))

        while not frontier.empty():
            current = frontier.get()
            for next in self.get_neighbors(*current):
                # print current, "current"
                # print "next of 0", next[0]
                # print "next of 1", next[1]
                # print all_tiles
                # check to make sure the tile is empty
                if not all_tiles[next[1]][next[0]]:
                    if next not in came_from:
                        frontier.put(next)
                        distance[next] = distance[current] + 1
                        came_from[next] = current
        return came_from

    def dijkstras_path(self, grid):

        frontier = PriorityQueue()
        frontier.put(self.endpoint, 0)
        came_from = {}
        cost_so_far = {}
        came_from[self.endpoint] = None
        cost_so_far[self.endpoint] = 0

        while not frontier.empty():
            current = frontier.get()
            neighbors = self.get_neighbors(*current)
            diagonal_neighbors = self.get_neighbors_diagonal(*current)
            all_neighbors = neighbors + diagonal_neighbors

            for neighbor in all_neighbors:
                can_move_diagonally = 0
                if neighbor in diagonal_neighbors:
                    intersecting_neighbors = set(self.get_neighbors(
                        neighbor[0], neighbor[1])).intersection(all_neighbors)
                    for tile in intersecting_neighbors:
                        if grid[tile[1]][tile[0]]:
                            can_move_diagonally += 1

                if not can_move_diagonally == 2:
                    new_cost = cost_so_far[
                        current] + math.hypot(neighbor[0] - current[0], neighbor[1] - current[1])
                    if not grid[neighbor[1]][neighbor[0]]:
                        if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                            cost_so_far[neighbor] = new_cost
                            frontier.put(neighbor, new_cost)
                            came_from[neighbor] = current

        # print came_from
        return came_from

    def get_single_path(self, location):
        path_return = {}
        myLocation = location
        while (myLocation != None):
            path_return[myLocation] = self.tilePaths[myLocation]
            myLocation = self.tilePaths[myLocation]

        return path_return

    def can_build(self, xCoord, yCoord):
        if((xCoord, yCoord) == self.endpoint):  # cant build on the goal
            return False

        if((xCoord, yCoord) == self.spawnpoint):  # cant build on the spawnpoint
            return False

        if(self.grid[yCoord][xCoord]):  # cant build where there is already a tower
            return False

        # create a copy of the current came board
        copy_board = copy.deepcopy(self.grid)

        # place a tower in the desired location
        copy_board[yCoord][xCoord] = True

        # calculate the paths of the new board
        copy_path = self.dijkstras_path(copy_board)

        for x in range(self.width):
            for y in range(self.height):
                # if a tile in the new board is empty but does not have a path,
                # the build does not work
                if(not copy_board[y][x] and (x, y) not in copy_path):
                    return False

        return True  # otherwise return true
