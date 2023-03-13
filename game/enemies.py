import pygame
from entities import Entities
import settings
import time
from ui import UI
import random


class Enemies(Entities):
    def __init__(self, game, enemy_type, coords, groups, collision_list, enemy_attacking_player):
        super().__init__(groups)
        self.collision_list = collision_list
        self.sprite_type = 'enemy'
        self.enemy_type = enemy_type
        
        # Animation
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.import_animations(enemy_type)
        self.chest_opened = False
        self.chest_opened_time = None
            
        # Larger size for bosses, shown my the scale to 100,100
        if enemy_type[-4::] == 'boss':
            self.image = pygame.transform.scale(self.animations[self.status][self.frame_index], (100,100))
            self.image2 = pygame.transform.scale(self.animations[self.status][self.frame_index], (100,100))
        else:
            self.image = self.animations[self.status][self.frame_index]
            self.image2 = self.animations[self.status][self.frame_index]
        self.left_facing = False

        # Movement
        self.rect = self.image.get_rect(topleft = (coords[1],coords[0]))
        self.hitbox = self.rect.inflate(40,35)
        self.position = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()

        # Stats
        enemy_info = settings.ENEMY_DATA[self.enemy_type]
        self.health = (enemy_info['health'] * (1.1**(1.3*settings.level_count))) + settings.enemies_killed
        self.exp = enemy_info["exp"]
        self.speed = enemy_info["speed"]
        self.attack_damage = enemy_info['damage']
        self.knockback = enemy_info['knockback']
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

        # Timers
        self.current_time = settings.current_time
        self.enemy_killed_time = None

    def import_animations(self,name):
        if name != 'chest':
            self.animations = {'attack':[],'idle':[],'move':[]}
            main_path = f'assets/sprites+items/enemies/{name}/'
            for animation in self.animations.keys():
                self.animations[animation] = settings.import_folder(main_path + animation)
        else:
            self.animations = {'idle':[],'open':[]}
            main_path = f'assets/sprites+items/chest/'
            for animation in self.animations.keys():
                self.animations[animation] = settings.import_folder(main_path + animation)

    # Prevents enemies from rapidly attacking the player when in range
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
    
    # Enemies get knocked backwards when attacked
    def get_knockback(self):
        if not self.vulnerable:
            self.direction *= -self.knockback

    # Function to damage the enemy if player has attacked
    def get_damage(self, player, amount):
        if self.vulnerable:
            self.direction = self.get_player_direction(player)[1]
            self.health -= amount * settings.player_stats['damage_multiplier']

        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False
    
    # Enemy triangulation of player location
    def get_player_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return (distance, direction)

    #  Checks enemy's health to make sure it's not 0, and if so, kills it and provides loot
    def check_for_death(self):
        if self.health <= 0:
            self.kill()
            settings.enemies_killed += 1
            self.enemy_killed_time = time.time()
            self.rng_item_drops()
  
    # Gets the status of the enemy, and changes the animation accordingly
    def get_status(self, player):
        distance = self.get_player_direction(player)[0]
        if self.enemy_type != 'chest':
            if distance <= self.attack_radius and self.can_attack:
                if self.status != 'attack':
                    self.frame_index = 0
                self.status = 'attack'
            elif distance <= self.notice_radius:
                self.status = 'move'
            else:
                self.status = 'idle'
        else:
            # If the item is a chest and has been opened, provides chest loot to the player
            keys = pygame.key.get_pressed()
            if (distance <= self.attack_radius) and keys[pygame.K_f] and not(self.chest_opened):
                self.status = 'open'
                self.chest_opened = True
                self.chest_opened_time = time.time()
                self.rng_item_drops()
    
    # Dependent on the enemies status, it either attacks, moves, or does nothing
    def actions(self,player):
                if self.status == 'attack':
                    self.attack_time = pygame.time.get_ticks()
                    self.enemy_attacking_player(self.attack_damage, self.attack_type)
                elif self.status == 'move':
                    self.direction = self.get_player_direction(player)[1]
                else:
                    self.direction = pygame.math.Vector2()
    
    # Provides the animation for the enemy
    def animate(self):
            animation = self.animations[self.status]

            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                if self.enemy_type != 'chest':
                    if self.status == 'attack':
                        self.can_attack = False
                self.frame_index = 0

            if self.enemy_type[-4::] == 'boss':
                self.image = pygame.transform.scale(self.animations[self.status][int(self.frame_index)], (100,100))
                self.image2 = pygame.transform.scale(self.animations[self.status][int(self.frame_index)], (100,100))
            else:
                self.image = self.animations[self.status][int(self.frame_index)]
                self.image2 = self.animations[self.status][int(self.frame_index)]
            self.rect = self.image.get_rect(center = self.hitbox.center)
    
    # Updates the enemy's physical actions through each frame, and calls the function required
    def update(self):
        if self.enemy_type != 'chest':
            self.get_knockback()
            # Scaling movement speed with time ended up being too fast, so I just made it a constant
            # Non-linear equation lead to speed being too fast 
            # Linear equation lead to the same but just at a slower rate
            # Cap on speed would have made the whole process irrelevant and added little to the game
            self.move(self.collision_list, self.speed)
        self.animate()
        self.cooldown()

    # Updates the enemy's statuses (non-physical) each frame, and calls the function required
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.check_for_death()

    # If the enemy is a chest and has been opened for 5 seconds, it disappears and the level is finished
    def chest_update(self, current_time):
        if self.chest_opened_time:
            if (current_time - self.chest_opened_time > 5) and (self.chest_opened):
                self.kill()
                settings.level_finished = True

    # Calculates the random item and powerup the chest drops 
    def drop_calculator(self):
        power_index = random.randint(0,2)
        item_index = random.randint(1,2)
        settings.player_items.append(list(settings.ITEM_DATA.keys())[item_index])
        settings.player_powerups.append(list(settings.POWER_UP_DATA.keys())[power_index])
       
        self.item_dropped()
        self.powerup_dropped()

    # Calculates, for all entities that drop loot, what loot they drop
    def rng_item_drops(self):
        
        # Chest drops a guaranteed a weapon and either a large health or damage potion
        if self.enemy_type == 'chest':
            
            weapon_value = random.randint(1,10) # 50 Percentage bracket
            if weapon_value < 5:
                settings.player_weapons.append(list(settings.WEAPON_DATA.keys())[weapon_value])
            
            elif (weapon_value > 4) and (weapon_value <= 7): # 30 Percentage bracket
                weapon_index = random.randint(1,4)
                settings.player_weapons.append(list(settings.WEAPON_DATA.keys())[weapon_index + 3])
            
            elif (weapon_value > 7) and (weapon_value <= 9): # 20 Percentage bracket
                weapon_index = random.randint(1,4)
                settings.player_weapons.append(list(settings.WEAPON_DATA.keys())[weapon_index + 7])
            
            elif weapon_value == 10: # 10 Percentage bracket
                weapon_index = random.randint(1,2)
                settings.player_weapons.append(list(settings.WEAPON_DATA.keys())[weapon_index + 11])
            
        # Guaranteed powerup or item
            self.drop_calculator()

        else:
        # Otherwise, if not a chest, it drops a random item (which is not guaranteed)
        # 16% drops a large health potion
        # 6% drops a damage potion
            value = random.randint(1,50)
            if (value <= 20) and (value >= 10):
                if (value >= 10) and (value <= 17):
                    settings.player_items.append(list(settings.ITEM_DATA.keys())[1])
                elif (value > 17) and (value <= 20):
                    settings.player_items.append(list(settings.ITEM_DATA.keys())[2])
                self.item_dropped()

    def item_dropped(self):
        settings.enemy_drop_item_time = time.time()

    def powerup_dropped(self):
        settings.enemy_drop_powerup_time = time.time()