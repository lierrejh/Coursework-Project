import pygame 
from tilesheet import Tilesheet
from tiles import *
from settings import *


tilesheet = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
map = Tilemap('assets/map/MapTest3.csv', tilesheet)
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite): # Character class
    def __init__(self, game, x , y, group, create_attack, remove_attack): # Organise init
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
        self.user_scaled = pygame.transform.scale(self.user, (25,40))
        self.rect = self.user_scaled.get_rect(center = (self.x ,self.y))
        self.position = pygame.math.Vector2(self.rect.center)
        #self.hitbox = self.rect.copy().inflate((25,40))
        self.hitbox = self.rect.inflate(40,35)
        self.display_surface = pygame.display.get_surface()
        
        #Health System
        self.current_health = 1000
        self.maximum_health = 1000
        self.health_bar_length = 600
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.target_health = 1000
        self.health_change_speed = 5

        #Weapon Sysem
        self.weapon_index = 0
        self.player_busy = False
        self.can_switch_weapons = True
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        self.create_attack = create_attack
        self.attack_time = None
        self.attack_cooldown = 400
        self.remove_attack = remove_attack

    def update(self,tileWall,collisionList):
        self.movement_inputs()
        self.attack_inputs()
        self.cooldowns()

        '''for tile in tileWall: #Testing wall boundary
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
        if self.target_health <= 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.maximum_health:
            self.target_health += amount
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health
    
    def advanced_health_bar(self):
        transition_width = 0
        transition_color = (100,0,0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (0,100,0)
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) /self.health_ratio)
            transition_color = (255, 255, 0)   

        health_bar_rect = pygame.Rect(50,45,self.current_health/self.health_ratio, 25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 45, transition_width, 25)

        pygame.draw.rect(self.display_surface, (100, 0, 0) , health_bar_rect)
        pygame.draw.rect(self.display_surface, transition_color, transition_bar_rect)
        pygame.draw.rect(self.display_surface,(255,255,255),(50,45,self.health_bar_length,25),4)

    def display_PlayerUI(self, player):
        self.advanced_health_bar()

    def movement_inputs(self):
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

    def attack_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and (self.player_busy == False) and (self.can_switch_weapons == True): #Cycle weapon
            self.player_busy = True
            self.can_switch_weapons = False
            self.weapon_switch_time = pygame.time.get_ticks()
			
            if self.weapon_index < len(list(weapon_data.keys())) - 1:
                self.weapon_index += 1
            else:
                self.weapon_index = 0
				
            self.weapon = list(weapon_data.keys())[self.weapon_index]
        
        if keys[pygame.K_SPACE] and (self.player_busy == False): # Attack
            self.player_busy = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if not self.can_switch_weapons:
                    if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                        self.can_switch_weapons = True
                        self.player_busy = False
                        
        if self.player_busy:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.player_busy = False
                self.remove_attack()

        