import pygame
import settings
import time

class UI():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/Fipps-Regular.otf', 48)
        self.font_enlarged = pygame.font.Font('assets/fonts/Fipps-Regular.otf', 80)
        self.game_over = pygame.image.load("assets/mainmenu/game_over.jpg").convert_alpha()


        #Weapon Images
        self.weapon_images = []
        for weapon in settings.WEAPON_DATA.values():
            path = weapon['image']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_images.append(weapon)
        self.item_images = []
        for item in settings.ITEM_DATA.values():
            path = item['image']
            item = pygame.image.load(path).convert_alpha()
            self.item_images.append(item)

    def current_item_box(self,left,top, size):
        if size == 0:
            bg_rect = pygame.Rect(left, top, 128, 128) 
        elif size > 0:
            bg_rect = pygame.Rect(left, top, size, size)
        pygame.draw.rect(self.display_surface,(32,32,32), bg_rect)
        pygame.draw.rect(self.display_surface,(100,0,0), bg_rect,3)
        return bg_rect

    def wave_indicator_box(self, wave):
        text_surface = self.font.render(str(int(wave)), False, (100,0,0))
        #x = self.display_surface.get_size()[0] - 120 #Bottom right
        #y = self.display_surface.get_size()[1] + 10 #
        x = self.display_surface.get_size()[0] - 120 #Top right
        y = 120
        text_rect = text_surface.get_rect(bottomright = (x,y))
        
        #pygame.draw.rect(self.display_surface, (0,100,0), text_rect.inflate (20,20))
        self.display_surface.blit(text_surface, text_rect) 
        #pygame.draw.rect (self.display_surface, (0,100,0), text_rect.inflate (20, 20))

    def weapon_overlay(self, weapon_index):
        bg_rect = self.current_item_box(40,840, 0)
        weapon_surface = pygame.transform.scale(self.weapon_images[weapon_index], (80,160))
        weapon_rect = weapon_surface.get_rect(center = bg_rect.center)
        
        self.display_surface.blit(weapon_surface, weapon_rect)

    def item_overlay(self, item_index):
        bg_rect = self.current_item_box(170,845,64)
        item_surface = pygame.transform.scale(self.item_images[item_index], (56,56))
        item_rect = item_surface.get_rect(center = bg_rect.center)
        
        self.display_surface.blit(item_surface, item_rect)

    def game_over_screen(self):
        self.display_surface.blit(self.game_over, (0,0))
        
        text_surface = self.font_enlarged.render("Game over", False, (100,0,0))
        if settings.enemies_killed == 1:
            x = 'enemy'
        else:
            x = 'enemies'
        text_surface2 = self.font.render(f'You have killed {settings.enemies_killed} {x}', False, (100,0,0))
        x = 1000 #Top right
        y = 600
        text_rect = text_surface.get_rect(bottomright = (x + 150,y))
        text_rect2 = text_surface2.get_rect(bottomright = (x+300,y+300))


        self.display_surface.blit(text_surface, text_rect)
        self.display_surface.blit(text_surface2, text_rect2)  
        pygame.display.flip()
        time.sleep(5)

    # Change to convert into cooldown bar - call within cooldown function in player and 
    # pass in parameters from there (only appears when cooldown is needed)
    '''def cooldown_bar(self):
        self.current_cooldown = 1000
        self.maximum_cooldown = 1000
        self.cooldown_bar_length = 400
        self.cooldown_ratio = self.maximum_cooldown / self.cooldown_bar_length
        self.target_cooldown = 1000
        self.cooldown_change_speed = 5

        transition_width = 0
        transition_color = (0,250,0)

        if self.current_cooldown > self.target_cooldown:
            self.current_cooldown -= self.health_change_speed
            transition_width = int((self.target_cooldown - self.current_cooldown) /self.cooldown_ratio)
            transition_color = (0, 0, 255)   

        cooldown_bar_rect = pygame.Rect(50, 85, 400, 25)
        transition_bar_rect = pygame.Rect(cooldown_bar_rect.right, 45, transition_width, 25)

        pygame.draw.rect(self.display_surface, (0, 0, 100) , cooldown_bar_rect)
        pygame.draw.rect(self.display_surface, transition_color, transition_bar_rect)
        pygame.draw.rect(self.display_surface,(255, 255, 255),(50, 85, 400, 25),4)'''

    def display(self, player, wave):
        self.weapon_overlay(player.weapon_index) #Current weapon
        self.item_overlay(player.item_index) #health/healing item
        self.wave_indicator_box(wave)