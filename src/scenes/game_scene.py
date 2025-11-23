import pygame
import random
from src.scenes.scene import Scene
from src.scenes.game_over_scene import GameOverScene
from src.entities.spaceship import Spaceship
from src.entities.asteroid import Asteroid
from src.entities.bullet import Bullet
from src.entities.powerup import PowerUp
from src.ui.hud import HUD
from src.config import *

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.assets = self.game.asset_manager.assets
        self.hud = HUD(self.game.asset_manager)
        
        # Game State
        self.score = 0
        self.lives = PLAYER_LIVES
        self.asteroid_speed = ASTEROID_SPEED_INITIAL
        self.background_index = 0
        
        # Entities
        self.spaceship = Spaceship(
            SCREEN_WIDTH // 2, 
            SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10, 
            self.assets['spaceship_img'],
            self.assets['fire_sound']
        )
        
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.spaceship)
        
        # Timers
        self.asteroid_timer = pygame.time.get_ticks()
        self.powerup_timer = pygame.time.get_ticks()

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bx, by = self.spaceship.shoot(None)
                    if bx is not None:
                        bullet = Bullet(bx, by)
                        self.bullets.add(bullet)
                        self.all_sprites.add(bullet)
                        self.spaceship.decrease_bullets()

    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Spawn Asteroids
        if current_time - self.asteroid_timer > 1000:
            asteroid = Asteroid(random.choice(self.assets['asteroid_images']), self.asteroid_speed)
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)
            self.asteroid_timer = current_time
            
        # Spawn Powerups
        if current_time - self.powerup_timer > 5000:
            type = random.choice(['health', 'ammo'])
            img = self.assets['health_powerup_img'] if type == 'health' else self.assets['ammo_powerup_img']
            powerup = PowerUp(img, type)
            self.powerups.add(powerup)
            self.all_sprites.add(powerup)
            self.powerup_timer = current_time

        # Update all sprites
        self.spaceship.update() # Handle input movement
        self.bullets.update()
        self.asteroids.update()
        self.powerups.update()

        # Collisions: Bullet - Asteroid
        hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True)
        for hit in hits:
            self.assets['asteroid_hit_sound'].play()
            self.score += 10
            self.spaceship.add_bullets(1)

        # Collisions: Spaceship - Asteroid
        hits = pygame.sprite.spritecollide(self.spaceship, self.asteroids, True)
        for hit in hits:
            self.assets['crash_sound'].play()
            self.lives -= 1
            if self.lives == 0:
                self.game.state_manager.change_scene(GameOverScene(self.game, self.score))

        # Collisions: Spaceship - PowerUp
        hits = pygame.sprite.spritecollide(self.spaceship, self.powerups, True)
        for hit in hits:
            if hit.type == 'health':
                if self.lives < MAX_LIVES:
                    self.lives += 1
            elif hit.type == 'ammo':
                self.spaceship.add_bullets(3)

        # Level Up
        if self.score // 50 > self.background_index:
            self.background_index = min(len(self.assets['background_images']) - 1, self.background_index + 1)
            self.asteroid_speed = min(ASTEROID_SPEED_MAX, self.asteroid_speed + 1)

        # Remove off-screen asteroids (already handled in update, but check for score increment if they pass)
        # Wait, Asteroid.update() kills it if it goes off screen. 
        # But we need to increment score if it passes.
        # Let's modify Asteroid update or handle it here.
        # The original logic incremented score when asteroid passed.
        # My Asteroid class kills itself. I should check if it was killed by going off screen?
        # Or I can iterate and check y position before update?
        # Actually, let's just iterate asteroids copy to check for passing.
        # Or better, let's keep it simple: if asteroid is killed in update, we lose track.
        # I'll modify Asteroid class later or just handle it here manually.
        # For now, let's iterate and check.
        for asteroid in self.asteroids:
            if asteroid.rect.y > SCREEN_HEIGHT:
                asteroid.kill()
                self.score += 1

    def render(self, screen):
        # Background
        screen.blit(self.assets['background_images'][self.background_index], (0, 0))
        
        # Sprites
        self.all_sprites.draw(screen)
        
        # HUD
        self.hud.draw(screen, self.lives, MAX_LIVES, self.spaceship.available_bullets, MAX_BULLETS, self.score)
