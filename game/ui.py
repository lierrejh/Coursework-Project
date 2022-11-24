import pygame

class UI():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        font = 'assets/fonts/Fipps-Regular.otf'
        self.font = pygame.font.Font('assets/fonts/Fipps-Regular.otf', 45)
        

    def current_item_box(self,left,top):
        bg_rect = pygame.Rect(left, top, 128, 128) 
        pygame.draw.rect(self.display_surface,(32,32,32), bg_rect)

    def wave_indicator_box(self, wave):
        text_surface = self.font.render(str(int(wave)), False, (100,0,0))
        x = self.display_surface.get_size()[0] - 120
        y = self.display_surface.get_size()[1] + 10
        text_rect = text_surface.get_rect(bottomright = (x,y))
        
        #pygame.draw.rect(self.display_surface, (0,100,0), text_rect.inflate (20,20))
        self.display_surface.blit(text_surface, text_rect) 
        #pygame.draw.rect (self.display_surface, (0,100,0), text_rect.inflate (20, 20))

    def display(self, player, wave):
        self.current_item_box(40,840)
        self.wave_indicator_box(wave)