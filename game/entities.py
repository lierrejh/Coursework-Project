import pygame

class Entities(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

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

    def get_hits(self, collision_list):
        hits = []
        for tile in collision_list:
            if self.hitbox.colliderect(tile):
                hits.append(tile)
        return hits
    
    def check_collisions_x(self, collision_list):
        collisions = self.get_hits(collision_list)
        for tile in collisions:
            print("coll")
            if self.direction.x > 0: #Moving right
                self.hitbox.right = tile.rect.left
                self.position.x = self.rect.centerx
            elif self.direction.x < 0: #Moving left
                self.hitbox.left = tile.rect.right
                self.position.x = self.rect.centerx
            self.rect.centerx = self.hitbox.centerx
            self.position.x = self.rect.centerx

    def check_collisions_y(self, collision_list):
        collisions = self.get_hits(collision_list)
        for tile in collisions:
            if self.direction.y > 0:
                self.hitbox.bottom = tile.rect.top 
            elif self.direction.y < 0:
                self.hitbox.top = tile.rect.bottom
            self.rect.centery = self.hitbox.centery
            self.position.y = self.hitbox.centery
    
    # def motion(self,speed):
    #     if self.direction.magnitude() != 0:
    #         self.direction = self.direction.normalize()

    #     self.hitbox.x += self.direction.x * speed
    #     self.check_collisions_x(self.collision_list)
    #     self.hitbox.y += self.direction.y * speed
    #     self.check_collisions_y(self.collision_list)
    #     self.rect.center = self.hitbox.center
        
    # def collision(self,direction):
    #     if direction == 'horizontal':
    #         for sprite in self.obstacle_sprites:
    #             if sprite.hitbox.colliderect(self.hitbox):
    #                 if self.direction.x > 0: # moving right
    #                     self.hitbox.right = sprite.hitbox.left
    #                 if self.direction.x < 0: # moving left
    #                     self.hitbox.left = sprite.hitbox.right

    #     if direction == 'vertical':
    #         for sprite in self.obstacle_sprites:
    #             if sprite.hitbox.colliderect(self.hitbox):
    #                 if self.direction.y > 0: # moving down
    #                     self.hitbox.bottom = sprite.hitbox.top
    #                 if self.direction.y < 0: # moving up
    #                     self.hitbox.top = sprite.hitbox.bottom