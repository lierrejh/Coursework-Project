import pygame
import buttoncontrol
from menu import OptionsMenu
from tilesheet import Tilesheet
from player import Player
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
        self.player = Player(self,800,500)


    
    def game_loop(self, screen):
         #menu variables
        game_paused = False
        
        run = True
        while run:
            
            Game.draw_window(self)

            if game_paused == True: #options menu
                optionsMenu = OptionsMenu(screen)
                optionsMenu.run()                
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and (game_paused == True): #Unpause on escape if game is paused
                        game_paused = False
                    elif (event.key == pygame.K_ESCAPE) and (game_paused == False): #Pause on escape
                        game_paused = True
                    if event.key == pygame.K_a:
                        self.player.left_pressed = True
                    if event.key == pygame.K_d:
                        self.player.right_pressed = True
                    if event.key == pygame.K_w:
                        self.player.up_pressed = True
                    if event.key == pygame.K_s:
                        self.player.down_pressed = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.left_pressed = False
                    if event.key == pygame.K_d:
                        self.player.right_pressed = False
                    if event.key == pygame.K_w:
                        self.player.up_pressed = False
                    if event.key == pygame.K_s:
                        self.player.down_pressed = False

                elif event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
        
        pygame.quit()
    
    def draw_window(self):
        self.screen.fill(self.bg_colour)
        self.player.update()
        pygame.display.flip()
        # bigger_player = pygame.transform.scale(player, (64,64))
        # self.screen.blit(bigger_player, [400,400])
        # self.tiles.draw(self.screen)

    def draw_text(self, text,font, text_colour, x , y):
        img = font.render(text, True, text_colour)
        self.screen.blit(img, (x,y))
