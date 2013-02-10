from time import sleep
import pygame
from pygame.locals import *

# config
width = 20
height = 20
iterations = 10

class Cell:
    def __init__(self, x, y):
        self.health = 0
        self.delta_health = 0
        self.givers_of_life = set()
        self.next_givers_of_life = set()
        self.pos = (x, y)
        self.x = x
        self.y = y
        self.neighbours_x = [1, 1, 1, 0, -1, -1, -1, 0]
        self.neighbours_y = [-1, 0, 1, 1, 1, 0, -1, -1]
        self._init_neighbours()

    def __repr__(self):
        return str(self.health)

    def _init_neighbours(self):
        for pos in xrange(8):
            self.neighbours_x[pos] += self.x
            self.neighbours_y[pos] += self.y
            if self.neighbours_x[pos] >= width:
                self.neighbours_x[pos] -= width
            if self.neighbours_y[pos] >= height:
                self.neighbours_y[pos] -= height

    def give_life(self, full_amount, share=True):
        if share:
            split = float(8 - len(self.givers_of_life))
            if split != 0:
                amount = int(full_amount/split + 0.5)
            else:
                return
        else:
            amount = full_amount

        for pos in xrange(8):
            give_y = self.neighbours_y[pos]
            give_x = self.neighbours_x[pos]
            receiver = grid[give_y][give_x]
            if receiver not in self.givers_of_life:
                receiver.add_health(amount, self)

        self.remove_health(full_amount)


    def add_health(self, amount, from_cell=None):
        self.delta_health += amount
        if from_cell is not None:
            self.next_givers_of_life.add(from_cell)

    def remove_health(self, amount):
        self.delta_health -= amount

    def update(self):
        self.health += self.delta_health
        self.delta_health = 0
        self.givers_of_life = self.next_givers_of_life
        self.next_givers_of_life = set()

def step_grid():
    for row in grid:
        for cell in row:
            if cell.health != 0:
                cell.give_life(cell.health)

def update_grid():
    for row in grid:
        for cell in row:
            cell.update()

def print_grid():
    for row in grid:
        print(' '.join(map(str,row)))

grid = [[Cell(i, j) for i in xrange(width)] for j in xrange(height)]

grid[0][0].health = 300

print 'Start'
print_grid()
print

for i in xrange(iterations):
    print 'Iteration %d' % (i+1)
    step_grid()
    update_grid()
    print_grid()
    print