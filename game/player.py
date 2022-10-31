import pygame 
from tilesheet import Tilesheet
from tiles import *

tilesheet = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
map = Tilemap('assets/map/MapTest3.csv', tilesheet)
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite): #Character class
    def __init__(self, game, x , y, group):#, groups):#, groups)
        super().__init__(group)
        self.game = game
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 6
        self.image = pygame.image.load('assets/sprites+items/individual_sprites/StartingCharacter.png').convert_alpha()
        self.rect = self.image.get_rect(center = (x,y))
        self.hitbox = self.rect.copy().inflate(100,100)
        self.direction = pygame.math.Vector2() 
        # self.tiles = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.user = pygame.image.load('assets/sprites+items/individual_sprites/StartingCharacter.png').convert_alpha()
        self.user_flipped = pygame.transform.flip(self.user, True, False)    
        self.left_facing = False
        self.screen = pygame.display.set_mode((1600, 1000))
        self.x = x
        self.y = y
        self.position, self.velocity = pygame.math.Vector2(self.rect.center), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.friction = -.12


    def update(self,tileWall):
        '''self.horizontal_movement()
        self.checkCollisionsX(tileWall)
        self.vertical_movement()
        self.checkCollisionsY(tileWall)'''
        self.movement()

        if self.direction.magnitude() != 0: #Normalising diagonl movement in order to not gain extra acceleartion
            self.direction = self.direction.normalize()
        

        
        self.hitbox.x += self.direction.x * self.speed
        self.hitbox.y += self.direction.y * self.speed
        self.rect.center = self.hitbox.center

        if self.left_facing:
            self.image = self.user_flipped
        else:
            self.image = self.user

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.left_facing = True
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.left_facing = False
        else: 
            self.direction.x = 0
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
    
    def horizontal_movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.left_facing = True
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.left_facing = False
        else:
            self.direction.x = 0

    def vertical_movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.direction.y = -1
            print(1)
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
                
    
    
    def get_hits(self, tileWall):
        '''hits = []
        for tile in tileWall:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits'''
        #print(tileWall)
        hits = pygame.sprite.spritecollide(self, tileWall, False)
        return hits 

    def checkCollisionsX(self, tileWall):
        #self.rect.x, self.rect.y = tileWall.sprites()[0].rect.x, tileWall.sprites()[0].rect.y
        collisions = self.get_hits(tileWall)
        for tile in collisions:
            if self.direction.x > 0:
                self.hitbox.right = tile.rect.left
            elif self.direction.x < 0:
                self.hitbox.left = tile.rect.right
            self.rect.centerx = self.hitbox.centerx
            self.position.x = self.hitbox.centerx
    
    def checkCollisionsY(self, tileWall):
        #self.rect.x, self.rect.y = tileWall.sprites()[0].rect.x, tileWall.sprites()[0].rect.y
        collisions = self.get_hits(tileWall)
        for tile in collisions:
            if self.direction.y > 0:
                self.hitbox.bottom = tile.rect.top
            elif self.direction.y < 0:
                self.hitbox.top = tile.rect.bottom
            self.rect.centery = self.hitbox.centery
            self.position.y = self.hitbox.centery