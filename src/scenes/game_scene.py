import pygame
import random
from src.scenes.scene import Scene
from src.scenes.game_over_scene import GameOverScene
from src.entities.spaceship import Spaceship
from src.entities.asteroid import Asteroid
from src.entities.bullet import Bullet
from src.entities.powerup import PowerUp
from src.entities.boss import Boss
from src.ui.hud import HUD
from src.core.background import Background
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
        self.level = 1
        self.level = 1
        self.asteroid_spawn_rate = ASTEROID_SPAWN_RATE_INITIAL
        self.next_boss_score = BOSS_SPAWN_SCORE
        
        # Background
        self.background = Background()
        
        # Entities
        self.spaceship = Spaceship(
            SCREEN_WIDTH // 2, 
            SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10, 
            self.assets['spaceship_img'],
            self.assets['fire_sound']
        )
        self.spaceship.set_assets(self.assets)
        
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.spaceship)
        
        # Timers
        self.asteroid_timer = pygame.time.get_ticks()
        self.powerup_timer = pygame.time.get_ticks()

        # Pause State
        self.paused = False
        self.pause_start_time = 0
        self.font_pause_sub = pygame.font.Font(None, 36)

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.toggle_pause()

                if not self.paused:
                    if event.key == pygame.K_SPACE:
                        new_bullets = self.spaceship.shoot(self.assets['bullet_img'])
                        for bx, by, img in new_bullets:
                            bullet = Bullet(bx, by, img)
                            self.bullets.add(bullet)
                            self.all_sprites.add(bullet)
                        if new_bullets:
                            self.spaceship.decrease_bullets()

    def update(self):
        if self.paused:
            return

        current_time = pygame.time.get_ticks()
        
        # Update Background
        self.background.update()
        
        # Spawn Asteroids
        if current_time - self.asteroid_timer > self.asteroid_spawn_rate:
            asteroid = Asteroid(random.choice(self.assets['asteroid_images']), self.asteroid_speed)
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)
            self.asteroid_timer = current_time
            
        # Spawn Powerups
        if current_time - self.powerup_timer > 5000:
            type = random.choice(['health', 'ammo', 'upgrade'])
            if type == 'health':
                img = self.assets['health_powerup_img']
            elif type == 'ammo':
                img = self.assets['ammo_powerup_img']
            else:
                img = self.assets['upgrade_powerup_img']
                
            powerup = PowerUp(img, type)
            self.powerups.add(powerup)
            self.all_sprites.add(powerup)
            self.powerup_timer = current_time

        # Spawn Boss
        if len(self.bosses) == 0 and self.score >= self.next_boss_score:
             # Spawn Boss
             boss = Boss(SCREEN_WIDTH // 2, 50, self.assets['boss_img'], self.assets['enemy_projectile_img'], BOSS_HEALTH_INITIAL + self.level)
             self.bosses.add(boss)
             self.all_sprites.add(boss)
             self.next_boss_score += BOSS_SPAWN_SCORE

        # Update all sprites
        self.spaceship.update() # Handle input movement
        self.bullets.update()
        self.asteroids.update()
        self.powerups.update()
        self.bosses.update()
        self.enemy_projectiles.update()
        
        # Add new projectiles from bosses to groups
        for boss in self.bosses:
            for projectile in boss.projectiles:
                if projectile not in self.enemy_projectiles:
                    self.enemy_projectiles.add(projectile)
                    self.all_sprites.add(projectile)
            # Clear boss projectiles group to avoid re-adding (or just use group logic)
            # Actually boss.projectiles is a group.
            # We can just add them.
            pass

        # Collisions: Bullet - Asteroid
        hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True)
        for hit in hits:
            self.assets['asteroid_hit_sound'].play()
            self.score += 10
            # self.spaceship.add_bullets(1) # Removed as per request

        # Collisions: Bullet - Boss
        hits = pygame.sprite.groupcollide(self.bosses, self.bullets, False, True)
        for boss, bullets in hits.items():
            self.assets['asteroid_hit_sound'].play()
            for b in bullets:
                if boss.take_damage():
                    boss.kill()
                    self.score += 50
                    self.assets['end_bomb_sound'].play() # Reuse sound for boss death

        # Collisions: Spaceship - Asteroid
        hits = pygame.sprite.spritecollide(self.spaceship, self.asteroids, True)
        for hit in hits:
            self.assets['crash_sound'].play()
            self.lives -= 1
            self.spaceship.downgrade()
            if self.lives == 0:
                self.game.state_manager.change_scene(GameOverScene(self.game, self.score))

        # Collisions: Spaceship - Boss
        hits = pygame.sprite.spritecollide(self.spaceship, self.bosses, False)
        for hit in hits:
            self.assets['crash_sound'].play()
            self.lives -= 1
            self.spaceship.downgrade()
            # Push back spaceship? Or invulnerability? 
            # For now just simple hit.
            if self.lives == 0:
                self.game.state_manager.change_scene(GameOverScene(self.game, self.score))

        # Collisions: Spaceship - Enemy Projectile
        hits = pygame.sprite.spritecollide(self.spaceship, self.enemy_projectiles, True)
        for hit in hits:
            self.assets['crash_sound'].play()
            self.lives -= 1
            self.spaceship.downgrade()
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
            elif hit.type == 'upgrade':
                self.spaceship.upgrade()

        # Level Up / Difficulty Progression
        new_level = (self.score // LEVEL_SCORE_THRESHOLD) + 1
        if new_level > self.level:
            self.level = new_level
            # Increase difficulty
            self.asteroid_speed = min(ASTEROID_SPEED_MAX, ASTEROID_SPEED_INITIAL + self.level)
            self.asteroid_spawn_rate = max(ASTEROID_SPAWN_RATE_MIN, int(ASTEROID_SPAWN_RATE_INITIAL * (DIFFICULTY_MULTIPLIER ** (self.level - 1))))

        # Remove off-screen asteroids and increment score
        for asteroid in self.asteroids:
            if asteroid.rect.y > SCREEN_HEIGHT:
                asteroid.kill()
                self.score += 1

    def render(self, screen):
        # Background
        self.background.draw(screen)
        
        # Sprites
        self.all_sprites.draw(screen)
        
        # HUD
        self.hud.draw(screen, self.lives, MAX_LIVES, self.spaceship.available_bullets, MAX_BULLETS, self.score, self.spaceship.level)

        if self.paused:
            self.draw_pause_screen(screen)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_start_time = pygame.time.get_ticks()
            pygame.mixer.music.pause()
        else:
            pause_duration = pygame.time.get_ticks() - self.pause_start_time
            self.asteroid_timer += pause_duration
            self.powerup_timer += pause_duration
            pygame.mixer.music.unpause()

    def draw_pause_screen(self, screen):
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128)) # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Pause Icon (Two vertical bars)
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        bar_width = 20
        bar_height = 60
        gap = 20
        
        pygame.draw.rect(screen, WHITE, (center_x - gap//2 - bar_width, center_y - bar_height//2 - 20, bar_width, bar_height))
        pygame.draw.rect(screen, WHITE, (center_x + gap//2, center_y - bar_height//2 - 20, bar_width, bar_height))
        
        # Text
        text_surf = self.font_pause_sub.render("Press P to Unpause", True, WHITE)
        text_rect = text_surf.get_rect(center=(center_x, center_y + 40))
        screen.blit(text_surf, text_rect)
