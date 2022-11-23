import pygame 
from tilesheet import Tilesheet
from tiles import *


tilesheet = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
map = Tilemap('assets/map/MapTest3.csv', tilesheet)
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite): #Character class
    def __init__(self, game, x , y, group):#, groups):#, groups)
        super().__init__(group)
        self.color = (250,0,0)
        self.screen = pygame.display.set_mode((1600, 1000))
        self.game = game
        self.left_pressed, self.right_pressed = False, False
        self.speed = 4
        #self.image = pygame.image.load('assets/sprites+items/individual_sprites/0x72_16x16DungeonTileset-245.png').convert_alpha()
        self.image = pygame.image.load('assets/sprites+items/individual_sprites/StartingCharacter.png').convert_alpha()
        self.direction = pygame.math.Vector2() 
        self.userTile = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.user_flipped = pygame.transform.flip(self.image, True, False)    
        self.left_facing = False
        self.x = x
        self.y = y
        #self.user = self.userTile.get_tile(15, 15), (400,400)
        self.user = pygame.image.load('assets/sprites+items/individual_sprites/StartingCharacter.png').convert_alpha()
        self.rect = self.user.get_rect(center = (self.x,self.y))
        self.position = pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect.copy().inflate((25,50))
        self.display_surface = pygame.display.get_surface()

        
        #Health System
        self.current_health = 1000
        self.maximum_health = 1000
        self.health_bar_length = 600
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.target_health = 500
        self.health_change_speed = 5

        #UI Sysem


    def update(self,tileWall,collisionList):
        self.movement()

        '''for tile in tileWall:
            pygame.draw.rect(
                self.screen,self.color, tile)'''
        
        '''if self.direction.magnitude() != 0: #Normalising diagonl movement in order to not gain extra acceleartion
            self.direction = self.direction.normalize()'''

        #Horizontal movement
        self.position.x += self.direction.x * self.speed
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        self.checkCollisionsX(collisionList)

        
        #Vertical Movement
        self.position.y += self.direction.y * self.speed
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
        self.checkCollisionsY(collisionList)

        if self.left_facing:
            self.image = self.user_flipped
        else:
            self.image = self.user
        
    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.maximum_health:
            self.target_health += amount
        if self.target_health > self.maximum_health:
            self.target_health = self.maximum_health
    
    def advanced_health_bar(self):
        transition_width = 0
        transition_color = (255,0,0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (0,255,0)
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) /self.health_ratio)
            transition_color = (255, 255, 0)   

        health_bar_rect = pygame.Rect(50,45,self.current_health/self.health_ratio, 25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 45, transition_width, 25)

        pygame.draw.rect(self.display_surface, (255, 0, 0) , health_bar_rect)
        pygame.draw.rect(self.display_surface, transition_color, transition_bar_rect)
        pygame.draw.rect(self.display_surface,(255,255,255),(50,45,self.health_bar_length,25),4)

    def display_PlayerUI(self, player):
        self.advanced_health_bar()
        #pygame.draw.rect(self.display_surface, (255,255,255), self.health_bar_rect)


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
            self.get_health(100)
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.get_damage(100)
        else:
            self.direction.y = 0
    
    def get_hits(self, collisionList):
        '''hits = pygame.sprite.spritecollide(self, collisionList, False)
        return hits'''
        hits = []
        for tile in collisionList:
            if self.hitbox.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsX(self, collisionList):
        collisions = self.get_hits(collisionList)
        for tile in collisions:
            if self.direction.x > 0: #Moving right
                self.hitbox.right = tile.rect.left
                self.position.x = self.rect.centerx
            elif self.direction.x < 0: #Moving left
                self.hitbox.left = tile.rect.right
                self.position.x = self.rect.centerx
            self.rect.centerx = self.hitbox.centerx
            self.position.x = self.rect.centerx

    
    def checkCollisionsY(self, collisionList):
        collisions = self.get_hits(collisionList)
        for tile in collisions:
            if self.direction.y > 0:
                self.hitbox.bottom = tile.rect.top
            elif self.direction.y < 0:
                self.hitbox.top = tile.rect.bottom
            self.rect.centery = self.hitbox.centery
            self.position.y = self.hitbox.centery