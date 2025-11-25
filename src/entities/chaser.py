import pygame
import math
from src.entities.entity import Entity
from src.config import *

class Chaser(Entity):
    def __init__(self, x, y, image, target):
        super().__init__(x, y, image)
        self.target = target
        self.speed = CHASER_SPEED
        self.health = CHASER_HEALTH
        
    def update(self):
        # Move down
        self.rect.y += self.speed // 2
        
        # Move towards target (spaceship)
        if self.target:
            if self.rect.centerx < self.target.rect.centerx:
                self.rect.x += self.speed
            elif self.rect.centerx > self.target.rect.centerx:
                self.rect.x -= self.speed
                
        # Keep within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
    def take_damage(self, amount=1):
        self.health -= amount
        return self.health <= 0
