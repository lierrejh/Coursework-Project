import pygame 
from tilesheet import Tilesheet
from tiles import *

tilesheet = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
map = Tilemap('assets/map/MapTest3.csv', tilesheet)

class Player(pygame.sprite.Sprite): #Character class
    def __init__(self, game, x , y, group):#, groups):#, groups)
        super().__init__(group)
        self.game = game
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
        self.image = pygame.image.load('assets/sprites+items/individual_sprites/StartingCharacter.png').convert_alpha()
        self.rect = self.image.get_rect(center = (x, y))
        self.hitbox = self.rect.inflate(0,-25)
        self.direction = pygame.math.Vector2() 
        # self.tiles = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.user = pygame.image.load('assets/sprites+items/individual_sprites/StartingCharacter.png').convert_alpha()
        self.user_flipped = pygame.transform.flip(self.user, True, False)    
        self.left_facing = False
        self.screen = pygame.display.set_mode((1600, 1000))
        self.x = x
        self.y = y
        self.velocity = pygame.math.Vector2(0,0)

    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.left_facing = True
        
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.left_facing = False
        else:
            self.direction.x = 0
   
   
    def update(self,tiles):
        self.input()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * self.speed
        self.hitbox.y += self.direction.y * self.speed
        self.rect.center = self.hitbox.center

        if self.left_facing:
            self.image = self.user_flipped
        else:
            self.image = self.user
    
