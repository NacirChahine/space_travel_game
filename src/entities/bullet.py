import pygame
from src.entities.entity import Entity
from src.config import *

class Bullet(Entity):
    def __init__(self, x, y, image, vx=0, vy=-10):
        super().__init__(x, y, image)
        self.vx = vx
        self.vy = vy

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.y < 0 or self.rect.x < 0 or self.rect.x > SCREEN_WIDTH:
            self.kill()
