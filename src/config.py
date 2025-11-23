import os

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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
INITIAL_BULLETS = 5
MAX_BULLETS = 10
ASTEROID_SPEED_INITIAL = 5
ASTEROID_SPEED_MAX = 15
POWERUP_SPEED = 3

# Difficulty Settings
LEVEL_SCORE_THRESHOLD = 50
ASTEROID_SPAWN_RATE_INITIAL = 1000
ASTEROID_SPAWN_RATE_MIN = 300
DIFFICULTY_MULTIPLIER = 0.9  # Multiply spawn rate by this every level

# Events
ASTEROID_SPAWN_EVENT = 0  # Will be set in pygame setup
POWERUP_SPAWN_EVENT = 0   # Will be set in pygame setup

# Upgrades
SPACESHIP_LEVEL_MAX = 3
UPGRADE_DURATION = 0 # Permanent until hit? Or temporary? Request implies permanent until hit.

# Boss
BOSS_HEALTH_INITIAL = 5
BOSS_SPAWN_SCORE = 100 # Score to spawn first boss
BOSS_WIDTH = 80
BOSS_HEIGHT = 80
BOSS_PROJECTILE_SPEED = 7

# UI Colors
GLASS_BG = (0, 0, 0, 128) # 50% transparent black
GLASS_BORDER = (255, 255, 255, 100) # Semi-transparent white
LEVEL_BAR_COLOR = (0, 255, 255) # Cyan for level
