import pygame 
from settings import import_folder

class ParticleObjects:
    def __init__(self):
        self.frames = {
            # Blood
            'blood' : import_folder('assets/sprites+items/particles/blood/'),
            'fire' : import_folder('assets/sprites+items/particles/fire/'),
            'magic' : import_folder('assets/sprites+items/particles/magic/'),
            'slash' : import_folder('assets/sprites+items/particles/slash/')
        }
    
    def create_particles(self,animation_type,coords,groups):
        animation_frames = self.frames[animation_type]
        ParticleFX(coords,animation_frames,groups)

class ParticleFX(pygame.sprite.Sprite):
    def __init__(self,coords,animation,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = (coords[0],coords[1]))
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        self.animate()
