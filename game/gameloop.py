import pygame
import buttoncontrol
import tilesheet

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
    
    def __init__(self):
        
        self.clock = pygame.time.Clock()
        self.bg_colour = pygame.Color('black')
        self.resumeButton = pygame.image.load("assets/buttons/Resume_Button.png").convert_alpha()

    
    def game_loop(self):
         #menu variables
        game_paused = False
        menu_state = "main"
        
        run = True
        while run:

            draw_window()

            if game_paused == True: #options menu
                if menu_state == "main": #menu settings for initial menu
                    if resume_button.draw(WIN):
                        game_paused = False
                    if options_button.draw(WIN):
                        menu_state = "options"
                    if quit_button.draw(WIN):
                        run = False
                
                elif menu_state == "options": #menu settings within options
                    if video_button.draw(WIN):
                        menu_state = "video_settings"
                    if audio_button.draw(WIN):
                        menu_state = "audio_settings"
                    if keyb_button.draw(WIN):
                        menu_state = "key_bindings"
                    if back_button.draw(WIN):
                        menu_state = "main"
                
                elif menu_state == "video_settings": #settings for graphics
                    if back_button.draw(WIN):
                        menu_state = "options"

                elif menu_state == "audio_settings": #settings for audio
                    if back_button.draw(WIN):
                        menu_state = "options"

                elif menu_state == "key_bindings": #settings for key bindings
                    if back_button.draw(WIN):
                        menu_state = "options"
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and (game_paused == True): #Unpause on escape if game is paused
                        game_paused = False
                    elif (event.key == pygame.K_ESCAPE) and (game_paused == False): #Pause on escape
                        game_paused = True
                        menu_state = "main"

                elif event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
        
        pygame.quit()
    
    def draw_window(self):
        self.screen.fill(self.bg_colour)

    def draw_text(self, text,font, text_colour, x , y):
        img = font.render(text, True, text_colour)
        self.screen.blit(img, (x,y))
