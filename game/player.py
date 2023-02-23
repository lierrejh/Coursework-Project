# Goals:
# Time scaling

import pygame 
from tilesheet import Tilesheet
from tiles import *
import settings
from ui import UI
from entities import Entities

CARDINAL_DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]


class Player(Entities): # Character class
    def __init__(self, game, x , y, group, create_attack, remove_attack, tile_wall, collision_list): # Organise init
        super().__init__(group)
        self.color = (250,0,0)
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.game = game
        self.left_pressed = False
        self.right_pressed = False
        self.speed = 4
        self.tile_wall, self.collision_list = tile_wall, collision_list
        self.image = pygame.image.load('assets/sprites+items/individual_sprites/StartingCharacter.png').convert_alpha()
        self.image2 = pygame.image.load('assets/sprites+items/individual_sprites/StartingCharacter.png').convert_alpha()
        self.direction = pygame.math.Vector2() 
        self.userTile = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.image_flipped = pygame.transform.flip(self.image, True, False)    
        self.left_facing = False
        self.x = x
        self.y = y
        self.user_scaled = pygame.transform.scale(self.image2, (25,40))
        self.rect = self.user_scaled.get_rect(center = (self.x ,self.y))
        self.position = pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect.inflate(40,35)
        self.display_surface = pygame.display.get_surface()
        
        #Health System
        self.current_health = 1000
        self.maximum_health = 1000
        self.health_bar_length = 600
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.target_health = 1000
        self.health_change_speed = 10
        self.vulnerable = True
        self.hit_time = None
        self.invulnerability_duration = 500
        self.dead = False

        # Weapon Sysem
        self.weapon_index = 0
        self.item_index = 0
        self.player_busy = False
        self.can_switch_weapons = True
        self.weapon = list(settings.WEAPON_DATA.keys())[self.weapon_index]
        self.item = list(settings.ITEM_DATA.keys())[self.item_index]
        self.switch_duration_cooldown = 1000
        self.create_attack = create_attack
        self.attack_cooldown = 200
        
            # Set by ticks
        self.switch_time = 0 
        self.attack_time = 0
       
        self.remove_attack = remove_attack
    
    def update(self):
        self.check_for_death()
        self.movement_inputs()
        self.attack_inputs(self.collision_list)
        self.cooldowns()
        self.move(self.collision_list, 0)
        '''for tile in tileWall: #Testing wall boundary
            pygame.draw.rect(
                self.screen,self.color, tile)'''
        
        '''if self.direction.magnitude() != 0: #Normalising diagonl movement in order to not gain extra acceleartion
            self.direction = self.direction.normalize()'''

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health = max(self.target_health - amount, 0)
        if self.target_health <= 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.maximum_health:
            self.target_health = max(self.target_health + amount, 0)
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
            # self.get_health(100)
        elif keys[pygame.K_s]:
            self.direction.y = 1
            # self.get_damage(100)
        else:
            self.direction.y = 0

    def misc_inputs(self, player):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Cycle healing item if E is pressed
        if keys[pygame.K_e] and (not self.player_busy) and (self.can_switch_weapons) and (current_time - self.switch_time >= self.switch_duration_cooldown):
            self.player_busy = True
            self.can_switch_weapons = False
            self.switch_time = pygame.time.get_ticks()
			
            if self.item_index < len(list(settings.ITEM_DATA.keys())) - 1:
                self.item_index += 1
            else:
                self.item_index = 0
				
            self.item = list(settings.ITEM_DATA.keys())[self.item_index]

        if keys[pygame.K_f] and (not self.player_busy) and (self.can_switch_weapons) and (current_time - self.switch_time >= self.switch_duration_cooldown):
            self.player_busy = True
            self.can_switch_weapons = False
            self.switch_time = pygame.time.get_ticks()

            # Use item
            player.get_health(settings.ITEM_DATA[player.item]["health"])

    def check_for_death(self):
        if self.current_health <= 0:
            self.dead = True
    
    def attack_inputs(self, collision_list):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        # Cycle weapon if Q is pressed and the player is not busy
        if keys[pygame.K_q] and (not self.player_busy) and (self.can_switch_weapons) and (current_time - self.switch_time >= self.switch_duration_cooldown):
            self.player_busy = True
            self.can_switch_weapons = False
            self.switch_time = pygame.time.get_ticks()
			
            if self.weapon_index < len(list(settings.WEAPON_DATA.keys())) - 1:
                self.weapon_index += 1
            else:
                self.weapon_index = 0
				
            self.weapon = list(settings.WEAPON_DATA.keys())[self.weapon_index]
        
        # Attack
        attack_duration_cooldown = settings.WEAPON_DATA.get(f'{self.weapon}').get('cooldown')

        colliding = False
        collisions = self.get_hits(collision_list)
        if collisions:
            colliding = True
        else:
            colliding = False

        if keys[pygame.K_SPACE] and (not self.player_busy) and ((current_time - self.attack_time >= attack_duration_cooldown)) and not colliding:
            # Can not attack if player moving in a diagonal direction
            if self.direction in CARDINAL_DIRECTIONS: 
                self.player_busy = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
        
        self.misc_inputs(self)

    def cooldowns(self):
        #UI.cooldown_bar(self)
        current_time = pygame.time.get_ticks()
        
        if not self.can_switch_weapons:
                    if current_time - self.switch_time >= self.switch_duration_cooldown:
                        self.can_switch_weapons = True

                        
        if self.player_busy:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.player_busy = False
                self.remove_attack()
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invulnerability_duration:
                self.vulnerable = True

    def get_total_weapon_damage(self):
        weapon_damage = settings.WEAPON_DATA[self.weapon]['damage']
        return weapon_damage