import pygame
import settings
import time

class UI():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font_minimised = pygame.font.Font('assets/fonts/Fipps-Regular.otf', 30)
        self.font = pygame.font.Font('assets/fonts/Fipps-Regular.otf', 48)
        self.font_enlarged = pygame.font.Font('assets/fonts/Fipps-Regular.otf', 80)
        self.game_over = pygame.image.load("assets/mainmenu/game_over.jpg").convert_alpha()

        # Weapon Images
        self.weapon_images = []
        for weapon in settings.WEAPON_DATA.values():
            path = weapon['image']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_images.append(weapon)
       
        
        # Item images 
        self.item_images = []
        for item in settings.ITEM_DATA.values():
            path = item['image']
            item = pygame.image.load(path).convert_alpha()
            self.item_images.append(item)
        
        # Power up images
        self.power_up_images = []
        for item in settings.POWER_UP_DATA.values():
            path = item['image']
            item = pygame.image.load(path).convert_alpha()
            self.power_up_images.append(item)

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
        x = self.display_surface.get_size()[0] - 120 #Top right
        y = 120
        text_rect = text_surface.get_rect(bottomright = (x,y))
        
        self.display_surface.blit(text_surface, text_rect) 

    def enemies_left_box(self, enemy_count, enemies_killed):
        text_surface = self.font_minimised.render(f'Enemies left {enemy_count - enemies_killed}', False, (100,0,0))
        x = self.display_surface.get_size()[0] - 120 #Top right
        y = 180
        text_rect = text_surface.get_rect(bottomright = (x,y))
        
        #pygame.draw.rect(self.display_surface, (0,100,0), text_rect.inflate (20,20))
        self.display_surface.blit(text_surface, text_rect) 

    def weapon_overlay(self, weapon):
        bg_rect = self.current_item_box(40,840, 0)
        weapon_surface = pygame.transform.scale(self.weapon_images[settings.WEAPON_DATA[weapon]['index']], (80,160))
        weapon_rect = weapon_surface.get_rect(center = bg_rect.center)
        
        self.display_surface.blit(weapon_surface, weapon_rect)

    def item_overlay(self, item):
        bg_rect = self.current_item_box(170,845,64)
        item_surface = pygame.transform.scale(self.item_images[settings.ITEM_DATA[item]['index']], (56,56))
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
    
    def display(self, player, wave, enemy_count, enemies_killed):
        self.weapon_overlay(player.weapon) #Current weapon
        self.item_overlay(player.item) #health/healing item
        self.wave_indicator_box(wave)
        self.enemies_left_box(enemy_count, enemies_killed)

    def next_round_indicator(self):
        text_surface = self.font_minimised.render(f'New wave commencing shortly', False, (255,255,255))
        x = self.display_surface.get_size()[0] / 2#Top right
        y = 400
        text_rect = text_surface.get_rect(bottomright = (x,y))
        
        self.display_surface.blit(text_surface, text_rect)

    def boss_round_indicator(self):
        text_surface = self.font_minimised.render(f'Boss wave incoming', False, (255,255,255))
        x = self.display_surface.get_size()[0] / 2
        y = 400
        text_rect = text_surface.get_rect(bottomright = (x,y))
        
        self.display_surface.blit(text_surface, text_rect) 

    def power_up_box(self, power_up):
        bg_rect = self.current_item_box(40,100, 64)
        power_surface = pygame.transform.scale(self.power_up_images[settings.POWER_UP_DATA[power_up]['index']], (64,64))
        power_rect = power_surface.get_rect(center = bg_rect.center)
        self.display_surface.blit(power_surface, power_rect)
    
    def item_loot_box(self, item):
        bg_rect = self.current_item_box(120,100, 64)
        item_surface = pygame.transform.scale(self.item_images[int(settings.ITEM_DATA[item]['index'])], (64,64))
        item_rect = item_surface.get_rect(center = bg_rect.center)
        self.display_surface.blit(item_surface, item_rect)