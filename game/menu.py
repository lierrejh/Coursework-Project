from buttoncontrol import Button
import pygame
import os
import buttoncontrol
import settings

# initialise pygame and screen
pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

# create buttons for menu screens
start_button = buttoncontrol.Button(575, 15, pygame.image.load("assets/buttons/Start_Button.png").convert_alpha(), 0.8)
options_button = buttoncontrol.Button(575, 315, pygame.image.load("assets/buttons/Options_Button.png").convert_alpha(), 0.8)
quit_button = buttoncontrol.Button(575, 615, pygame.image.load("assets/buttons/Quit_Button.png").convert_alpha(), 0.8)
back_button = buttoncontrol.Button(585, 650, pygame.image.load("assets/buttons/Back_Button.png").convert_alpha(), 0.8)
keyb_button = buttoncontrol.Button(600, 415, pygame.image.load("assets/buttons/Key_Bindings.png").convert_alpha(), 0.8)
audio_button = buttoncontrol.Button(600, 215, pygame.image.load("assets/buttons/Audio_Settings.png").convert_alpha(), 0.8)
video_button = buttoncontrol.Button(600, 15, pygame.image.load("assets/buttons/Video_Settings.png").convert_alpha(), 0.8)
resume_button = buttoncontrol.Button(575, 15, pygame.image.load("assets/buttons/Resume_Button.png").convert_alpha(), 0.8)


class MainMenu:
    def __init__(self):
        self.width, self.height = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        
        self.bg = pygame.image.load("assets/mainmenu/background.jpg")
        self.screen = screen
        self.state = "main"

    def run(self):

        run = True

        while run:
            self.screen.blit(self.bg, (0, 0))

            # menu settings for initial menu
            if self.state == "main":
                if start_button.draw(self.screen):
                    # strange import location due to preventing circular imports
                    from gameloop import Game
                    game = Game(self.screen)
                    game.game_loop(self.screen)
                    del game
                if options_button.draw(self.screen):
                    self.state = "options"
                if quit_button.draw(self.screen):
                    run = False

            elif self.state == "options":
                if video_button.draw(self.screen):
                    self.state = "video_settings"
                if audio_button.draw(self.screen):
                    self.state = "audio_settings"
                if keyb_button.draw(self.screen):
                    self.state = "key_bindings"
                if back_button.draw(self.screen):
                    self.state = "main"

            elif self.state == "video_settings":
                if back_button.draw(self.screen):
                    self.state = "options"

            elif self.state == "audio_settings":
                if back_button.draw(self.screen):
                    self.state = "options"

            elif self.state == "key_bindings":
                if back_button.draw(self.screen):
                    self.state = "options"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            pygame.display.update()

        pygame.quit()


class OptionsMenu:
    def __init__(self, screen):
        self.width = settings.SCREEN_WIDTH
        self.height = settings.SCREEN_HEIGHT
        self.screen = screen
        self.state = "main"

    def run(self):

        run = True

        while run:
            bg = pygame.Surface((self.width, self.height)).convert_alpha()
            bg.fill([0, 0, 0, 0])
            self.screen.blit(bg, (0, 0))

            if self.state == "main":  # menu settings for initial menu
                if resume_button.draw(self.screen):
                    run = False
                if options_button.draw(self.screen):
                    self.state = "options"
                if quit_button.draw(self.screen):
                    mainMenu = MainMenu(self.screen)
                    mainMenu.run()

            elif self.state == "options":  # menu settings within options
                if video_button.draw(self.screen):
                    self.state = "video_settings"
                if audio_button.draw(self.screen):
                    self.state = "audio_settings"
                if keyb_button.draw(self.screen):
                    self.state = "key_bindings"
                if back_button.draw(self.screen):
                    self.state = "main"

            elif self.state == "video_settings":  # settings for graphics
                if back_button.draw(self.screen):
                    self.state = "options"

            elif self.state == "audio_settings":  # settings for audio
                if back_button.draw(self.screen):
                    self.state = "options"

            elif self.state == "key_bindings":  # settings for key bindings
                if back_button.draw(self.screen):
                    self.state = "options"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()
