import pygame
import settings

class UI():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/Fipps-Regular.otf', 45)

        #Weapon Images
        self.weapon_images = []
        for weapon in settings.WEAPON_DATA.values():
            path = weapon['image']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_images.append(weapon)

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
        weapon_surface = pygame.transform.scale(self.weapon_images[weapon_index], (64,128))
        weapon_rect = weapon_surface.get_rect(center = bg_rect.center)
        
        self.display_surface.blit(weapon_surface, weapon_rect)

    def display(self, player, wave):
        self.weapon_overlay(player.weapon_index) #Current weapon
        self.current_item_box(170,845,64) #Current health/healing item
        self.wave_indicator_box(wave)