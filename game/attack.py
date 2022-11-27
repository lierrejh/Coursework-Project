import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)
        direction = player.direction
        print(direction)

        # image
        path = f"assets/sprites+items/weapons/{player.weapon}.png"
        self.image = pygame.image.load(path).convert_alpha()

        # placement
        if direction == (-1,-1):
            self.rect = self.image.get_rect(midright = player.hitbox.midleft + pygame.math.Vector2(-20, -12))
        elif (direction == (0,1)): # down
            self.rect = self.image.get_rect(midtop = player.hitbox.midbottom + pygame.math.Vector2(-6, -6))
        elif (direction == (0,-1)): # up
            self.rect = self.image.get_rect(midbottom = player.hitbox.midtop + pygame.math.Vector2(-6, -12))
        elif (direction == (1,0)): # right
            self.rect = self.image.get_rect(midleft = player.hitbox.midright + pygame.math.Vector2(5, -12))
        elif (direction == (-1,0)): # left
            self.rect = self.image.get_rect(midright = player.hitbox.midleft + pygame.math.Vector2(-20, -12))
        elif (direction == (0,0)) & player.left_facing == True:
            self.rect = self.image.get_rect(midright = player.hitbox.midleft + pygame.math.Vector2(-20, -12))
        elif (direction == (0,0)) & player.left_facing == False:
            self.rect = self.image.get_rect(midleft = player.hitbox.midright + pygame.math.Vector2(5, -12))

    