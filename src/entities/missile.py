import pygame
from src.entities.entity import Entity
from src.config import *

class Missile(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.target_y = SCREEN_HEIGHT // 2
        self.speed = 12
        self.exploded = False
        self.trail_timer = 0

    def update(self):
        # Move towards center
        if self.rect.centery > self.target_y:
            self.rect.y -= self.speed
        else:
            self.exploded = True
