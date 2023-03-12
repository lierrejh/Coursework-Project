import pygame
class Entities(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

    # Provides movement to all entities
    def move(self, collision_list, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()


            #Horizontal movement
            self.position.x += self.direction.x * self.speed
            self.hitbox.centerx = round(self.position.x)
            self.rect.centerx = self.hitbox.centerx
            self.check_collisions_x(collision_list)

            
            #Vertical Movement
            self.position.y += self.direction.y * self.speed
            self.hitbox.centery = round(self.position.y)
            self.rect.centery = self.hitbox.centery
            self.check_collisions_y(collision_list)

            if self.left_facing:
                self.image = self.image_flipped
            else:
                self.image = self.image2
    
    # Hits measures collisions detected (for wall collisions and enemy collisions with player)
    def get_hits(self, collision_list):
        hits = []
        for tile in collision_list:
            if self.hitbox.colliderect(tile):
                hits.append(tile)
        return hits
    
    # Checks for collisions in the x direction
    def check_collisions_x(self, collision_list):
        collisions = self.get_hits(collision_list)
        for tile in collisions:
            if self.direction.x > 0: #Moving right
                self.hitbox.right = tile.rect.left
                self.position.x = self.rect.centerx
            elif self.direction.x < 0: #Moving left
                self.hitbox.left = tile.rect.right
                self.position.x = self.rect.centerx
            self.rect.centerx = self.hitbox.centerx
            self.position.x = self.rect.centerx

    # Checks for collisions in the y direction
    def check_collisions_y(self, collision_list):
        collisions = self.get_hits(collision_list)
        for tile in collisions:
            if self.direction.y > 0:
                self.hitbox.bottom = tile.rect.top 
            elif self.direction.y < 0:
                self.hitbox.top = tile.rect.bottom
            self.rect.centery = self.hitbox.centery
            self.position.y = self.hitbox.centery
    
    