import pygame

grid_s = '''4 0 0 2 0 0 0 10 0 0 0 0 0 10 0 0 0 2 0 0
0 0 0 1 0 0 0 9 0 0 0 0 0 9 0 0 0 1 0 0
0 0 0 1 0 0 4 6 0 0 0 0 0 6 4 0 0 1 0 0
2 1 1 0 0 0 2 3 0 0 0 0 0 3 2 0 0 0 1 1
0 0 0 0 0 0 1 1 0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 2 1 0 0 0 0 0 0 0 0 0 0 0 1 2 4 0
10 9 6 3 1 0 0 0 0 0 0 0 0 0 0 0 1 3 6 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
10 9 6 3 1 0 0 0 0 0 0 0 0 0 0 0 1 3 6 9
0 0 4 2 1 0 0 0 0 0 0 0 0 0 0 0 1 2 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0 0 0 0 1 1 0 0 0 0 0
2 1 1 0 0 0 2 3 0 0 0 0 0 3 2 0 0 0 1 1
0 0 0 1 0 0 4 6 0 0 0 0 0 6 4 0 0 1 0 0
0 0 0 1 0 0 0 9 0 0 0 0 0 9 0 0 0 1 0 0'''

grid = [map(int,line.split()) for line in grid_s.split('\n')]

width = 20
height = 20

cell_width = 20 #pixels
cell_height = 20 #pixels

window_width = width*cell_width + width - 1
window_height = height*cell_height + height - 1

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Splash')

screen = pygame.display.get_surface()

fpsclock = pygame.time.Clock()
fps = 60

grid_surface = pygame.Surface((window_width, window_height))
grid_surface.fill((255,0,255))
grid_surface.set_colorkey((255,0,255))
for x in xrange(cell_width, window_width, cell_width+1):
    pygame.draw.line(grid_surface, (0,0,0), (x, 0), (x, window_height))
for y in xrange(cell_height, window_height, cell_height+1):
    pygame.draw.line(grid_surface, (0,0,0), (0, y), (window_width, y))


while True:
    screen.fill((255,255,0))
    screen.blit(grid_surface, (0,0))
    for row in xrange(len(grid)):
        for col in xrange(len(grid)):
            colour = int(grid[row][col]/10.0 * 255)
            xpos = col*(cell_width+1)
            ypos = row*(cell_height+1)
            pygame.draw.rect(screen, (0,colour,colour), (xpos, ypos, cell_width, cell_height))
    pygame.display.flip()