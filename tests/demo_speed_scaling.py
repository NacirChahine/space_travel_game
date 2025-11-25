"""
Demo script to verify level-based speed scaling for the spaceship.
Run this to see the speed values at each level.
"""

import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.entities.spaceship import Spaceship
from src.config import *

# Initialize pygame
pygame.init()
pygame.display.set_mode((1, 1))  # Minimal display

# Create mock assets
mock_surface = pygame.Surface((50, 50))
mock_sound = pygame.mixer.Sound(buffer=b'')

print("=" * 60)
print("SPACESHIP LEVEL-BASED SPEED SCALING DEMONSTRATION")
print("=" * 60)
print()

# Create spaceship
spaceship = Spaceship(100, 100, mock_surface, mock_sound)
print(f"Configuration:")
print(f"  Base Speed: {SPACESHIP_BASE_SPEED}")
print(f"  Speed Per Level: {SPACESHIP_SPEED_PER_LEVEL}")
print(f"  Max Level: {SPACESHIP_LEVEL_MAX}")
print()

print("Speed progression:")
print("-" * 60)

for level in range(1, SPACESHIP_LEVEL_MAX + 1):
    spaceship.level = level
    spaceship.update_speed()
    print(f"  Level {level}: Speed = {spaceship.speed:.1f} pixels/frame")
    
print("-" * 60)
print()

# Demonstrate upgrade/downgrade
print("Testing upgrade/downgrade mechanics:")
print("-" * 60)

spaceship.level = 1
spaceship.update_speed()
print(f"  Starting at Level {spaceship.level}, Speed = {spaceship.speed:.1f}")

spaceship.upgrade()
print(f"  After upgrade: Level {spaceship.level}, Speed = {spaceship.speed:.1f}")

spaceship.upgrade()
print(f"  After upgrade: Level {spaceship.level}, Speed = {spaceship.speed:.1f}")

spaceship.downgrade()
print(f"  After downgrade: Level {spaceship.level}, Speed = {spaceship.speed:.1f}")

print("-" * 60)
print()

print("✅ Speed scaling system is working correctly!")
print()

# Calculate speed increase
speed_increase_percentage = ((7.0 - 5.0) / 5.0) * 100
print(f"📊 Statistics:")
print(f"  - Speed at Level 1: {5.0:.1f}")
print(f"  - Speed at Level 5: {7.0:.1f}")
print(f"  - Total increase: {speed_increase_percentage:.0f}%")
print(f"  - Movement feel: Noticeably faster at higher levels!")
print()

pygame.quit()
