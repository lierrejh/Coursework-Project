import pygame 
from tilesheet import Tilesheet

class Player:
    def __init__(self, game, x, y):
        self.x = int(x)
        self.game = game
        self.y = int(y)
        # self.user = self.tiles.get_tile(15, 15)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
        self.screen = pygame.display.set_mode((1600, 1000))
        self.tiles = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)

    
    def draw(self, screen):
        self.screen.blit(self.tiles.get_tile(15, 15), (400,400))
    
    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
        
        self.x += self.velX
        self.y += self.velY

        self.user = self.screen.blit(self.tiles.get_tile(15, 15), (int(self.x), int(self.y)))