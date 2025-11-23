import pygame
import random
from src.entities.entity import Entity
from src.config import *

class PowerUp(Entity):
    def __init__(self, image, type):
        x = random.randint(0, SCREEN_WIDTH - POWERUP_WIDTH)
        y = -POWERUP_HEIGHT
        super().__init__(x, y, image)
        self.type = type
        self.speed = POWERUP_SPEED

    def update(self):
        self.rect.y += self.speed
