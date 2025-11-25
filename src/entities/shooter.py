import pygame
from src.entities.entity import Entity
from src.entities.enemy_projectile import EnemyProjectile
from src.config import *

class Shooter(Entity):
    def __init__(self, x, y, image, projectile_image):
        super().__init__(x, y, image)
        self.projectile_image = projectile_image
        self.speed = SHOOTER_SPEED
        self.health = SHOOTER_HEALTH
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = SHOOTER_FIRE_RATE
        self.projectiles = pygame.sprite.Group()
        
    def update(self):
        # Move down slowly
        self.rect.y += self.speed
        
        # Shoot
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            self.shoot()
            self.last_shot_time = current_time
            
        self.projectiles.update()
            
    def shoot(self):
        # Shoot straight down
        projectile = EnemyProjectile(self.rect.centerx, self.rect.bottom, self.projectile_image)
        self.projectiles.add(projectile)
        
    def take_damage(self, amount=1):
        self.health -= amount
        return self.health <= 0
