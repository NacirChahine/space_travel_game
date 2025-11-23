import pygame
import random
from src.entities.entity import Entity
from src.entities.enemy_projectile import EnemyProjectile
from src.config import *

class Boss(Entity):
    def __init__(self, x, y, image, projectile_image, difficulty_tier='MEDIUM'):
        super().__init__(x, y, image)
        
        # Store difficulty tier and get its properties
        self.difficulty_tier = difficulty_tier
        tier_config = BOSS_DIFFICULTY_TIERS.get(difficulty_tier, BOSS_DIFFICULTY_TIERS['MEDIUM'])
        
        # Set health based on difficulty tier
        health_min, health_max = tier_config['health_range']
        self.health = random.randint(health_min, health_max)
        self.max_health = self.health
        
        # Set projectile count based on difficulty tier
        self.projectile_count = tier_config['projectile_count']
        
        # Visual indicators based on difficulty
        self.color = tier_config['color']
        self.border_color = tier_config['border_color']
        
        self.projectile_image = projectile_image
        self.speed = 2
        self.direction = 1 # 1 for right, -1 for left
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = 1500 # ms
        self.projectiles = pygame.sprite.Group()
        
        # Create colored version of the boss image
        self.original_image = image.copy()
        self.apply_color_overlay()

    def apply_color_overlay(self):
        """Apply color overlay to the boss image based on difficulty"""
        # Create a colored surface
        colored_surface = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)
        colored_surface.fill((*self.color, 100))  # Semi-transparent color overlay
        
        # Create the final image with overlay
        self.image = self.original_image.copy()
        self.image.blit(colored_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Add colored border
        border_width = 3
        pygame.draw.rect(self.image, self.border_color, self.image.get_rect(), border_width)

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
        """Shoot projectiles based on difficulty tier"""
        # Calculate positions for multiple projectiles
        boss_width = self.rect.width
        projectile_spacing = boss_width / (self.projectile_count + 1)
        
        for i in range(self.projectile_count):
            x_pos = self.rect.left + projectile_spacing * (i + 1)
            y_pos = self.rect.centery
            projectile = EnemyProjectile(x_pos, y_pos, self.projectile_image)
            self.projectiles.add(projectile)

    def take_damage(self, amount=1):
        self.health -= amount
        return self.health <= 0
