#!/usr/bin/python3

import pygame as pg
from random import choice

cell_size = 8
window_size = (640, 640)

pg.init()

class Cell(pg.sprite.Sprite):

    def __init__(self, x, y, alive):
        pg.sprite.Sprite.__init__(self)
        self.alive = alive
        self.x = x
        self.y = y
        
        self.img = pg.Surface([cell_size, cell_size])
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        rgb = (255*self.alive, 255*self.alive, 255*self.alive)
        self.img.fill(rgb)

class Engine:

    def __init__(self):
        self.running = False
        self.paused = False
        self.grid = False

        self.width = 80
        self.height = 80
        self.matrix = []
        self.generations = 0

        self.screen = None
        self.clock = None

    def start(self):
        self.running = True
        self.paused = True

        for y in range(self.height):
            for x in range(self.width):
                c = Cell(x*cell_size, y*cell_size, False)
                self.matrix.append(c)

        self.screen = pg.display.set_mode(window_size)
        self.clock = pg.time.Clock()

        pg.display.set_caption("GameOfDigits")
        pg.key.set_repeat(50, 100)

        self.run()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.event()
            self.update()

    def get_neighbors(self, matrix, i):
        neighbors = 0
        for y in range(-1, 2):
            for x in range(-1, 2):
                try:
                    index = ((y * self.width) + x) + i
                    if index != i:
                        neighbors += int(matrix[index])#int(matrix[index].alive)
                except IndexError:
                    pass
        return neighbors

    def draw_grid(self):
        if self.grid:
            ws = list(window_size)
            for x in range(0, ws[0], cell_size):
                pg.draw.line(self.screen, (128, 128, 128, 128), (x, 0), (x, ws[1]))
            for y in range(0, ws[1], cell_size):
                pg.draw.line(self.screen, (128, 128, 128, 128), (0, y), (ws[0], y))

            ds = [self.width*cell_size, self.height*cell_size]
            for x in range(0, ds[0], cell_size):
                pg.draw.line(self.screen, (255, 255, 255, 128), (x, 0), (x, ds[1]))
            for y in range(0, ds[1], cell_size):
                pg.draw.line(self.screen, (255, 255, 255, 128), (0, y), (ds[0], y))
        pg.display.flip()

    def draw_cells(self):
        for cell in self.matrix:
            cell.update()
            self.screen.blit(cell.img, cell)
        pg.display.flip()

    def event(self):
        for event in pg.event.get():
            # Window Input
            if event.type == pg.QUIT:
                self.running = False
                quit()

            # Mouse Input
            if event.type == pg.MOUSEBUTTONDOWN:
                try:
                    mp = list(pg.mouse.get_pos())
                    x, y = int(mp[0]/cell_size), int(mp[1]/cell_size)
                    index = (y * self.width) + x
                    if pg.mouse.get_pressed() == (1, 0, 0):
                        self.matrix[index].alive = True
                    if pg.mouse.get_pressed() == (0, 0, 1):
                        self.matrix[index].alive = False
                except IndexError:
                    pass
                self.draw_cells()

            # Key Input
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

                if event.key == pg.K_r:
                    self.matrix.clear()
                    for y in range(self.height):
                        for x in range(self.width):
                            c = Cell(x*cell_size, y*cell_size, bool(choice([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])))
                            self.matrix.append(c)
                    self.draw_cells()
                    #print("\n"*50)
                    print("Matrix randomized.")

                if event.key == pg.K_c:
                    self.generations = 0
                    self.matrix.clear()
                    for y in range(self.height):
                        for x in range(self.width):
                            c = Cell(x*cell_size, y*cell_size, False)
                            self.matrix.append(c)
                    #print("\n"*50)
                    print("Matrix reset.")

                if event.key == pg.K_p:
                    if self.paused == True:
                        self.paused = False
                    else:
                        self.paused = True
                    #print("\n"*50)
                    print("Paused:", self.paused)

                if event.key == pg.K_g:
                    if self.grid == True:
                        self.grid = False
                    else:
                        self.grid = True
                    #print("\n"*50)
                    print("Grid:", self.grid)

                if event.key == pg.K_o:
                    if self.paused:
                        self.apply_rules()
                        #print("\n"*50)
                        print("Generations:", self.generations)
                        self.draw_cells()

                if event.key == pg.K_i:
                    mp = list(pg.mouse.get_pos())
                    x, y = int(mp[0]/cell_size), int(mp[1]/cell_size)
                    index = (y * self.width) + x
                    #print("\n"*50)
                    print("Alive:", self.matrix[index].alive, "\nNeighbors:", self.get_neighbors(self.matrix, index))

    def apply_rules(self):
        # Get last generation
        last_gen = []
        for cell in self.matrix:
            last_gen.append(cell.alive)

        # Apply rules
        for i in range(len(self.matrix)):
            n = self.get_neighbors(last_gen, i)
            if (n > 3 or n < 2) and last_gen[i] == True:
                self.matrix[i].alive = False
            if (n == 3 or n == 2) and last_gen[i] == True:
                self.matrix[i].alive = True
            if n == 3 and last_gen[i] == False:
                self.matrix[i].alive = True
        self.generations += 1

    def update(self):
        if not self.paused:
            self.apply_rules()
            self.draw_cells()

        self.draw_grid()

E = Engine()
E.start()
