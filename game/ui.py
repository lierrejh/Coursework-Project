import pygame

class UI:
    def __init__(self, ):
        self.display_surface = pygame.display.get_surface()
        self.health_bar_rect = pygame.Rect(10, 10, 200, 100)

    def display(self, player):
        pygame.draw.rect(self.display_surface, (255,255,255), self.health_bar_rect)
        