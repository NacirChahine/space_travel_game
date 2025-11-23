import pygame
import pytest
from unittest.mock import MagicMock, Mock
from src.scenes.game_scene import GameScene
from src.config import BOSS_SPAWN_SCORE

# Mock pygame
pygame.init()
pygame.display.set_mode((1, 1))

class MockGame:
    """Mock Game object for testing"""
    def __init__(self):
        self.asset_manager = MagicMock()
        self.state_manager = MagicMock()
        
        # Create mock assets
        mock_surface = pygame.Surface((50, 50))
        mock_sound = pygame.mixer.Sound(buffer=b'')
        
        self.asset_manager.assets = {
            'spaceship_img': mock_surface,
            'boss_img': mock_surface,
            'bullet_img': mock_surface,
            'enemy_projectile_img': mock_surface,
            'health_powerup_img': mock_surface,
            'ammo_powerup_img': mock_surface,
            'upgrade_powerup_img': mock_surface,
            'asteroid_images': [mock_surface, mock_surface],
            'fire_sound': mock_sound,
            'asteroid_hit_sound': mock_sound,
            'crash_sound': mock_sound,
            'end_bomb_sound': mock_sound,
            'spaceship_levels': {
                1: mock_surface,
                2: mock_surface,
                3: mock_surface
            }
        }

def test_boss_spawn_at_score_200():
    """Test that boss spawns when score reaches 200"""
    game = MockGame()
    scene = GameScene(game)
    
    # Initially no bosses
    assert len(scene.bosses) == 0
    assert scene.next_boss_score == BOSS_SPAWN_SCORE  # Should be 200
    
    # Set score to 199, no boss should spawn
    scene.score = 199
    scene.update()
    assert len(scene.bosses) == 0
    
    # Set score to 200, boss should spawn
    scene.score = 200
    scene.update()
    assert len(scene.bosses) == 1
    assert scene.next_boss_score == 400  # Next boss at 400

def test_boss_spawn_at_multiple_thresholds():
    """Test that bosses spawn at correct score milestones (200, 400, 600, etc.)"""
    game = MockGame()
    scene = GameScene(game)
    
    # Score 200 - first boss
    scene.score = 200
    scene.update()
    assert len(scene.bosses) == 1
    assert scene.next_boss_score == 400
    
    # Score 350 - no new boss
    scene.score = 350
    scene.update()
    assert len(scene.bosses) == 1
    assert scene.next_boss_score == 400
    
    # Score 400 - second boss
    scene.score = 400
    scene.update()
    assert len(scene.bosses) == 2
    assert scene.next_boss_score == 600
    
    # Score 600 - third boss
    scene.score = 600
    scene.update()
    assert len(scene.bosses) == 3
    assert scene.next_boss_score == 800
    
    # Score 800 - fourth boss
    scene.score = 800
    scene.update()
    assert len(scene.bosses) == 4
    assert scene.next_boss_score == 1000

def test_no_boss_before_threshold():
    """Test that no boss spawns before reaching first threshold"""
    game = MockGame()
    scene = GameScene(game)
    
    # Test various scores below 200
    for score in [0, 50, 100, 150, 199]:
        scene.score = score
        scene.update()
        assert len(scene.bosses) == 0, f"Boss should not spawn at score {score}"

def test_boss_spawn_with_score_jump():
    """Test that boss spawns correctly when score jumps over threshold"""
    game = MockGame()
    scene = GameScene(game)
    
    # Jump from 190 to 210 (skipping 200)
    scene.score = 190
    scene.update()
    assert len(scene.bosses) == 0
    
    scene.score = 210
    scene.update()
    assert len(scene.bosses) == 1
    assert scene.next_boss_score == 400

def test_multiple_bosses_can_exist():
    """Test that multiple bosses can exist simultaneously"""
    game = MockGame()
    scene = GameScene(game)
    
    # Spawn first boss
    scene.score = 200
    scene.update()
    first_boss = list(scene.bosses)[0]
    
    # Spawn second boss without killing first
    scene.score = 400
    scene.update()
    assert len(scene.bosses) == 2
    assert first_boss in scene.bosses  # First boss still exists
