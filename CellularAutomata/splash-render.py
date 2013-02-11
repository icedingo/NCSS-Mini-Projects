# This is a work in progress but it gives some cool looking things

import sys
import pygame
from pygame.locals import *
import random

pygame.font.init()

# config
width = 64
height = 64
cell_width = 10 #pixels
cell_height = 10 #pixels

max_health = 300
min_health = 0
life_threshold = 10
# iterations = 10

# Change this value for a different look!
EFFECT = 1.00

paused = False

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
        if self.health > max_health:
            self.health = max_health
        if self.health < min_health:
            self.health = min_health
        if min_health < self.health < life_threshold:
            self.health = min_health
        self.delta_health = 0
        self.givers_of_life = self.next_givers_of_life
        self.next_givers_of_life = set()

def step_grid():
    for row in grid:
        for cell in row:
            if cell.health != 0:
                cell.give_life(cell.health*EFFECT)

def update_grid():
    for row in grid:
        for cell in row:
            cell.update()

def print_grid():
    for row in grid:
        print(' '.join(map(str,row)))

def handle_events(events):
    global paused
    global max_health
    global min_health
    global life_threshold
    global EFFECT

    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == UPDATECELLS and not paused:
            step_grid()
            update_grid()
        elif event.type == KEYDOWN:
            if event.key == K_r:
                reset()
            elif event.key == K_c:
                reset(fillrandom=False)
            elif event.key == K_SPACE:
                paused = not paused
            elif event.key == K_s and paused:
                step_grid()
                update_grid()
            elif event.key == K_ESCAPE or event.key == K_q:
                sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > grid_width:
                if event.button == 4:
                    # scroll up
                    change_direction = 1
                elif event.button == 5:
                    # scroll down
                    change_direction = -1
                else:
                    continue

                if 0 < mouse_y < 80:
                    # max_health
                    if max_health >= 5:
                        max_health += 5*change_direction
                        if max_health < 5:
                            max_health = 4
                    else:
                        max_health += 1*change_direction
                    if max_health < 1:
                        max_health = 1
                elif 80 < mouse_y < 160:
                    # min_health
                    min_health += 5*change_direction
                    if min_health < 0:
                        min_health = 0
                elif 160 < mouse_y < 240:
                    # life_threshold
                    life_threshold += 1*change_direction
                    if life_threshold < 0:
                        life_threshold = 0
                elif 240 < mouse_y < 360:
                    # EFFECT
                    EFFECT += 0.05*change_direction

    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < grid_width and mouse_y < grid_height:
            grid[mouse_y/(cell_height+1)][mouse_x/(cell_width+1)].health = max_health
    elif mouse_buttons[2]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < grid_width and mouse_y < grid_height:
            grid[mouse_y/(cell_height+1)][mouse_x/(cell_width+1)].health = min_health

def draw_gui():
    gui_surface.fill((0,0,0))
    pygame.draw.rect(gui_surface, (255,255,255), (0,0,2,window_height))
    max_health_val = big_font.render('%d' % max_health, True, (255,255,255))
    min_health_val = big_font.render('%d' % min_health, True, (255,255,255))
    life_threshold_val = big_font.render('%d' % life_threshold, True, (255,255,255))
    EFFECT_val = big_font.render('%.2f' % EFFECT, True, (255,255,255))

    gui_surface.blit(max_health_text, (5, 10))
    gui_surface.blit(max_health_val, (max(0, 90 - max_health_val.get_width()), 35))
    pygame.draw.line(gui_surface, (255,255,255), (0, 80), (100, 80))
    
    gui_surface.blit(min_health_text, (5, 90))
    gui_surface.blit(min_health_val, (max(0, 90 - min_health_val.get_width()), 115))
    pygame.draw.line(gui_surface, (255,255,255), (0, 160), (100, 160))
    
    gui_surface.blit(life_threshold_text, (5, 170))
    gui_surface.blit(life_threshold_val, (max(0, 90 - life_threshold_val.get_width()), 195))
    pygame.draw.line(gui_surface, (255,255,255), (0, 240), (100, 240))
    
    gui_surface.blit(EFFECT_text, (5, 250))
    gui_surface.blit(EFFECT_val, (max(0, 90 - EFFECT_val.get_width()), 275))
    pygame.draw.line(gui_surface, (255,255,255), (0, 320), (100, 320))

    screen.blit(gui_surface, (grid_width, 0))
    screen.blit(below_grid_surface, (0, grid_height))
    if paused:
        screen.blit(pause_surface, (grid_width - 80, grid_height - 80))
        


def reset(fillrandom=True):
    global grid
    global paused
    grid = [[Cell(i, j) for i in xrange(width)] for j in xrange(height)]
    paused = False

    if fillrandom:
        for i in xrange(50):
            grid[random.randint(0,height-1)][random.randint(0,width-1)].health = random.randint(int(min_health + 0.75*(max_health - min_health)), max_health)

reset(fillrandom=False)


grid_width = width*cell_width + width - 1
grid_height = height*cell_height + height - 1

window_width = grid_width + 100
window_height = grid_height + 90
if window_height < 320:
    window_height = 320
    draw_below_grid = True

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Splash')

screen = pygame.display.get_surface()

fpsclock = pygame.time.Clock()
fps = 60

UPDATECELLS = USEREVENT+1
pygame.time.set_timer(UPDATECELLS, 100)

grid_surface = pygame.Surface((grid_width, grid_height))
grid_surface.fill((255,0,255))
grid_surface.set_colorkey((255,0,255))
for x in xrange(cell_width, grid_width, cell_width+1):
    pygame.draw.line(grid_surface, (0,0,0), (x, 0), (x, grid_height))
for y in xrange(cell_height, grid_height, cell_height+1):
    pygame.draw.line(grid_surface, (0,0,0), (0, y), (grid_width, y))

pause_surface = pygame.Surface((60,60))
pause_surface.fill((255,0,255))
pause_surface.set_colorkey((255,0,255))
pygame.draw.rect(pause_surface, (255,255,255), (0,0,20,60))
pygame.draw.rect(pause_surface, (255,255,255), (40,0,20,60))

gui_surface = pygame.Surface((100, window_height))

below_grid_surface = pygame.Surface((grid_width, window_height - grid_height))
pygame.draw.rect(below_grid_surface, (255,255,255), (0,0,grid_width,2))

font = pygame.font.Font(None, 20)
mid_font = pygame.font.Font(None, 30)
big_font = pygame.font.Font(None, 50)

max_health_text = font.render('Max health', True, (255,255,255))
min_health_text = font.render('Min health', True, (255,255,255))
life_threshold_text = font.render('Life threshold', True, (255,255,255))
EFFECT_text = font.render('Magic level', True, (255,255,255))

usage_title = mid_font.render('USAGE', True, (255,255,255))
usage_1_text = font.render('KEYS:', True, (255,255,255))
usage_2_text = font.render('C - clear grid', True, (255,255,255))
usage_3_text = font.render('R - new random grid', True, (255,255,255))
usage_4_text = font.render('S - step grid while paused', True, (255,255,255))
usage_5_text = font.render('Space - pause', True, (255,255,255))
usage_6_text = font.render('Esc/Q - exit', True, (255,255,255))

usage_7_text = font.render('MOUSE:', True, (255,255,255))
usage_8_text = font.render('Left button - set cell to max health', True, (255,255,255))
usage_9_text = font.render('Right button - set cell to min health', True, (255,255,255))
usage_10_text = font.render('Scroll up - increase sidebar value', True, (255,255,255))
usage_11_text = font.render('Scroll down - decrease sidebar value', True, (255,255,255))

col1 = 5
col2 = 15 + col1 + usage_title.get_width()
col3 = 20 + col2 + usage_3_text.get_width()
col4 = 20 + col3 + usage_5_text.get_width()
col5 = 20 + col4 + usage_7_text.get_width()

bottom_mid = below_grid_surface.get_height()/2

row1 = bottom_mid - 45 + 10
row2 = bottom_mid - 45 + 30
row3 = bottom_mid - 45 + 50
row4 = bottom_mid - 45 + 70

below_grid_surface.blit(usage_title, (col1, row3))
below_grid_surface.blit(usage_1_text, (5+usage_title.get_width()-usage_1_text.get_width(), row1))
below_grid_surface.blit(usage_2_text, (col2, row1))
below_grid_surface.blit(usage_3_text, (col2, row2))
below_grid_surface.blit(usage_4_text, (col2, row3))
below_grid_surface.blit(usage_5_text, (col3, row1))
below_grid_surface.blit(usage_6_text, (col3, row2))

below_grid_surface.blit(usage_7_text, (col4, row1))
below_grid_surface.blit(usage_8_text, (col5, row1))
below_grid_surface.blit(usage_9_text, (col5, row2))
below_grid_surface.blit(usage_10_text, (col5, row3))
below_grid_surface.blit(usage_11_text, (col5, row4))



while True:
    screen.fill((255,255,0))
    screen.blit(grid_surface, (0,0))

    handle_events(pygame.event.get())

    for row in xrange(len(grid)):
        for col in xrange(len(grid[row])):
            colour = int(grid[row][col].health/float(max_health) * 255)
            if colour > 255: 
                colour = 255
            elif colour < 0:
                colour = 0
            xpos = col*(cell_width+1)
            ypos = row*(cell_height+1)
            pygame.draw.rect(screen, (0,colour,colour), (xpos, ypos, cell_width, cell_height))

    draw_gui()
    pygame.display.flip()
    fpsclock.tick(fps)
