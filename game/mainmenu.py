from buttoncontrol import Button
import pygame
import os
from gameloop import Game
import buttoncontrol

startButton = pygame.image.load("assets/buttons/Start_Button.png").convert_alpha()
videoSettings = pygame.image.load("assets/buttons/Video_Settings.png").convert_alpha()
backButton = pygame.image.load("assets/buttons/Back_Button.png").convert_alpha()
keyBindings = pygame.image.load("assets/buttons/Key_Bindings.png").convert_alpha()
audioSettings = pygame.image.load("assets/buttons/Audio_Settings.png").convert_alpha()
quitButton = pygame.image.load("assets/buttons/Quit_Button.png").convert_alpha()
optionsButton = pygame.image.load("assets/buttons/Options_Button.png").convert_alpha()

start_button = (buttoncontrol.Button(575, 15, startButton, 0.8))
options_button = buttoncontrol.Button(575, 315, optionsButton, 0.8)
quit_button = buttoncontrol.Button(575, 615, quitButton , 0.8)
back_button = buttoncontrol.Button(585, 650, backButton, 0.8)
keyb_button = buttoncontrol.Button(600, 415, keyBindings, 0.8)
audio_button = buttoncontrol.Button(600, 215, audioSettings, 0.8)
video_button = buttoncontrol.Button(600, 15, videoSettings, 0.8)



class MainMenu:
    def __init__(self, screen):
        self.width = 1600
        self.height = 1000
        self.bg = pygame.image.load("assets/mainmenu/background.jpg")
        self.screen = screen
        


    # def draw(self):
    #     self.screen.blit(self.bg, (0,0))
    #     self.screen.blit(buttoncontrol.Button(575, 15, startButton, 0.8))
    #     self.options_button = buttoncontrol.Button(575, 315, optionsButton, 0.8)
    #     self.quit_button = buttoncontrol.Button(575, 615, quitButton , 0.8)
    #     self.back_button = buttoncontrol.Button(585, 650, backButton, 0.8)
    #     self.keyb_button = buttoncontrol.Button(600, 415, keyBindings, 0.8)
    #     self.audio_button = buttoncontrol.Button(600, 215, audioSettings, 0.8)
    #     self.video_button = buttoncontrol.Button(600, 15, videoSettings, 0.8)
    #     pygame.display.update()

    
    def run(self):
            menu_state = "main"
            
            run = True
            
            while run:
                self.screen.blit(self.bg, (0,0))

                if menu_state == "main": #menu settings for initial menu
                    if start_button.draw(self.screen):
                        game = Game(self.screen)
                        game.run()
                        del game
                    if options_button.draw(self.screen):
                        menu_state = "options"
                    if quit_button.draw(self.screen):
                        run = False
                
                elif menu_state == "options": #menu settings within options
                    if video_button.draw(self.screen):
                        menu_state = "video_settings"
                    if audio_button.draw(self.screen):
                        menu_state = "audio_settings"
                    if keyb_button.draw(self.screen):
                        menu_state = "key_bindings"
                    if back_button.draw(self.screen):
                        menu_state = "main"
                
                elif menu_state == "video_settings": #settings for graphics
                    if back_button.draw(self.screen):
                        menu_state = "options"

                elif menu_state == "audio_settings": #settings for audio
                    if back_button.draw(self.screen):
                        menu_state = "options"

                elif menu_state == "key_bindings": #settings for key bindings
                    if back_button.draw(self.screen):
                        menu_state = "options"
               
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                pygame.display.update()
            
            pygame.quit()   
        
