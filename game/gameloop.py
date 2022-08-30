import pygame
import buttoncontrol
from menu import OptionsMenu
from tilesheet import Tilesheet
pygame.font.init()
pygame.init()


#provide fonts & colour for the text
font = pygame.font.SysFont("arialblack", 40)
TEXT_COLOUR = (255,255,255)

#create button image
# resume_button = buttoncontrol.Button(575, 15, resume_img, 0.8)
# options_button = buttoncontrol.Button(575, 315, options_img, 0.8)
# quit_button = buttoncontrol.Button(575, 615, quit_img, 0.8)
# back_button = buttoncontrol.Button(585, 650, back_img, 0.8)
# keyb_button = buttoncontrol.Button(600, 415, keyb_img, 0.8)
# audio_button = buttoncontrol.Button(600, 215, audio_img, 0.8)
# video_button = buttoncontrol.Button(600, 15, video_img, 0.8)
# start_button = buttoncontrol.Button(575, 15, start_img, 0.8)

class Game:
    
    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.bg_colour = pygame.Color('black')
        self.resumeButton = pygame.image.load("assets/buttons/Resume_Button.png").convert_alpha()
        self.tiles = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.screen = screen

    
    def game_loop(self, screen):
         #menu variables
        game_paused = False
        
        run = True
        while run:
            
            screen.fill((0,0,0))

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
        self.screen.fill(self.bg_colour)
        self.screen.blit(self.tiles.get_tile(5, 2) (400, 400))

    def draw_text(self, text,font, text_colour, x , y):
        img = font.render(text, True, text_colour)
        self.screen.blit(img, (x,y))
