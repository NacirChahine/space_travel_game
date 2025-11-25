import pygame
from src.config import *
from src.utils.helpers import resource_path
from src.utils.graphics import GraphicsGenerator

class AssetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.assets = {}
            cls._instance.load_assets()
        return cls._instance

    def load_assets(self):
        # Load logo (Keep logo as image if available, or draw text? Plan said remove dependency on external images.
        # But logo might be special. Let's keep logo loading but fallback or just keep it if it exists.
        # The plan said "Convert all current image-based assets...".
        # Let's assume we keep the logo file for branding, but everything else is drawn.
        try:
            logo_img = pygame.image.load(resource_path('naro_chan_logo.png'))
            self.assets['logo_img'] = pygame.transform.scale(logo_img, (400, 300))
        except:
            # Fallback if logo missing
            self.assets['logo_img'] = pygame.Surface((400, 300))
            self.assets['logo_img'].fill(BLACK)

        # Generate spaceship levels
        self.assets['spaceship_levels'] = {
            1: GraphicsGenerator.draw_spaceship(SPACESHIP_WIDTH, SPACESHIP_HEIGHT, 1),
            2: GraphicsGenerator.draw_spaceship(SPACESHIP_WIDTH, SPACESHIP_HEIGHT, 2),
            3: GraphicsGenerator.draw_spaceship(SPACESHIP_WIDTH, SPACESHIP_HEIGHT, 3),
            4: GraphicsGenerator.draw_spaceship(SPACESHIP_WIDTH, SPACESHIP_HEIGHT, 3), # Reuse level 3 for now
            5: GraphicsGenerator.draw_spaceship(SPACESHIP_WIDTH, SPACESHIP_HEIGHT, 3)  # Reuse level 3 for now
        }
        self.assets['spaceship_img'] = self.assets['spaceship_levels'][1] # Default

        # Generate asteroids
        # Create a few variations
        self.assets['asteroid_images'] = [
            GraphicsGenerator.draw_asteroid(ASTEROID_WIDTH, ASTEROID_HEIGHT) for _ in range(5)
        ]

        # Backgrounds will be handled by Background class, but we can keep a placeholder or remove this.
        # The plan says "Replace the static background image blitting with the Background class".
        # So we don't need 'background_images' here anymore, or we can leave empty list.
        self.assets['background_images'] = [] 

        # Generate Bullet
        self.assets['bullet_img'] = GraphicsGenerator.draw_bullet(BULLET_WIDTH, BULLET_HEIGHT, 1)
        self.assets['bullet_levels'] = {
            1: GraphicsGenerator.draw_bullet(BULLET_WIDTH, BULLET_HEIGHT, 1),
            2: GraphicsGenerator.draw_bullet(BULLET_WIDTH, BULLET_HEIGHT, 2),
            3: GraphicsGenerator.draw_bullet(BULLET_WIDTH, BULLET_HEIGHT, 3),
            4: GraphicsGenerator.draw_bullet(BULLET_WIDTH, BULLET_HEIGHT, 3),
            5: GraphicsGenerator.draw_bullet(BULLET_WIDTH, BULLET_HEIGHT, 3)
        }

        # Generate Missile
        self.assets['missile_img'] = GraphicsGenerator.draw_missile(20, 40)

        # Generate Explosion Frames
        self.assets['explosion_frames'] = []
        for i in range(10):
            radius = 10 + i * 15 # Expanding radius
            alpha = max(0, 255 - i * 25) # Fading out
            color_core = (255, 255, 200, alpha)
            color_outer = (255, 100, 0, alpha)
            self.assets['explosion_frames'].append(
                GraphicsGenerator.draw_explosion_frame(radius, color_core, color_outer)
            )
        
        # Generate Fullscreen Missile Explosion Frames
        self.assets['missile_explosion_frames'] = []
        for i in range(15):
            # Create a fullscreen surface
            explosion_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            
            # Calculate alpha for fade in/out effect
            if i < 5:
                # Fade in quickly
                alpha = int((i / 5) * 180)
            else:
                # Fade out gradually
                alpha = max(0, int(180 - ((i - 5) / 10) * 180))
            
            # Draw multiple expanding rings from center
            center_x = SCREEN_WIDTH // 2
            center_y = SCREEN_HEIGHT // 2
            
            # Create pulsing wave effect
            for j in range(3):
                ring_progress = (i + j * 3) / 18.0
                if ring_progress <= 1.0:
                    ring_radius = int(ring_progress * max(SCREEN_WIDTH, SCREEN_HEIGHT) * 1.5)
                    ring_alpha = int(alpha * (1.0 - ring_progress))
                    
                    # Outer ring (orange)
                    pygame.draw.circle(explosion_surface, (255, 150, 0, ring_alpha), 
                                     (center_x, center_y), ring_radius, 
                                     max(1, int(30 * (1.0 - ring_progress))))
                    
                    # Inner ring (bright yellow/white)
                    if ring_radius > 20:
                        pygame.draw.circle(explosion_surface, (255, 255, 200, ring_alpha), 
                                         (center_x, center_y), ring_radius - 15, 
                                         max(1, int(20 * (1.0 - ring_progress))))
            
            # Add flash overlay at the beginning
            if i < 3:
                flash_alpha = int((1.0 - i/3) * 100)
                flash_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                flash_overlay.fill((255, 255, 255, flash_alpha))
                explosion_surface.blit(flash_overlay, (0, 0))
            
            self.assets['missile_explosion_frames'].append(explosion_surface)

        # Generate Boss
        self.assets['boss_img'] = GraphicsGenerator.draw_boss(BOSS_WIDTH, BOSS_HEIGHT)
        self.assets['enemy_projectile_img'] = GraphicsGenerator.draw_enemy_projectile(10, 10)

        # Load sounds
        pygame.mixer.init()
        try:
            self.assets['fire_sound'] = pygame.mixer.Sound(resource_path('fire.aiff'))
            self.assets['asteroid_hit_sound'] = pygame.mixer.Sound(resource_path('asteroid_hit.wav'))
            self.assets['crash_sound'] = pygame.mixer.Sound(resource_path('crash.wav'))
            self.assets['end_bomb_sound'] = pygame.mixer.Sound(resource_path('end_bomb.wav'))
            self.assets['missile_launch_sound'] = pygame.mixer.Sound(resource_path('missile.wav'))
            self.music_path = resource_path('drive-breakbeat.mp3')
        except:
            print("Warning: Sound files not found. Running without sound.")
            # Create dummy sounds to prevent crashes
            dummy_sound = pygame.mixer.Sound(buffer=bytearray([0]*100))
            self.assets['fire_sound'] = dummy_sound
            self.assets['asteroid_hit_sound'] = dummy_sound
            self.assets['crash_sound'] = dummy_sound
            self.assets['end_bomb_sound'] = dummy_sound
            self.assets['missile_launch_sound'] = dummy_sound
            self.music_path = None

        # Create Power-up Assets
        self._create_powerup_assets()

    def _create_powerup_assets(self):
        # Health Power-up (Red Cross)
        health_pu_surf = pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(health_pu_surf, (255, 255, 255), (POWERUP_WIDTH // 2, POWERUP_HEIGHT // 2), POWERUP_WIDTH // 2)
        pygame.draw.rect(health_pu_surf, RED, (POWERUP_WIDTH // 2 - 4, 5, 8, 20))
        pygame.draw.rect(health_pu_surf, RED, (5, POWERUP_HEIGHT // 2 - 4, 20, 8))
        self.assets['health_powerup_img'] = health_pu_surf

        # Ammo Power-up (Yellow Bullet Icon)
        ammo_pu_surf = pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(ammo_pu_surf, (50, 50, 50), (POWERUP_WIDTH // 2, POWERUP_HEIGHT // 2), POWERUP_WIDTH // 2)
        # Draw simplified bullet shape
        pygame.draw.rect(ammo_pu_surf, YELLOW, (10, 8, 10, 14))
        pygame.draw.polygon(ammo_pu_surf, YELLOW, [(10, 8), (20, 8), (15, 2)])
        self.assets['ammo_powerup_img'] = ammo_pu_surf

        # Missile Power-up (Blue Orb with 'M')
        missile_pu_surf = pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(missile_pu_surf, (50, 50, 100), (POWERUP_WIDTH // 2, POWERUP_HEIGHT // 2), POWERUP_WIDTH // 2)
        # Draw 'M'
        font_pu = pygame.font.SysFont(None, 24)
        m_surf = font_pu.render("M", True, (255, 165, 0))
        missile_pu_surf.blit(m_surf, (POWERUP_WIDTH // 2 - m_surf.get_width()//2, POWERUP_HEIGHT // 2 - m_surf.get_height()//2))
        self.assets['missile_powerup_img'] = missile_pu_surf

        # Upgrade Power-up (Blue Up Arrow)
        upgrade_pu_surf = pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(upgrade_pu_surf, (50, 50, 100), (POWERUP_WIDTH // 2, POWERUP_HEIGHT // 2), POWERUP_WIDTH // 2)
        # Draw arrow
        pygame.draw.polygon(upgrade_pu_surf, (0, 255, 255), [
            (POWERUP_WIDTH // 2, 5), 
            (POWERUP_WIDTH - 5, POWERUP_HEIGHT // 2), 
            (POWERUP_WIDTH // 2 + 5, POWERUP_HEIGHT // 2),
            (POWERUP_WIDTH // 2 + 5, POWERUP_HEIGHT - 5),
            (POWERUP_WIDTH // 2 - 5, POWERUP_HEIGHT - 5),
            (POWERUP_WIDTH // 2 - 5, POWERUP_HEIGHT // 2),
            (5, POWERUP_HEIGHT // 2)
        ])
        self.assets['upgrade_powerup_img'] = upgrade_pu_surf

    def get_asset(self, name):
        return self.assets.get(name)

    def play_music(self):
        if self.music_path:
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play(-1)
            except:
                pass
