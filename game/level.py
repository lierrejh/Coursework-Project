import pygame

class Level:
    def __init__(self):


        #sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.visible_obstacles = pygame.sprite.Group()
    
    def run(self):