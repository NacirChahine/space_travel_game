import pygame
from src.entities.entity import Entity
from src.config import *

class Bullet(Entity):
    def __init__(self, x, y):
        # Create a simple surface for the bullet if no image is provided, 
        # but ideally we should pass an image or create one.
        # For now, let's create a surface here to match the original logic 
        # which drew a rect. Or we can use a passed image.
        # Let's assume we'll pass a surface or create one.
        image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        image.fill(WHITE)
        super().__init__(x, y, image)
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
