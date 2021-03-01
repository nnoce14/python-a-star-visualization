import pygame
import random
import time
import math

pygame.init()

width = 600
height = 600
rows = 50
cols = 50

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255)
}



class Node:
    # generic node class
    def __init__(self, i, j):
        self.i = i
        self.j = j

        self.f = 0
        self.g = 0
        self.h = 0

        self.parent = None
        self.obstacle = False

        self.neighbors = []

        if random.random() < 0.2:
            self.obstacle = True

    def draw(self, screen, col):
        w = width / rows
        h = height / cols
        rect = pygame.Rect(self.i * w + 1, self.j * h + 1, w - 2, h - 2)
        if not self.obstacle:
            pygame.draw.rect(screen, col, rect)
        else:
            pygame.draw.rect(screen, colors["black"], rect)

    def add_neighbors(self, grid):
        if self.i > 0:
            self.neighbors.append(grid[self.i-1][self.j])
        if self.j < rows - 1:
            self.neighbors.append(grid[self.i][self.j+1])
        if self.i < cols - 1:
            self.neighbors.append(grid[self.i+1][self.j])
        if self.j > 0:
            self.neighbors.append(grid[self.i][self.j-1])


    def show_neighbors(self):
        print(self.neighbors)


def end_game(grid, screen, path, open_l, closed_l):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()  # quits the game when red X is clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

        draw_window(screen, grid, open_l, closed_l, path)
        pygame.display.update()


def draw_grid(grid, screen):
    for i in range(cols):
        for j in range(rows):
            grid[i][j].draw(screen, colors["white"])


def draw_window(win, grid, open_l, closed_l, path):
    # colors in the background
    win.fill(colors["black"])

    # draws the grid
    draw_grid(grid, win)

    # draws open/closed nodes
    for i in range(len(open_l)):
        open_l[i].draw(win, colors["green"])
    for j in range(len(closed_l)):
        closed_l[j].draw(win, colors["red"])

    # draws the path
    for x in range(len(path)):
        path[x].draw(win, colors["blue"])

def main():
    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    grid = []
    grid = init_grid(grid)

    path = []

    openSet = []
    closedSet = []
    start = grid[0][0]
    end = grid[cols-1][rows-1]

    start.obstacle = False
    end.obstacle = False

    openSet.append(start)

    # sets the speed of the animation
    count = 0
    speed = 3

    run = True
    while run:
        # pygame event listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()  # quits the game when red X is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                i = math.floor((event.pos[0] / width) * cols)
                j = math.floor((event.pos[1] / height) * rows)
                print([i, j])
                grid[i][j].obstacle = True
        # A* Algorithm #
        # checks to see if nodes in open set list
        if True:
            if len(openSet) > 0:
                index = get_lowest_f(openSet)
                current = openSet[index]

                path = []
                temp = current
                path.append(current)
                while temp.parent is not None:
                    path.append(temp.parent)
                    temp = temp.parent

                # found the end node
                if current == end:
                    # find the path
                    run = False
                    end_game(grid, win, path, openSet, closedSet)

                openSet.remove(current)
                closedSet.append(current)

                # get and check
                neighbors = current.neighbors
                for n in neighbors:
                    # checks to see if neighbor has not already been evaluated
                    if n not in closedSet and not n.obstacle:
                        temp_g_score = current.g + 1

                        new_path = False
                        # checks if in openSet to potentially replace g value
                        if n in openSet:
                            if temp_g_score < n.g:
                                n.g = temp_g_score
                                new_path = True
                        else:
                            n.g = temp_g_score
                            openSet.append(n)
                            new_path = True

                        if new_path:
                            n.h = heuristic(n, end)
                            n.f = n.g + n.h
                            n.parent = current
            else:
                # no solution
                print("No Solution")
                path = []
                end_game(grid, win, path, openSet, closedSet)

        draw_window(win, grid, openSet, closedSet, path)
        pygame.display.update()

        count += 1


# helper functions

def get_lowest_f(openSet):
    # iterate through open
    index = 0
    for i in range(len(openSet)):
        if openSet[i].f < openSet[index].f:
            index = i
    return index


def init_grid(grid):
    for i in range(cols):
        grid.append([])

    for i in range(cols):
        for j in range(rows):
            grid[i].append(Node(i, j))

    for i in range(cols):
        for j in range(rows):
            grid[i][j].add_neighbors(grid)
            
    return grid


def heuristic(a, b):
    return math.sqrt((b.i - a.i)**2 + (b.j - a.j)**2)

main()
