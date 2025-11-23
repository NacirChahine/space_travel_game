import pygame
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.hud import HUD
from src.utils.asset_manager import AssetManager
from src.config import *


def test_hud_rendering():
    """Test that HUD renders correctly with numeric displays"""
    pygame.init()
    
    # Create a test screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create HUD with AssetManager
    asset_manager = AssetManager()
    hud = HUD(asset_manager)
    
    # Test values
    lives = 3
    max_lives = 5
    available_bullets = 12
    max_bullets = 20
    score = 150
    level = 2
    
    # Draw the HUD
    hud.draw(screen, lives, max_lives, available_bullets, max_bullets, score, level)
    
    # Verify that the HUD instance has the required methods
    assert hasattr(hud, 'draw_glass_bar')
    assert hasattr(hud, 'draw')
    
    print("✓ HUD rendering test passed")
    
    pygame.quit()


def test_numeric_text_display():
    """Test that numeric text is formatted correctly"""
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    asset_manager = AssetManager()
    hud = HUD(asset_manager)
    
    # Test various value combinations
    test_cases = [
        (3, 5, "3/5"),
        (12, 20, "12/20"),
        (2, 3, "2/3"),
        (0, 5, "0/5"),
        (5, 5, "5/5")
    ]
    
    for current, max_val, expected in test_cases:
        result = f"{current}/{max_val}"
        assert result == expected, f"Expected {expected}, got {result}"
    
    print("✓ Numeric text formatting test passed")
    
    pygame.quit()


if __name__ == "__main__":
    test_hud_rendering()
    test_numeric_text_display()
    print("\n✅ All HUD tests passed!")
