from tkinter import Y
import pygame
import buttoncontrol
from menu import OptionsMenu
from tilesheet import Tilesheet
from player import Player
from tiles import *
pygame.font.init()
pygame.init()
from tiles import Tilemap
map = Tilemap('assets/map/MapTest3.csv', tilesheet)


# Load Spritesheet for level
tilesheet = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)


# Game (EVERYTHING SCALED BY 2.5X (as per line 131))

class Game:
    
    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.bg_colour = pygame.Color('black')
        self.resumeButton = pygame.image.load("assets/buttons/Resume_Button.png").convert_alpha()
        self.tiles = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.screen = screen
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCamera()
        # self.obstacle_sprites = pygame.sprite.Group()
        # self.user = Player(self,1250,1300, [self.visible_sprites], self.obstacle_sprites)
        self.tile_size = 16
        # visible_sprites = YSortCamera()
        # obstacle_sprites = pygame.sprite.Group()
        self.user = Player(self,1250,1300, self.visible_sprites)
        self.map = Tilemap('assets/map/MapTest3.csv', tilesheet)


    def game_loop(self, screen):
         #menu variables
        self.screen = screen
        game_paused = False

        run = True
        while run:

            self.draw_window()
            # self.user.add(self.user)


            if game_paused == True: #options menu
                optionsMenu = OptionsMenu(self.screen)
                game_paused = False
                optionsMenu.run()
                

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and (game_paused == True): #Unpause on escape if game is paused
                        game_paused = False
                    elif (event.key == pygame.K_ESCAPE) and (game_paused == False): #Pause on escape
                        game_paused = True
                elif event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    
    def draw_window(self):
        self.screen.fill(self.bg_colour)
        # self.tiles.draw(self.screen) for identifying tiles
        self.map.draw_map(self.display_surface)
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.user)
        pygame.display.flip()

    '''def draw_text(self, text,font, text_colour, x , y):
        img = font.render(text, True, text_colour)
        self.screen.blit(img, (x,y))'''

class YSortCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.screen = pygame.display.set_mode((1600, 1000))

        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.ground_surf = self.display_surface

        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))    
    
    def center_target(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

        
    def custom_draw(self, user):    
        self.center_target(user)
        ground_offset = self.ground_rect.topleft - self.offset
        self.screen.blit(pygame.transform.scale(self.ground_surf, (4000,2500)) , ground_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(pygame.transform.scale(sprite.image , (60,60)), offset_pos)
           
