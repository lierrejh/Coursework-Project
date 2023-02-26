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
        self.enemy_count = 0
        self.wave = 0
        
        self.ParticleObjects = ParticleObjects()

    def create_wave(self):
        self.enemy_count = 0
        self.wave += 1
        print(self.coords_removable)
        self.coords_removable = None
        print("after none", self.coords_removable)
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

    def game_loop(self, screen):
        #menu variables
        self.screen = screen
        game_paused = False
        total_waves = random.randint(1, 5)
        
        self.create_wave()

        run = True
        while run:
            self.dt = clock.tick(60) * .001 * FPS
            self.draw_window(self.wave) #passes wave into UI - make wave system with enemies

            if self.user.dead:
                run = False
                self.restore()

            # Boss implementation
            if (settings.enemies_killed == self.enemy_count) and (self.wave < total_waves):
                self.create_wave()

            if game_paused == True: #options menu
                optionsMenu = OptionsMenu(self.screen)
                game_paused = False
                optionsMenu.run()
                
            keys = pygame.key.get_pressed() #testing wave system
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and (game_paused): #Unpause on escape if game is paused
                        game_paused = False
                    elif (event.key == pygame.K_ESCAPE) and (not game_paused): #Pause on escape
                        game_paused = True
                    elif keys[pygame.K_f]: #testing wave system / remove later
                        pass
                        # wave += 1
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

        
    def player_attacking_enemy(self):
        if self.non_damageable_sprites:
            for non_damageable_sprite in self.non_damageable_sprites:
                collision = pygame.sprite.spritecollide(non_damageable_sprite, self.damageable_sprites, False)
                if collision:
                    for sprite in collision:
                        sprite.get_damage(self.user, Player.get_total_weapon_damage(self.user))
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

    def draw_window(self, wave):
        self.screen.fill(self.bg_colour)
        # self.tiles.draw(self.screen) for identifying tiles
        self.map.draw_map(self.screen)

        # Camera
        self.visible_sprites.custom_draw(self.user)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.user)
        self.player_attacking_enemy()


        # Displaying UI        
        self.user.display_PlayerUI(self.user)
        self.UI.display(self.user, wave)
        
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
            self.screen.blit(pygame.transform.scale(sprite.image , (50,50)), offset_pos)
            #self.screen.blit(sprite.image , offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

