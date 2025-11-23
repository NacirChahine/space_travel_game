import pygame
from src.entities.entity import Entity
from src.config import *

class Spaceship(Entity):
    def __init__(self, x, y, image, sound):
        super().__init__(x, y, image)
        self.speed = 5
        self.fire_sound = sound
        self.bullets = pygame.sprite.Group()
        self.available_bullets = INITIAL_BULLETS

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep within screen bounds
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - SPACESHIP_WIDTH:
            self.rect.x = SCREEN_WIDTH - SPACESHIP_WIDTH

    def shoot(self, bullet_image):
        if self.available_bullets > 0:
            self.fire_sound.play()
            # Create bullet centered on spaceship
            bullet_x = self.rect.x + SPACESHIP_WIDTH // 2 - BULLET_WIDTH // 2
            bullet_y = self.rect.y
            return bullet_x, bullet_y
        return None, None

    def add_bullets(self, amount):
        self.available_bullets = min(MAX_BULLETS, self.available_bullets + amount)

    def decrease_bullets(self):
        self.available_bullets -= 1
