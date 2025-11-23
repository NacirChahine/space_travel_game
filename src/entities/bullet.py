import pygame
from src.entities.entity import Entity
from src.config import *

class Bullet(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = 10  # Increased speed for better feel

        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
