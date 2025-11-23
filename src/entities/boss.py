import pygame
import random
from src.entities.entity import Entity
from src.entities.enemy_projectile import EnemyProjectile
from src.config import *

class Boss(Entity):
    def __init__(self, x, y, image, projectile_image, health):
        super().__init__(x, y, image)
        self.health = health
        self.max_health = health
        self.projectile_image = projectile_image
        self.speed = 2
        self.direction = 1 # 1 for right, -1 for left
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = 1500 # ms
        self.projectiles = pygame.sprite.Group()

    def update(self):
        # Movement
        self.rect.x += self.speed * self.direction
        
        # Bounce off walls
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1
            
        # Shooting
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            self.shoot()
            self.last_shot_time = current_time
            
        self.projectiles.update()

    def shoot(self):
        # Shoot from two points
        p1 = EnemyProjectile(self.rect.left + 10, self.rect.centery, self.projectile_image)
        p2 = EnemyProjectile(self.rect.right - 20, self.rect.centery, self.projectile_image)
        self.projectiles.add(p1)
        self.projectiles.add(p2)

    def take_damage(self, amount=1):
        self.health -= amount
        return self.health <= 0
