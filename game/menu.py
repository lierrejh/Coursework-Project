# Finish settings

from buttoncontrol import Button
import pygame
import os
import buttoncontrol
import settings
from roomgeneration import room_generation, get_player_spawn
import random

# initialise pygame and screen
pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

# create buttons for menu screens
start_button = buttoncontrol.Button(575, 415, pygame.image.load("assets/buttons/Start_Button.png").convert_alpha(), 0.8)
options_button = buttoncontrol.Button(565, 615, pygame.image.load("assets/buttons/Options_Button.png").convert_alpha(), 0.8)
quit_button = buttoncontrol.Button(575, 815, pygame.image.load("assets/buttons/Quit_Button.png").convert_alpha(), 0.8)
tutorial_button = buttoncontrol.Button(570, 280, pygame.image.load("assets/buttons/Tutorial_Button.png").convert_alpha(), 0.8)

back_button = buttoncontrol.Button(575, 815, pygame.image.load("assets/buttons/Back_Button.png").convert_alpha(), 0.8)
audio_button = buttoncontrol.Button(575, 615, pygame.image.load("assets/buttons/Audio_Settings.png").convert_alpha(), 0.8)
video_button = buttoncontrol.Button(575, 415, pygame.image.load("assets/buttons/Video_Settings.png").convert_alpha(), 0.8)
resume_button = buttoncontrol.Button(575, 415, pygame.image.load("assets/buttons/Resume_Button.png").convert_alpha(), 0.8)

tutorial_image = pygame.image.load("assets/mainmenu/tutorial.png").convert_alpha()

volume_100 = buttoncontrol.Button(575, 215, pygame.image.load("assets/buttons/Volume_100%.png").convert_alpha(), 0.8)
volume_50 = buttoncontrol.Button(575, 415, pygame.image.load("assets/buttons/Volume_50%.png").convert_alpha(), 0.8)
volume_0 = buttoncontrol.Button(575, 615, pygame.image.load("assets/buttons/Volume_0%.png").convert_alpha(), 0.8)

class MainMenu:
    # Class for the main menu
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
                # If the start button is clicked, start the game
                if start_button.draw(self.screen):
                    # Restoring all values to default in order to prevent 
                    # old values from affecting new game
                    room_center_points = None
                    spawn_point = None
                    room_center_points = room_generation()
                    spawn_point = get_player_spawn(room_center_points)
                    room_center_points.remove(spawn_point)
                    settings.waves_completed = 0
                    settings.enemies_killed = 0
                    settings.level_count = 1
                    settings.player_weapons = ['wooden-sword']
                    settings.player_items = ['small-health-potion']
                    settings.player_powerups = []
                    settings.player_stats = {
                    'damage_multiplier' : 1,
                    'defense' : 1,
                    'health_multiplier' : 1,
                    'speed' : 8,
                    }
                    
                    # preventing circular imports
                    from gameloop import Game
                    game = Game(self.screen, spawn_point, room_center_points, 0, 0, 1)
                    game.game_loop(self.screen)
                    del game

                # If the options button is clicked, change the state to options (options screen)
                if options_button.draw(self.screen):
                    self.state = "options"
                # If the quit button is clicked, quit the game
                if quit_button.draw(self.screen):
                    run = False
                # If the tutorial button is clicked, change the state to tutorial (tutorial screen)
                if tutorial_button.draw(self.screen):
                    self.state = "tutorial"

            # Options menu allows the user to click on the audio settings button to change the volume
            # or the back button to return to the main menu
            elif self.state == "options":
                if audio_button.draw(self.screen):
                    self.state = "audio_settings"
                if back_button.draw(self.screen):
                    self.state = "main"

            # Tutorial menu shows the user how to play and allows user to return back to the menu
            elif self.state == "tutorial":
                self.screen.blit((pygame.transform.scale((tutorial_image), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))), (0, 0))
                if back_button.draw(self.screen):
                    self.state = "main"

            # Audio settings menu allows the user to change the volume of the game
            elif self.state == "audio_settings":
                # If the volume 100% button is clicked, set the volume to 100%
                if volume_100.draw(self.screen):
                    pygame.mixer.music.set_volume(1)
                
                # If the volume 50% button is clicked, set the volume to 50%
                if volume_50.draw(self.screen):
                    pygame.mixer.music.set_volume(0.5)

                # If the volume 0% button is clicked, mute the volume
                if volume_0.draw(self.screen):
                    pygame.mixer.music.set_volume(0)
                
                # If the back button is clicked, return to the options menu
                if back_button.draw(self.screen):
                    self.state = "options"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            pygame.display.update()

        pygame.quit()


class OptionsMenu:
    # Class for the options menu which can only be reached when pressing escape from within 
    # a running game playthrough
    def __init__(self, screen):
        self.width = settings.SCREEN_WIDTH
        self.height = settings.SCREEN_HEIGHT
        self.screen = screen
        self.state = "main"

    def run(self):

        run = True

        while run:
            bg = pygame.Surface((self.width, self.height))
            bg.fill([0, 0, 0])
            self.screen.blit(bg, (0, 0))

            if self.state == "main":  # menu settings for initial menu
                if resume_button.draw(self.screen):
                    run = False
                if options_button.draw(self.screen):
                    self.state = "options"
                if quit_button.draw(self.screen):
                    main_menu = MainMenu(self.screen)
                    main_menu.run()

            elif self.state == "options":  # menu settings within options
                if audio_button.draw(self.screen):
                    self.state = "audio_settings"
                if back_button.draw(self.screen):
                    self.state = "main"

            elif self.state == "audio_settings":
                if volume_100.draw(self.screen):
                    pygame.mixer.music.set_volume(1)
                if volume_50.draw(self.screen):
                    pygame.mixer.music.set_volume(0.5)
                if volume_0.draw(self.screen):
                    pygame.mixer.music.set_volume(0)
                if back_button.draw(self.screen):
                    self.state = "options"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()
