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
        self.level = 1
        self.asset_manager = None # Will be set by GameScene or passed in init if refactored. 
        # Actually, better to pass assets dict or manager. 
        # Current init takes 'image' and 'sound'. 
        # I'll need access to other level images.
        # Let's assume we can pass the assets dictionary or handle image updates from outside?
        # Or better, pass the assets dictionary to __init__ instead of single image.
        # But to avoid breaking existing calls too much, I'll add a set_assets method or just update image from outside.
        # Wait, GameScene creates Spaceship. I can pass assets there.
        
    def set_assets(self, assets):
        self.assets = assets
        self.update_image()

    def update_image(self):
        if hasattr(self, 'assets'):
            self.image = self.assets['spaceship_levels'][self.level]
            # Update rect but keep center
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center

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
            
            # Determine bullet image based on level
            b_img = self.assets['bullet_levels'][self.level] if hasattr(self, 'assets') else bullet_image
            
            bullets = []
            
            if self.level == 1:
                # Single shot
                bx = self.rect.centerx - BULLET_WIDTH // 2
                by = self.rect.y
                bullets.append((bx, by, b_img))
            elif self.level == 2:
                # Double shot
                bx1 = self.rect.centerx - 10 - BULLET_WIDTH // 2
                bx2 = self.rect.centerx + 10 - BULLET_WIDTH // 2
                by = self.rect.y
                bullets.append((bx1, by, b_img))
                bullets.append((bx2, by, b_img))
            elif self.level == 3:
                # Triple shot
                bx1 = self.rect.centerx - 15 - BULLET_WIDTH // 2
                bx2 = self.rect.centerx + 15 - BULLET_WIDTH // 2
                bx3 = self.rect.centerx - BULLET_WIDTH // 2
                by = self.rect.y
                bullets.append((bx1, by, b_img))
                bullets.append((bx2, by, b_img))
                bullets.append((bx3, by - 5, b_img)) # Center one slightly forward

            return bullets
        return []

    def upgrade(self):
        if self.level < SPACESHIP_LEVEL_MAX:
            self.level += 1
            self.update_image()

    def downgrade(self):
        if self.level > 1:
            self.level -= 1
            self.update_image()

    def add_bullets(self, amount):
        self.available_bullets = min(MAX_BULLETS, self.available_bullets + amount)

    def decrease_bullets(self):
        self.available_bullets -= 1
