import pygame
from entities import Entities
from settings import *

class Enemies(Entities):
    def __init__(self, game, enemy_type, coords, groups, collision_list):
        super().__init__(groups)
        self.collision_list = collision_list
        self.sprite_type = 'enemy'
        self.image = pygame.image.load(ENEMY_DATA[enemy_type]['image']).convert_alpha()
        self.image2 = pygame.image.load(ENEMY_DATA[enemy_type]['image']).convert_alpha()
        self.status = 'idle'
        
        # Movement
        self.rect = self.image.get_rect(topleft = (coords[1],coords[0]))
        self.hitbox = self.rect.inflate(40,35)
        self.position = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.left_facing = False
        self.image_flipped = pygame.transform.flip(self.image, True, False)    

        # Stats
        self.enemy_type = enemy_type
        enemy_info = ENEMY_DATA[self.enemy_type]
        self.health = enemy_info['health']
        self.exp = enemy_info["exp"]
        self.speed = enemy_info["speed"]
        self.attack_damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400

    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    
    def get_player_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        print(distance)
        
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_direction(player)[0]
        if distance <= self.attack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def actions(self,player):
                if self.status == 'attack':
                    self.attack_time = pygame.time.get_ticks()
                    print('attack')
                elif self.status == 'move':
                    self.direction = self.get_player_direction(player)[1]
                else:
                    self.direction = pygame.math.Vector2()

    def update(self):
        self.move(self.collision_list, self.speed)
        self.cooldown()


    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)