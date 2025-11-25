import os

# Game Version
# Update this version number when game mechanics or difficulty changes
# Each version maintains its own separate leaderboard
GAME_VERSION = "3.1.1"

# Screen settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 150)
RED = (200, 0, 50)
GREEN = (0, 200, 50)
BLUE = (50, 50, 200)
SHADOW_COLOR = (50, 50, 50)

# Entity Dimensions
SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 50
ASTEROID_WIDTH = 50
ASTEROID_HEIGHT = 50
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
POWERUP_WIDTH = 30
POWERUP_HEIGHT = 30

# Game Settings
PLAYER_LIVES = 3
MAX_LIVES = 5
INITIAL_BULLETS = 25
MAX_BULLETS = 40
INITIAL_MISSILES = 1
MAX_MISSILES = 3
ASTEROID_SPEED_INITIAL = 5
ASTEROID_SPEED_MAX = 15
POWERUP_SPEED = 3
AMMO_POWERUP_BULLETS = 8

# Difficulty Settings
LEVEL_SCORE_THRESHOLD = 50
ASTEROID_SPAWN_RATE_INITIAL = 1000
ASTEROID_SPAWN_RATE_MIN = 300
DIFFICULTY_MULTIPLIER = 0.9  # Multiply spawn rate by this every level

# Events
ASTEROID_SPAWN_EVENT = 0  # Will be set in pygame setup
POWERUP_SPAWN_EVENT = 0   # Will be set in pygame setup

# Upgrades
SPACESHIP_LEVEL_MAX = 5
MISSILE_POWERUP_CHANCE = 0.1 # 10% chance when a powerup spawns
UPGRADE_DURATION = 0 # Permanent until hit? Or temporary? Request implies permanent until hit.

# Boss
BOSS_HEALTH_INITIAL = 5
BOSS_SPAWN_SCORE = 200 # Score to spawn bosses (every 200 points)
BOSS_WIDTH = 80
BOSS_HEIGHT = 80
BOSS_PROJECTILE_SPEED = 7

# Boss Difficulty Tiers
# Difficulty is determined by health and projectile count
# Colors provide visual indicators for difficulty
BOSS_DIFFICULTY_TIERS = {
    'WEAK': {
        'health_range': (3, 5),
        'projectile_count': 2,
        'color': (100, 200, 100),  # Green - Easy
        'border_color': (150, 255, 150)
    },
    'MEDIUM': {
        'health_range': (6, 10),
        'projectile_count': 3,
        'color': (200, 150, 50),  # Orange - Medium
        'border_color': (255, 200, 100)
    },
    'STRONG': {
        'health_range': (11, 20),
        'projectile_count': 4,
        'color': (200, 50, 50),  # Red - Hard
        'border_color': (255, 100, 100)
    }
}

# UI Colors
GLASS_BG = (0, 0, 0, 128) # 50% transparent black
GLASS_BORDER = (255, 255, 255, 100) # Semi-transparent white
LEVEL_BAR_COLOR = (0, 255, 255) # Cyan for level
MISSILE_COLOR = (255, 165, 0) # Orange for missiles
