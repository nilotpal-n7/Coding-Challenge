import pygame
import ctypes
from random import choice

#####ABOUT#####
#MAZE GENERATION is based on DEAPTH FIRST SEARCH algorithm
#MAZE SOLUTION is based on A*(A Star) Pathfinder algorithm

#but I have used STACK instead of PRIORITY QUEUE



#####NOTE######
##change cols and rows to get maze of different sizes --->
cols, rows = 42, 24 #no of rows and cols in maze
user32 = ctypes.windll.user32



#####NOTE######
##if theres problem with window size --> manually set WIDTH and HEIGHT of your screen (preffered and easy)
# or any value so that you can see full window
# or use PRIMERY SCREEN and not SECONDARY SCREEN through hdmi or screen cast
# or change (0, 1) with the index of your Secondary Screen
RES = WIDTH, HEIGHT = user32.GetSystemMetrics(0) * 0.95, user32.GetSystemMetrics(1) * 0.85



TILE = min(WIDTH / cols, HEIGHT / rows)
SQUARE = 7 * TILE / 50
RES = cols * TILE + 2, rows * TILE + 2

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()



class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False #is the cell visited during maze creation
        self.g_score = float("inf")
        self.parent = None #parent cell after which current cell is born
        self.sol_visit = False #is the cell visited during solving the maze



    def h_fun(self, goal): #hurestic function
        x = abs(self.x - goal.x)
        y = abs(self.y - goal.y)
        return (x + y)
    
    def g_fun(self): #cost till current position from the starting position
        return self.g_score

    def f_fun(self, goal): #measuring function of a*(a star) pathfinder
        h = self.h_fun(goal)
        g = self.g_fun()
        return (g + h)



    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        breadth = max(int(TILE / 10), 1)
        if self.visited:
            pygame.draw.rect(sc, pygame.Color("black"), (x, y, TILE, TILE))

        if self.walls["top"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x, y), (x + TILE, y), breadth)
        if self.walls["right"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x + TILE, y), (x + TILE, y + TILE), breadth)
        if self.walls["bottom"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x + TILE, y + TILE), (x, y + TILE), breadth)
        if self.walls["left"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x, y + TILE), (x, y), breadth)



    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]
    

    
    def check_neighbours(self): #for maze creation
        neighbours = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        if top and not top.visited:
            neighbours.append(top)
        if right and not right.visited:
            neighbours.append(right)
        if bottom and not bottom.visited:
            neighbours.append(bottom)
        if left and not left.visited:
            neighbours.append(left)
        return choice(neighbours) if neighbours else False
    

    
    def check_directions(self): #for solving maze
        directions = []
        find_index = lambda x, y: x + y * cols
        child_g = self.g_score + 1

        if not self.walls["top"] and self.y > 0:
            dir = grid_cells[find_index(self.x, self.y - 1)]
            if child_g <= dir.g_fun() and not dir.sol_visit:
                dir.g_score = child_g
                directions.append(dir)
        if not self.walls["right"] and self.x < cols - 1:
            dir = grid_cells[find_index(self.x + 1, self.y)]
            if child_g <= dir.g_fun() and not dir.sol_visit:
                dir.g_score = child_g
                directions.append(dir)
        if not self.walls["bottom"] and self.y < rows - 1:
            dir = grid_cells[find_index(self.x, self.y + 1)]
            if child_g <= dir.g_fun() and not dir.sol_visit:
                dir.g_score = child_g
                directions.append(dir)
        if not self.walls["left"] and self.x > 0:
            dir = grid_cells[find_index(self.x - 1, self.y)]
            if child_g <= dir.g_fun() and not dir.sol_visit:
                dir.g_score = child_g
                directions.append(dir)

        return choice(directions) if directions else False
    


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls["left"] = False
        next.walls["right"] = False
    elif dx == -1:
        current.walls["right"] = False
        next.walls["left"] = False

    dy = current.y - next.y
    if dy == 1:
        current.walls["top"] = False
        next.walls["bottom"] = False
    elif dy == -1:
        current.walls["bottom"] = False
        next.walls["top"] = False



grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)] #collection of all cells
current_cell = grid_cells[0] #current cell of maze creation
stack = []
colors, color = [], 0



#####NOTE#####
## [{(for random starting and ending point for maze solving change index)}] --->
start = grid_cells[-1] #starting cell for maze solving(default index: -1)
goal = grid_cells[0] #ending cell for maze solving(default index: 0)



start.g_score = 0
active_cell = start #current cell for maze solving
road = [start] #path for maze solving
is_maze = True #maze creation --> true, maze solving --> false
is_popped = False



while True:
    sc.fill(pygame.Color("darkslategray"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [cell.draw() for cell in grid_cells]



##### MAZE CREATION #####
    if is_maze:
        pygame.display.set_caption("MAZE GENERATION")
        current_cell.visited = True
        current_cell.draw()
        [pygame.draw.rect(sc, colors[i], (cell.x * TILE + SQUARE, cell.y * TILE + SQUARE, TILE - 2 * SQUARE, TILE - 2 * SQUARE), border_radius=int(2 * SQUARE)) for i, cell in enumerate(stack)]

        next_cell = current_cell.check_neighbours()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            colors.append((min(color, 255), 10, 100))
            color += 2 * 255 / (rows * cols)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
            
        elif stack:
            current_cell = stack.pop()

        if current_cell == grid_cells[0]:
            is_maze = False



##### MAZE SOLVER #####
    elif(not is_maze):
        pygame.display.set_caption("MAZE SOLUTION")
        active_cell.sol_visit = True
        pygame.draw.rect(sc, pygame.Color("red"), (goal.x * TILE + SQUARE, goal.y * TILE + SQUARE, TILE - 2 * SQUARE, TILE - 2 * SQUARE), border_radius=int(2 * SQUARE))
        [pygame.draw.rect(sc, colors[i], (cell.x * TILE + SQUARE, cell.y * TILE + SQUARE, TILE - 2 * SQUARE, TILE - 2 * SQUARE), border_radius=int(2 * SQUARE)) for i, cell in enumerate(road)]

        if active_cell == goal:
            continue

        dir = active_cell.check_directions()
        if dir:
            if is_popped:
                road.append(active_cell)
                is_popped = False
            dir.sol_visit = True
            dir.parent = active_cell
            road.append(dir)
            active_cell = dir
            
        elif road:
            active_cell = road.pop()
            is_popped = True
            if(len(road) == 0):
                road.append(start)

    pygame.display.flip()
    clock.tick(120)
