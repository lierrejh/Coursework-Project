import pygame
import json

class Tilesheet:
    def __init__(self, filename, width, height, rows, cols):
        image = pygame.image.load(filename).convert()
        self.tile_table = []
        for tile_x in range (0, cols):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0,rows):
                rect = (tile_x * width , tile_y * height , width, height)
                line.append(image.subsurface(rect))
    
    # Gets the tile at the given x and y from the tilesheet
    def get_tile(self, x , y):
        tileNeeded = pygame.transform.scale(self.tile_table[x][y], (16,16))
        return tileNeeded
    
    # Draws the tilesheet to the screen
    def draw(self, screen):
        for x, row in enumerate(self.tile_table):
            for y, tile in enumerate(row):
                screen.blit(tile, (x * 50, y * 50))

    