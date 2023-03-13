
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
pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()
FPS = 60
clock = pygame.time.Clock()

# Load Spritesheet for level
tilesheet = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)

# Start the game background music
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Game (EVERYTHING SCALED BY 2.5X (as per custom_draw))

class Game:
    
    def __init__(self, screen, spawn_point, room_coords, wave, enemy_count, level_count):
        self.map = Tilemap('assets/map/MapTest2.csv', tilesheet)
        self.clock = pygame.time.Clock()
        self.bg_colour = pygame.Color('black')
        self.tile_wall, self.collision_list = self.map.tile_wall, self.map.collision_list
        self.level_count = level_count
        

        self.resumeButton = pygame.image.load("assets/buttons/Resume_Button.png").convert_alpha()
        self.tiles = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.screen = screen
        self.font = pygame.font.Font('assets/fonts/Fipps-Regular.otf', 80)
        self.visible_sprites = Camera()
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
        self.enemy_count = enemy_count
        self.wave = wave
        self.wave_commencing = False
        self.chest_spawned = False
        self.powerup_applied = False
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
            # Between 1 and 4 enemies per room
            # Add enemies to room and increase enemy count every time an enemy is added
            # Enemy count is used to determine when the wave is over

            # Starting wave has 1 enemy per room
            # Other waves have 1-4 enemies per room
            self.create_room_enemies()
  
        self.wave_commencing = False

    # Creates the special wave for the boss round (only the boss spawns)
    def create_boss_wave(self):
        self.wave += 1
        self.coords_removable = None
        self.coords_removable = []
        self.coords_removable.extend(self.coords)

        room_index = random.randint(0, (len(self.coords_removable)-1))

        self.create_boss(self.coords_removable[room_index])
        self.coords_removable.remove(self.coords_removable[room_index])    

    def game_loop(self, screen):
        self.screen = screen
        game_paused = False
        total_waves = (random.randint(2, 5)) + self.wave
       
        # Creates the first wave
        self.create_wave()

        run = True
        while run:
            settings.current_time = time.time()
            # Passes wave into UI, allowing it to be displayed
            self.draw_window(self.wave, screen) 

            # Checks if the player is dead and if so, ends the current run through
            if self.user.dead:
                run = False
                self.restore()

            
            # Timers
            # Announcement to boss wave coming up next
            if (settings.enemies_killed + 2 == self.enemy_count) and (self.wave + 1 == total_waves):
                self.boss_round_commencing_time = time.time()

            # Announcement to new wave coming up    
            elif (settings.enemies_killed + 2 == self.enemy_count) and (self.wave + 1 < total_waves):
                self.end_of_round_time = time.time()
            
            # Sets the time of when the boss is killed
            elif (settings.enemies_killed == self.enemy_count) and (self.wave == total_waves):
                self.boss_killed_time = time.time()
                # Spawns the chest and makes a note of the time
                if not self.chest_spawned:
                    self.display_chest(self.boss_coords)
                    self.chest_spawned = True
                    self.chest_spawned_time = time.time()
                # If the items have been received from the chest and the time is sufficient, 
                # the new level begins
                elif settings.level_finished:
                    settings.level_finished = False
                    self.new_level()
                
            # Increases wave count and creates a new wave
            if (settings.enemies_killed == self.enemy_count) and (self.wave < total_waves - 1):
                settings.waves_completed += 1
                self.create_wave()
            # Creates the boss wave if at the final wave
            elif (settings.enemies_killed == self.enemy_count) and (self.wave == total_waves - 1):
                self.create_boss_wave()
            
            # If paused, grants the options menu
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

    # Creates an instance of the players weapon
    def create_attack(self):
        self.current_attack = Weapon(self.user,[self.visible_sprites, self.non_damageable_sprites])

    # Removes the players weapon from the screen once attacked
    def remove_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    # Creates all the enemies which occupy a room
    def create_room_enemies(self):
        room_index = random.randint(0, (len(self.coords_removable)-1))
        old_coords = self.coords_removable[room_index]

        # 1-4 enemies per room
        if self.wave == 1:
            number_of_enemies = 2
        else:
            number_of_enemies = random.randint(2, 5)

        # Randomly shifts the enemies coordinates so they are not all in the same place
        for i in range(1,number_of_enemies):
            rand_x = random.randint(-100, 100)
            rand_y = random.randint(-100, 100)
            new_coords = [old_coords[0] + rand_x, old_coords[1] + rand_y]
            self.create_enemy(new_coords)
            self.enemy_count += 1
        # Removes the coordinates so future enemies are not spawned in the same room
        self.coords_removable.remove(self.coords_removable[room_index])

    # Randomly determines which enemy is going to be spawned and creates an instance of it
    def create_enemy(self, coords):
        enemy_value = random.randint(1,3)
        if enemy_value == 1:
            enemy_type = 'fire-demon'
        elif enemy_value == 2:
            enemy_type = 'goblin'
        elif enemy_value == 3:
            enemy_type = 'mage'

        self.enemy = Enemies(self, enemy_type, coords, [self.visible_sprites, self.damageable_sprites], self.collision_list, self.enemy_attacking_player)
     
    # Randomly determines which boss is going to be spawned and creates an instance of it in a random room
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
        # Sets the boss coordinates so the chest can be spawned in the same room
        self.boss_coords = coords
    
    # If the player is attacking the enemy, creates the player damaging particles
    def player_attacking_enemy(self):
        if self.non_damageable_sprites:
            for non_damageable_sprite in self.non_damageable_sprites:
                collision = pygame.sprite.spritecollide(non_damageable_sprite, self.damageable_sprites, False)
                if collision:
                    for sprite in collision:
                        sprite.get_damage(self.user, Player.get_total_weapon_damage(self.user) * settings.player_stats['damage_multiplier'])
                        attack_type = 'blood'
                        self.ParticleObjects.create_particles(attack_type, sprite.rect.center, [self.visible_sprites])

    # If the enemy is attacking the player, creates the enemy specific attacking partiles
    # The user also takes damage based on the amount of damage the enemy deals with 
    # respect to the players defense level and time elapsed
    # The user is also made invulnerable for a short period of time, in order to prevent the player
    # from taking damage from multiple enemies at once
    def enemy_attacking_player(self, amount, attack_type):
        if self.user.vulnerable:
            self.user.get_damage(amount * settings.player_stats['defense'])
            self.user.vulnerable = False
            self.user.hit_time = pygame.time.get_ticks()
            self.ParticleObjects.create_particles(attack_type, self.user.rect.center, [self.visible_sprites])

    # Rests the player coordinates 
    def restore(self):
        # Reset player/game variables
        self.y, self.x = None, None
        self.coords = None

        # Game over screen
        self.UI.game_over_screen()

        settings.enemies_killed = 0
        main_menu = MainMenu()
        main_menu.run()

    # Creates the next level (a completely new game instance with previous stats carried over)
    def new_level(self):
        room_center_points = None
        spawn_point = None
        room_center_points = room_generation()
        spawn_point = get_player_spawn(room_center_points)
        room_center_points.remove(spawn_point)
        settings.level_count += 1

        game = Game(self.screen, spawn_point, room_center_points, self.wave, self.enemy_count, settings.level_count)
        game.game_loop(self.screen)
        del game

    # Displays the chest
    def display_chest(self, coords):
        enemy_type = 'chest'
        self.enemy = Enemies(self, enemy_type, coords, [self.visible_sprites, self.damageable_sprites], self.collision_list, self.enemy_attacking_player)

    # Updates the game with elements which take place on the screen
    def draw_window(self, wave, screen):
        # Displaying map
        self.screen.fill(self.bg_colour)
        self.map.draw_map(self.screen)

        # Camera
        self.visible_sprites.custom_draw(self.user)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.user)
        self.player_attacking_enemy()

        # Displaying UI (player health, current round and enemies left)        
        self.user.display_PlayerUI(self.user)
        self.UI.display(self.user, wave, self.enemy_count, settings.enemies_killed)
        
        # Display round commencing screen for 5 seconds when required
        if (settings.current_time - self.end_of_round_time) < 5:
            self.UI.next_round_indicator()
        
        # Display boss round commencing screen for 5 seconds when required
        if (settings.current_time - self.boss_round_commencing_time) < 5:
            self.UI.boss_round_indicator()
        
        # If a chest is on the map, update it with the required methods
        if self.chest_spawned:
            self.visible_sprites.chest_update(settings.current_time)

        # If the player has picked up an item, display the item for 3 seconds
        if (settings.current_time - settings.enemy_drop_item_time) < 3:
            self.UI.item_loot_box(settings.player_items[-1::][0])
        
        # If the player has picked up a powerup, display the powerup for 3 seconds
        if (settings.current_time - settings.enemy_drop_powerup_time) < 3:
            # Display power up box
            x = settings.player_powerups[-1::][0]
            self.UI.power_up_box(x)

        # After 3 seconds, the powerup is popped from the players powerup list
        if (settings.current_time - settings.enemy_drop_powerup_time) == 3:
            settings.player_powerups.pop()
            
        # Uses the player's powerup if the player has one
        if settings.player_powerups and not self.powerup_applied:
            # Apply power up
            power = settings.player_powerups[0]
            if power == 'speed-increase':
                settings.player_stats['speed'] += settings.POWER_UP_DATA[power]['speed']
            elif power == 'defense-increase':
                settings.player_stats['defense'] -= settings.POWER_UP_DATA[power]['defense']
            elif power == 'damage-increase':
                settings.player_stats['damage_multiplier'] += settings.POWER_UP_DATA[power]['damage']
            else:
                settings.player_stats['health_multiplier'] += settings.POWER_UP_DATA[power]['health']
            self.powerup_applied = True


            pygame.display.flip()

class Camera(pygame.sprite.Group): #Camera system
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.ground_surf = self.screen

        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))    

    def center_target(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    # Creates a zoom and follows the player with the use of the center target function
    def custom_draw(self, user):    
        self.center_target(user)
        ground_offset = self.ground_rect.topleft - self.offset
        self.screen.blit(pygame.transform.scale(self.ground_surf, (4000,2500)) , ground_offset) # scale from 1600x1000 to 4000x2500

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            # Bosses are larger than normal enemies
            if (hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy') and (sprite.enemy_type[-4::] == 'boss'):
                self.screen.blit(pygame.transform.scale(sprite.image , (120,120)), offset_pos)
            else:
                self.screen.blit(pygame.transform.scale(sprite.image , (50,50)), offset_pos)

    # Updates the enemies on the screen (all which are alive)
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    # Updates the chest if currently on the map
    def chest_update(self, current_time):
        chest_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.enemy_type == 'chest']
        for chest in chest_sprites:
            chest.chest_update(current_time)

