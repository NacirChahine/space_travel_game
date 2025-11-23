import pygame
from src.config import *
from src.utils.helpers import resource_path

class AssetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.assets = {}
            cls._instance.load_assets()
        return cls._instance

    def load_assets(self):
        # Load logo
        logo_img = pygame.image.load(resource_path('naro_chan_logo.png'))
        self.assets['logo_img'] = pygame.transform.scale(logo_img, (400, 300))

        # Load spaceship
        spaceship_img = pygame.image.load(resource_path('space_ship.png'))
        self.assets['spaceship_img'] = pygame.transform.scale(spaceship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

        # Load asteroids
        asteroid_files = ['asteroid_1.png', 'asteroid_2.png', 'asteroid_3.png']
        self.assets['asteroid_images'] = [
            pygame.transform.scale(pygame.image.load(resource_path(f)), (ASTEROID_WIDTH, ASTEROID_HEIGHT)) 
            for f in asteroid_files
        ]

        # Load backgrounds
        background_files = [
            'background-1.jpg', 'background-2.jpg', 'background-4.jpg', 'background-5.jpg', 'background-6.jpg',
            'background-7.jpg'
        ]
        self.assets['background_images'] = [
            pygame.transform.scale(pygame.image.load(resource_path(f)), (SCREEN_WIDTH, SCREEN_HEIGHT)) 
            for f in background_files
        ]

        # Load sounds
        pygame.mixer.init()
        self.assets['fire_sound'] = pygame.mixer.Sound(resource_path('fire.aiff'))
        self.assets['asteroid_hit_sound'] = pygame.mixer.Sound(resource_path('asteroid_hit.wav'))
        self.assets['crash_sound'] = pygame.mixer.Sound(resource_path('crash.wav'))
        self.assets['end_bomb_sound'] = pygame.mixer.Sound(resource_path('end_bomb.wav'))

        # Load music
        # Note: Music is streamed, not loaded into a dict usually, but we can store the path or init it here
        self.music_path = resource_path('drive-breakbeat.mp3')

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

    def get_asset(self, name):
        return self.assets.get(name)

    def play_music(self):
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play(-1)
