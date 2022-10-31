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
        self.hitbox = self.rect.copy().inflate((-90,-90))
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
        self.movement()

        if self.direction.magnitude() != 0: #Normalising diagonl movement in order to not gain extra acceleartion
            self.direction = self.direction.normalize()
        
        #Horizontal movement
        self.position.x += self.direction.x * self.speed
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        self.checkCollisionsX(tileWall)

        
        #Vertical Movement
        self.position.y += self.direction.y * self.speed
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
        self.checkCollisionsY(tileWall)


        '''self.hitbox.x += self.direction.x * self.speed
        self.hitbox.y += self.direction.y * self.speed
        self.rect.center = self.hitbox.center'''

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
    
    def get_hits(self, tileWall):
        hits = pygame.sprite.spritecollide(self, tileWall, False)
        return hits 

    def checkCollisionsX(self, tileWall):
        collisions = self.get_hits(tileWall)
        for tile in collisions:
            if self.direction.x < 0:
                self.hitbox.right = tile.rect.left
            elif self.direction.x > 0:
                self.hitbox.left = tile.rect.right
            self.rect.centerx = self.hitbox.centerx
            self.position.x = self.hitbox.centerx
    
    def checkCollisionsY(self, tileWall):
        collisions = self.get_hits(tileWall)
        for tile in collisions:
            if self.direction.y < 0:
                self.hitbox.bottom = tile.rect.top
            elif self.direction.y > 0:
                self.hitbox.top = tile.rect.bottom
            self.rect.centery = self.hitbox.centery
            self.position.y = self.hitbox.centery