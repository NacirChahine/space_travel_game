import pygame
from src.entities.entity import Entity

class Explosion(Entity):
    def __init__(self, x, y, images):
        # Start with the first frame
        super().__init__(x, y, images[0])
        self.images = images
        self.frame_index = 0
        self.animation_speed = 0.5 # Frames per update tick (adjust as needed)
        self.current_frame = 0
        
        # Center the explosion
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.images):
            self.kill()
        else:
            self.image = self.images[int(self.current_frame)]
            # Keep centered
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
