import pygame
from src.entities.entity import Entity
from src.config import *

class EnemyProjectile(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = BOSS_PROJECTILE_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
