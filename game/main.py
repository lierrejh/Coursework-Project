import pygame


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 1000))
    from menu import MainMenu
    mainMenu = MainMenu(screen)
    mainMenu.run()