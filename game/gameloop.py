# Goals:
# Time scaling

from tkinter import Y
import pygame
import buttoncontrol
from menu import OptionsMenu, MainMenu
from tilesheet import Tilesheet
from player import Player
from tiles import *
from ui import UI
from attack import Weapon
import settings
from enemies import Enemies
import random
from particles import ParticleObjects
import time
from roomgeneration import room_generation, get_player_spawn

pygame.font.init()
pygame.init()
FPS = 60
clock = pygame.time.Clock()

# Load Spritesheet for level
tilesheet = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)

# Game (EVERYTHING SCALED BY 2.5X (as per custom_draw))

class Game:
    
    def __init__(self, screen, spawn_point, room_coords):
        self.map = Tilemap('assets/map/MapTest2.csv', tilesheet)
        self.clock = pygame.time.Clock()
        self.bg_colour = pygame.Color('black')
        self.tile_wall, self.collision_list = self.map.tile_wall, self.map.collision_list
        

        self.resumeButton = pygame.image.load("assets/buttons/Resume_Button.png").convert_alpha()
        self.tiles = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.screen = screen
        self.font = pygame.font.Font('assets/fonts/Fipps-Regular.otf', 80)
        self.visible_sprites = YSortCamera()
        self.damageable_sprites = pygame.sprite.Group()
        self.non_damageable_sprites = pygame.sprite.Group()

        self.y, self.x = spawn_point[0], spawn_point[1]
        self.tile_size = 16
        self.user = Player(self,self.x, self.y, [self.visible_sprites], self.create_attack, self.remove_attack, self.tile_wall, self.collision_list)
        self.UI = UI()
        self.current_attack = None
        self.enemy = None
        self.spawn_point = spawn_point
        self.coords = room_coords
        self.coords_removable = None
        self.boss_coords = None
        self.enemy_count = 0
        self.wave = 0
        self.wave_commencing = False
        self.chest_spawned = False
        
        self.ParticleObjects = ParticleObjects()
        
        # Timers
        self.end_of_round_time = 0
        self.boss_round_commencing_time = 0
        settings.current_time = None
        self.boss_killed_time = 0
        self.chest_spawned_time = 0
        

    def create_wave(self):
        self.wave_commencing = True
        self.wave += 1
        self.coords_removable = None
        self.coords_removable = []
        self.coords_removable.extend(self.coords)
        # 7 rooms

        for i in range(1,7):
            self.create_room_enemies()

            # Between 1 and 4 enemies per room
            # Add enemies to room and increase enemy count every time an enemy is added
            # Enemy count is used to determine when the wave is over

            # Differentiate between starting wave and other waves?
            # Starting wave has 1 enemy per room
            # Other waves have 1-4 enemies per room -> coordinate system
            # Other waves don't spawn enemies in the room you're in
            # Enemy FX when spawning?
        self.wave_commencing = False

    def create_boss_wave(self):
        self.wave += 1
        self.coords_removable = None
        self.coords_removable = []
        self.coords_removable.extend(self.coords)

        room_index = random.randint(0, (len(self.coords_removable)-1))

        self.create_boss(self.coords_removable[room_index])
        self.coords_removable.remove(self.coords_removable[room_index])    

    def game_loop(self, screen):
        #menu variables
        self.screen = screen
        game_paused = False
        total_waves = 2 #random.randint(1, 5)
        
        self.create_wave()

        run = True
        while run:
            settings.current_time = time.time()
            self.draw_window(self.wave, screen) #passes wave into UI - make wave system with enemies

            if self.user.dead:
                run = False
                self.restore()

                # Boss wave implementation
            
            # Timers

            # Announcement to boss wave coming up next
            if (settings.enemies_killed + 2 == self.enemy_count) and (self.wave + 1 == total_waves):
                self.boss_round_commencing_time = time.time()

            # Announcement to new wave coming up    
            elif (settings.enemies_killed + 2 == self.enemy_count) and (self.wave + 1 < total_waves):
                self.end_of_round_time = time.time()
            
            elif (settings.enemies_killed == self.enemy_count) and (self.wave == total_waves):
                self.boss_killed_time = time.time()
                if not self.chest_spawned:
                    self.display_chest(self.boss_coords)
                    self.chest_spawned = True
                    self.chest_spawned_time = time.time()
                
            # Need to get when enemies are killed in order to spawn item power up box

            if (settings.enemies_killed == self.enemy_count) and (self.wave < total_waves - 1):
                self.create_wave()
            elif (settings.enemies_killed == self.enemy_count) and (self.wave == total_waves - 1):
                self.create_boss_wave()



            # Options menu
            if game_paused == True: 
                optionsMenu = OptionsMenu(self.screen)
                game_paused = False
                optionsMenu.run()
                
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and (game_paused): #Unpause on escape if game is paused
                        game_paused = False
                    elif (event.key == pygame.K_ESCAPE) and (not game_paused): #Pause on escape
                        game_paused = True
                elif event.type == pygame.QUIT:
                    run = False

            pygame.display.update()

        pygame.quit()

    def create_attack(self):
        self.current_attack = Weapon(self.user,[self.visible_sprites, self.non_damageable_sprites])

    def remove_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
        
    def create_room_enemies(self):
        room_index = random.randint(0, (len(self.coords_removable)-1))
        old_coords = self.coords_removable[room_index]

        # 1-4 enemies per room
        if self.wave == 1:
            number_of_enemies = 2
        else:
            number_of_enemies = random.randint(2, 5)
            # if number_of_enemies = 0, spawn a chest in the room maybe?

        for i in range(1,number_of_enemies):
            rand_x = random.randint(-100, 100)
            rand_y = random.randint(-100, 100)
            new_coords = [old_coords[0] + rand_x, old_coords[1] + rand_y]
            self.create_enemy(new_coords)
            self.enemy_count += 1
        self.coords_removable.remove(self.coords_removable[room_index])

    def create_enemy(self, coords):
        enemy_value = random.randint(1,3)
        if enemy_value == 1:
            enemy_type = 'fire-demon'
        elif enemy_value == 2:
            enemy_type = 'goblin'
        elif enemy_value == 3:
            enemy_type = 'mage'

        self.enemy = Enemies(self, enemy_type, coords, [self.visible_sprites, self.damageable_sprites], self.collision_list, self.enemy_attacking_player)
     
    def create_boss(self, coords):
        enemy_value = random.randint(1,3)
        if enemy_value == 1:
            enemy_type = 'demon-boss'
        elif enemy_value == 2:
            enemy_type = 'goblin-boss'
        elif enemy_value == 3:
            enemy_type = 'giant-boss'

        self.enemy = Enemies(self, enemy_type, coords, [self.visible_sprites, self.damageable_sprites], self.collision_list, self.enemy_attacking_player)
        self.enemy_count += 1
        self.boss_coords = coords

    def player_attacking_enemy(self):
        if self.non_damageable_sprites:
            for non_damageable_sprite in self.non_damageable_sprites:
                collision = pygame.sprite.spritecollide(non_damageable_sprite, self.damageable_sprites, False)
                if collision:
                    for sprite in collision:
                        sprite.get_damage(self.user, Player.get_total_weapon_damage(self.user) * settings.player_stats['damage_multiplier'])
                        attack_type = 'blood'
                        self.ParticleObjects.create_particles(attack_type, sprite.rect.center, [self.visible_sprites])

    def enemy_attacking_player(self, amount, attack_type):
        if self.user.vulnerable:
            self.user.get_damage(amount)
            self.user.vulnerable = False
            self.user.hit_time = pygame.time.get_ticks()
            self.ParticleObjects.create_particles(attack_type, self.user.rect.center, [self.visible_sprites])

    def restore(self):
        # Reset player/game variables
        self.y, self.x = None, None
        self.coords = None

        # Game over screen
        self.UI.game_over_screen()

        settings.enemies_killed = 0
        main_menu = MainMenu()
        main_menu.run()

    def display_chest(self, coords):
        enemy_type = 'chest'
        self.enemy = Enemies(self, enemy_type, coords, [self.visible_sprites, self.damageable_sprites], self.collision_list, self.enemy_attacking_player)

    def draw_window(self, wave, screen):
        # print(settings.PLAYER_ITEMS, settings.PLAYER_POWER_UPS)
        # print(settings.PLAYER_WEAPONS)
        self.screen.fill(self.bg_colour)
        self.map.draw_map(self.screen)

        # Camera
        self.visible_sprites.custom_draw(self.user)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.user)
        self.player_attacking_enemy()

        # Displaying UI        
        self.user.display_PlayerUI(self.user)
        self.UI.display(self.user, wave, self.enemy_count, settings.enemies_killed)
        
        # Display round commencing screen
        if (settings.current_time - self.end_of_round_time) < 5:
            self.UI.next_round_indicator()
        
        # Display boss round commencing screen
        if (settings.current_time - self.boss_round_commencing_time) < 5:
            self.UI.boss_round_indicator()
        
        if self.chest_spawned:
            self.visible_sprites.chest_update(settings.current_time)

        # if settings.chest_items or rng -> current time & display the pop up for ~5 seconds
        #  and add to players usable inventory
        if (settings.current_time - settings.enemy_drop_item_time) < 5:
            self.UI.item_loot_box(settings.PLAYER_ITEMS[-1::][0])
        
        if (settings.current_time - settings.enemy_drop_powerup_time) < 5:
            # Display power up box
            self.UI.power_up_box(settings.PLAYER_POWER_UPS[-1::][0])
            # Apply power up
            power = settings.PLAYER_POWER_UPS[0]
            if power == 'speed-increase':
                settings.player_stats['speed'] += settings.POWER_UP_DATA[power]['speed']
            elif power == 'defense-increase':
                settings.player_stats['defense'] += settings.POWER_UP_DATA[power]['defense']
            elif power == 'damage-increase':
                settings.player_stats['damage_multiplier'] += settings.POWER_UP_DATA[power]['damage']
            else:
                settings.player_stats['health_multiplier'] += settings.POWER_UP_DATA[power]['health']
        pygame.display.flip()

class YSortCamera(pygame.sprite.Group): #Camera system
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.screen = pygame.display.set_mode((1600, 1000))

        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.ground_surf = self.screen

        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))    

    def center_target(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

        
    def custom_draw(self, user):    
        self.center_target(user)
        ground_offset = self.ground_rect.topleft - self.offset
        self.screen.blit(pygame.transform.scale(self.ground_surf, (4000,2500)) , ground_offset) # scale from 1600x1000 to 4000x2500

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            if (hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy') and (sprite.enemy_type[-4::] == 'boss'):
                self.screen.blit(pygame.transform.scale(sprite.image , (120,120)), offset_pos)
            else:
                self.screen.blit(pygame.transform.scale(sprite.image , (50,50)), offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def chest_update(self, current_time):
        chest_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.enemy_type == 'chest']
        for chest in chest_sprites:
            chest.chest_update(current_time)

