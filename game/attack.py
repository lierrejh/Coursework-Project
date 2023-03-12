import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)
        direction = player.direction

        # image
        path = f"assets/sprites+items/weapons/{player.weapon}.png"
        self.image = pygame.image.load(path).convert_alpha()

        # placement
        if direction == (-1,-1):
            self.rect = self.image.get_rect(midright = player.hitbox.midleft + pygame.math.Vector2(-20, -12))
        elif direction == (-1,1):
            self.rect = self.image.get_rect(midright = player.hitbox.midleft + pygame.math.Vector2(-20, -12))
        
        # down    
        elif (direction == (0,1)): 
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(midtop = player.hitbox.midbottom + pygame.math.Vector2(-6, -1))
        
        # up    
        elif (direction == (0,-1)): 
            self.rect = self.image.get_rect(midbottom = player.hitbox.midtop + pygame.math.Vector2(-6, -12))
        
        # right    
        elif (direction == (1,0)): 
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect(midleft = player.hitbox.midright + pygame.math.Vector2(-3, -12))
        
        # left
        elif (direction == (-1,0)): 
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect(midright = player.hitbox.midleft + pygame.math.Vector2(10, -12))
        
        # not moving and facing left
        elif (direction == (0,0)) & player.left_facing == True: 
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect(midright = player.hitbox.midleft + pygame.math.Vector2(15, -12))
        
        # not moving and facing right
        elif (direction == (0,0)) & player.left_facing == False: 
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect(midleft = player.hitbox.midright + pygame.math.Vector2(-10, -12))

    