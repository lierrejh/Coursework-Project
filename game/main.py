import pygame


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 1000))

    # Surely this import statement should be at the top?
    # I'd get an autoformatter set up, either "black" or "autopep8"
    from menu import MainMenu

    # Should be using snake case for variables, main_menu
    mainMenu = MainMenu(screen)
    mainMenu.run()