from tkinter import Y
import pygame
import buttoncontrol
from menu import OptionsMenu
from tilesheet import Tilesheet
from player import Player
from tiles import *
from ui import UI
from attack import Weapon

pygame.font.init()
pygame.init()
map = Tilemap('assets/map/MapTest3.csv', tilesheet)
FPS = 60
clock = pygame.time.Clock()

# Load Spritesheet for level
tilesheet = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)

# Game (EVERYTHING SCALED BY 2.5X (as per custom_draw))

class Game:
    
    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.bg_colour = pygame.Color('black')
        self.resumeButton = pygame.image.load("assets/buttons/Resume_Button.png").convert_alpha()
        self.tiles = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.screen = screen
        self.visible_sprites = YSortCamera()
        # self.obstacle_sprites = pygame.sprite.Group()
        # self.user = Player(self,1250,1300, [self.visible_sprites], self.obstacle_sprites)
        self.tile_size = 16
        # visible_sprites = YSortCamera()
        # obstacle_sprites = pygame.sprite.Group()
        self.user = Player(self,1250,1300, self.visible_sprites, self.create_attack, self.remove_attack)
        self.UI = UI()
        self.current_attack = None


    def game_loop(self, screen):
        #menu variables
        self.screen = screen
        game_paused = False

        run = True
        wave = 0
        while run:
            self.dt = clock.tick(60) * .001 * FPS
            self.draw_window(wave) #passes wave into UI - make wave system with enemies

            if game_paused == True: #options menu
                optionsMenu = OptionsMenu(self.screen)
                game_paused = False
                optionsMenu.run()
                
            keys = pygame.key.get_pressed() #testing wave system
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and (game_paused == True): #Unpause on escape if game is paused
                        game_paused = False
                    elif (event.key == pygame.K_ESCAPE) and (game_paused == False): #Pause on escape
                        game_paused = True
                    elif keys[pygame.K_f]: #testing wave system / remove later
                        wave += 1
                elif event.type == pygame.QUIT:
                    run = False

            pygame.display.update()

        pygame.quit()

    def create_attack(self):
        self.current_attack = Weapon(self.user,self.visible_sprites)

    def remove_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def draw_window(self, wave):
        self.screen.fill(self.bg_colour)
        # self.tiles.draw(self.screen) for identifying tiles
        map.draw_map(self.screen)
        #self.visible_sprites.update(map.tileWall)
        self.user.update(map.tileWall, map.collisionList)
        self.visible_sprites.custom_draw(self.user)
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
 


