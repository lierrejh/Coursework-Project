from tkinter import Y
import pygame
import buttoncontrol
from menu import OptionsMenu
from tilesheet import Tilesheet
from player import Player
from tilemap import *
pygame.font.init()
pygame.init()
from tilemap import Tilemap
# Load Spritesheet for level
tilesheet = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
map = Tilemap('assets/map/MapTest3.csv', tilesheet)

# Game (EVERYTHING SCALED BY 2 (as per line 131))

class Game:
    
    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.bg_colour = pygame.Color('black')
        self.resumeButton = pygame.image.load("assets/buttons/Resume_Button.png").convert_alpha()
        self.tiles = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.screen = screen
        self.display_surface = pygame.display.get_surface()
        self.camera_group = YSortCamera()
        self.user = Player(self,768,800, self.camera_group)

    def game_loop(self, screen):
         #menu variables
        game_paused = False

        run = True
        while run:

            Game.draw_window(self)
            # self.user.add(self.user)


            if game_paused == True: #options menu
                optionsMenu = OptionsMenu(screen)
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

        pygame.quit()

    
    def draw_window(self):
        self.display_surface.fill(self.bg_colour)
        # self.tiles.draw(self.screen) for identifying tiles
        map.draw_map(self.display_surface)
        self.camera_group.update()
        self.camera_group.custom_draw(self.user)
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
        self.screen.blit(pygame.transform.scale(self.ground_surf, (3200,2000)) , ground_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(pygame.transform.scale(sprite.image , (50,50)), offset_pos)
           