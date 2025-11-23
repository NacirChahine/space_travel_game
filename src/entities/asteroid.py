import pygame
import random
from src.entities.entity import Entity
from src.config import *

class Asteroid(Entity):
    def __init__(self, image, speed):
        x = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
        y = -ASTEROID_HEIGHT
        super().__init__(x, y, image)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
