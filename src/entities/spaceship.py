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
        self.missiles = INITIAL_MISSILES
        self.level = 1
        self.asset_manager = None
        
        # Invincibility mechanic
        self.is_invincible = False
        self.invincibility_start_time = 0
        self.invincibility_duration = 2000  # 2 seconds in milliseconds
        self.blink_interval = 100  # Blink every 100ms
        self.visible = True  # For blinking effect 
        
    def set_assets(self, assets):
        self.assets = assets
        self.update_image()

    def update_image(self):
        if hasattr(self, 'assets'):
            # Ensure level doesn't exceed available images if they aren't defined for 4/5 yet
            # Assuming assets['spaceship_levels'] has enough images or we reuse max level image
            # For now, let's clamp the index to the max available in assets if needed, 
            # but ideally assets should be updated. 
            # If assets only has 3 levels, we reuse level 3 image for 4 and 5.
            lvl_idx = min(self.level, len(self.assets['spaceship_levels']))
            self.image = self.assets['spaceship_levels'][lvl_idx]
            
            # Update rect but keep center
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Vertical movement (NEW)
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep within screen bounds (horizontal)
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - SPACESHIP_WIDTH:
            self.rect.x = SCREEN_WIDTH - SPACESHIP_WIDTH
        
        # Keep within screen bounds (vertical)
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > SCREEN_HEIGHT - SPACESHIP_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - SPACESHIP_HEIGHT
        
        # Handle invincibility timer and blinking
        if self.is_invincible:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.invincibility_start_time
            
            # Check if invincibility period has expired
            if elapsed >= self.invincibility_duration:
                self.is_invincible = False
                self.visible = True  # Ensure spaceship is visible after invincibility
            else:
                # Toggle visibility for blinking effect
                blink_cycle = (elapsed // self.blink_interval) % 2
                self.visible = (blink_cycle == 0)

    def shoot(self, bullet_image):
        if self.available_bullets > 0:
            self.fire_sound.play()
            
            # Determine bullet image based on level
            # Reuse level 3 bullet image for higher levels if needed
            b_lvl_idx = min(self.level, len(self.assets['bullet_levels']))
            b_img = self.assets['bullet_levels'][b_lvl_idx] if hasattr(self, 'assets') else bullet_image
            
            bullets = []
            
            # Base positions
            cx = self.rect.centerx
            y = self.rect.y
            
            # Velocity constants
            SPEED = 10
            # 30 degrees: vx approx +/- 5, vy approx -8.5
            VX_30 = 5
            VY_30 = -8.5
            # 15 degrees: vx approx +/- 2.5, vy approx -9.6
            VX_15 = 2.5
            VY_15 = -9.6
            
            # Standard Upward Shot (Levels 1-3 base)
            if self.level == 1:
                bullets.append((cx - BULLET_WIDTH // 2, y, 0, -SPEED, b_img))
            elif self.level == 2:
                bullets.append((cx - 10 - BULLET_WIDTH // 2, y, 0, -SPEED, b_img))
                bullets.append((cx + 10 - BULLET_WIDTH // 2, y, 0, -SPEED, b_img))
            elif self.level >= 3:
                bullets.append((cx - 15 - BULLET_WIDTH // 2, y, 0, -SPEED, b_img))
                bullets.append((cx + 15 - BULLET_WIDTH // 2, y, 0, -SPEED, b_img))
                bullets.append((cx - BULLET_WIDTH // 2, y - 5, 0, -SPEED, b_img))

            # Level 4: Add +/- 30 degrees
            if self.level >= 4:
                bullets.append((cx - BULLET_WIDTH // 2, y, -VX_30, VY_30, b_img))
                bullets.append((cx - BULLET_WIDTH // 2, y, VX_30, VY_30, b_img))

            # Level 5: Add +/- 15 degrees (or another pair)
            if self.level >= 5:
                bullets.append((cx - BULLET_WIDTH // 2, y, -VX_15, VY_15, b_img))
                bullets.append((cx - BULLET_WIDTH // 2, y, VX_15, VY_15, b_img))

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
        
    def add_missiles(self, amount):
        self.missiles = min(MAX_MISSILES, self.missiles + amount)
        
    def fire_missile(self):
        if self.missiles > 0:
            self.missiles -= 1
            return True
        return False
    
    def take_damage(self):
        """
        Activates invincibility when spaceship takes damage.
        Returns True if damage can be applied (not invincible), False otherwise.
        """
        if self.is_invincible:
            return False  # Cannot take damage while invincible
        
        # Activate invincibility
        self.is_invincible = True
        self.invincibility_start_time = pygame.time.get_ticks()
        return True  # Damage can be applied

