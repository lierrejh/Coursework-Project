import pygame
from entities import Entities
from settings import *
import aid

class Enemies(Entities):
    def __init__(self, game, enemy_type, coords, groups, collision_list, enemy_attacking_player):
        super().__init__(groups)
        self.collision_list = collision_list
        self.sprite_type = 'enemy'

        
        # Animation
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.import_animations(enemy_type)
        self.image = self.animations[self.status][self.frame_index]
        self.image2 = self.animations[self.status][self.frame_index]
        self.image_flipped = pygame.transform.flip(self.image, True, False)   
        self.left_facing = False


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
        self.attack_type = enemy_info['attack_type']

        # Player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.enemy_attacking_player = enemy_attacking_player

        # Damaging system
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def import_animations(self,name):
        self.animations = {'attack':[],'idle':[],'move':[]}
        main_path = f'assets/sprites+items/enemies/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = aid.import_folder(main_path + animation)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
            
    def knockback(self):
        if not self.vulnerable:
            self.direction *= -5

    def get_damage(self, player, amount):
        if self.vulnerable:
            self.direction = self.get_player_direction(player)[1]
            self.health -= amount

        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False

    
    def get_player_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return (distance, direction)

    def check_for_death(self):
        if self.health <= 0:
            self.kill()
   
    def get_status(self, player):
        distance = self.get_player_direction(player)[0]
        
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def actions(self,player):
                if self.status == 'attack':
                    self.attack_time = pygame.time.get_ticks()
                    self.enemy_attacking_player(self.attack_damage, self.attack_type)
                elif self.status == 'move':
                    self.direction = self.get_player_direction(player)[1]
                else:
                    self.direction = pygame.math.Vector2()
    
    def animate(self):
            animation = self.animations[self.status]

            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                if self.status == 'attack':
                    self.can_attack = False
                self.frame_index = 0

            self.image = animation[int(self.frame_index)]
            self.rect = self.image.get_rect(center = self.hitbox.center)
    
    def update(self):
        self.knockback()
        self.move(self.collision_list, self.speed)
        self.animate()
        self.cooldown()


    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.check_for_death()