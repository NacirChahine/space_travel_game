import pygame
import pytest
from unittest.mock import MagicMock, Mock
from src.scenes.game_scene import GameScene
from src.config import BOSS_SPAWN_SCORE_INITIAL, BOSS_SPAWN_GAP_INITIAL, BOSS_SPAWN_GAP_DECREASE, BOSS_SPAWN_GAP_MIN, LEVEL_SCORE_THRESHOLD

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
            'chaser_img': mock_surface,
            'shooter_img': mock_surface,
            'missile_img': mock_surface,
            'missile_powerup_img': mock_surface,
            'asteroid_images': [mock_surface, mock_surface],
            'fire_sound': mock_sound,
            'asteroid_hit_sound': mock_sound,
            'crash_sound': mock_sound,
            'end_bomb_sound': mock_sound,
            'missile_launch_sound': mock_sound,
            'spaceship_levels': {
                1: mock_surface,
                2: mock_surface,
                3: mock_surface
            }
        }

def test_boss_spawn_at_initial_score():
    """Test that boss spawns when score reaches initial threshold"""
    game = MockGame()
    scene = GameScene(game)
    
    # Initially no bosses
    assert len(scene.bosses) == 0
    assert scene.next_boss_score == BOSS_SPAWN_SCORE_INITIAL
    
    # Set score just below threshold
    scene.score = BOSS_SPAWN_SCORE_INITIAL - 1
    scene.update()
    assert len(scene.bosses) == 0
    
    # Set score to threshold
    scene.score = BOSS_SPAWN_SCORE_INITIAL
    scene.update()
    assert len(scene.bosses) == 1
    
    # Calculate expected next score
    level = (BOSS_SPAWN_SCORE_INITIAL // LEVEL_SCORE_THRESHOLD) + 1
    gap = max(BOSS_SPAWN_GAP_MIN, BOSS_SPAWN_GAP_INITIAL - (level * BOSS_SPAWN_GAP_DECREASE))
    expected_next = BOSS_SPAWN_SCORE_INITIAL + gap
    
    assert scene.next_boss_score == expected_next

def test_boss_spawn_progressive():
    """Test that bosses spawn at progressively calculated thresholds"""
    game = MockGame()
    scene = GameScene(game)
    
    current_score = BOSS_SPAWN_SCORE_INITIAL
    
    # First boss
    scene.score = current_score
    scene.update()
    assert len(scene.bosses) == 1
    
    # Calculate next
    level = (current_score // LEVEL_SCORE_THRESHOLD) + 1
    gap = max(BOSS_SPAWN_GAP_MIN, BOSS_SPAWN_GAP_INITIAL - (level * BOSS_SPAWN_GAP_DECREASE))
    next_score = current_score + gap
    
    assert scene.next_boss_score == next_score
    
    # Second boss
    scene.score = next_score
    scene.update()
    assert len(scene.bosses) == 2
    
    # Calculate next again
    current_score = next_score
    level = (current_score // LEVEL_SCORE_THRESHOLD) + 1
    gap = max(BOSS_SPAWN_GAP_MIN, BOSS_SPAWN_GAP_INITIAL - (level * BOSS_SPAWN_GAP_DECREASE))
    next_score = current_score + gap
    
    assert scene.next_boss_score == next_score

def test_no_boss_before_threshold():
    """Test that no boss spawns before reaching first threshold"""
    game = MockGame()
    scene = GameScene(game)
    
    # Test various scores below initial threshold
    for score in [0, 50, 100, BOSS_SPAWN_SCORE_INITIAL - 1]:
        scene.score = score
        scene.update()
        assert len(scene.bosses) == 0, f"Boss should not spawn at score {score}"

def test_boss_spawn_with_score_jump():
    """Test that boss spawns correctly when score jumps over threshold"""
    game = MockGame()
    scene = GameScene(game)
    
    # Jump over threshold
    scene.score = BOSS_SPAWN_SCORE_INITIAL + 10
    scene.update()
    assert len(scene.bosses) == 1
    
    # Next score should be set correctly relative to the *previous* threshold logic
    # Note: The code adds gap to the *previous* next_boss_score, not current score.
    # So next_boss_score should be BOSS_SPAWN_SCORE_INITIAL + gap
    
    level = (scene.score // LEVEL_SCORE_THRESHOLD) + 1
    # Wait, the code uses self.level which is updated in update()
    # Let's check if level is updated before or after boss spawn?
    # In update(): Boss spawn is BEFORE Level Up check.
    # So self.level is still 1 (or whatever it was initialized/updated to previously).
    # But wait, self.level is updated at the end of update().
    # So for the FIRST boss spawn, self.level is likely 1 (initialized in __init__).
    
    # Let's re-verify the logic in GameScene.update()
    # Boss spawn uses self.level.
    # Level update is at the end.
    # So if we set score manually, self.level might be stale if we don't update it.
    # But in the test we just set scene.score.
    # scene.level is 1 by default.
    
    # So gap calculation uses level=1.
    gap = max(BOSS_SPAWN_GAP_MIN, BOSS_SPAWN_GAP_INITIAL - (1 * BOSS_SPAWN_GAP_DECREASE))
    # gap = 400 - 10 = 390.
    
    assert scene.next_boss_score == BOSS_SPAWN_SCORE_INITIAL + gap

def test_multiple_bosses_can_exist():
    """Test that multiple bosses can exist simultaneously"""
    game = MockGame()
    scene = GameScene(game)
    
    # Spawn first boss
    scene.score = BOSS_SPAWN_SCORE_INITIAL
    scene.update()
    first_boss = list(scene.bosses)[0]
    
    # Force spawn second boss
    scene.score = scene.next_boss_score
    scene.update()
    assert len(scene.bosses) == 2
    assert first_boss in scene.bosses  # First boss still exists

