import pygame 
from tilesheet import Tilesheet
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x , y, group):#, groups):#, groups)
        super().__init__(group)
        self.game = game
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 2
        self.screen = pygame.display.set_mode((1600, 1000))
        self.image = pygame.image.load('assets/sprites+items/individual_sprites/StartingCharacter.png').convert_alpha()
        self.rect = self.image.get_rect(center = (x, y))
        self.direction = pygame.math.Vector2()
 
        # self.tiles = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)
        self.user = pygame.image.load('assets/sprites+items/individual_sprites/StartingCharacter.png').convert_alpha()
        self.left_facing = False

    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
    

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed            
        
        
        '''if self.left_facing == False:
            self.screen.blit(self.user, (int(self.x), int(self.y)))
        else:
            flipped_user = pygame.transform.flip(self.user, True, False)    
            self.screen.blit(flipped_user, (int(self.x), int(self.y)))  '''

