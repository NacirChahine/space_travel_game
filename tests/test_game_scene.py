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
    # Note: scene.level is 8 because we called update() with score 399 (Level 8) previously
    level = 8 
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
    # Level is 1 during first spawn
    level = 1
    gap = max(BOSS_SPAWN_GAP_MIN, BOSS_SPAWN_GAP_INITIAL - (level * BOSS_SPAWN_GAP_DECREASE))
    next_score = current_score + gap
    
    assert scene.next_boss_score == next_score
    
    # Update scene level manually to simulate gameplay progression
    # In real game, level updates every frame. Here we just jumped score.
    # We need to call update() or set level to reflect the score 790.
    # But wait, we just called update() above.
    # So scene.level should now be updated based on score 400.
    # Score 400 -> Level 9.
    assert scene.level == (current_score // LEVEL_SCORE_THRESHOLD) + 1
    
    # Second boss
    scene.score = next_score
    scene.update()
    assert len(scene.bosses) == 2
    
    # Calculate next again
    # Now level should be based on next_score (790) -> Level 16?
    # No, when scene.update() was called with score=next_score (790), 
    # the spawn happened using the level from *before* that update?
    # No, scene.level was updated in the PREVIOUS call (when score was 400).
    # So level is 9.
    
    current_score = next_score
    level = 9 # Level from score 400
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

def test_spaceship_vertical_movement_up():
    """Test spaceship can move up"""
    game = MockGame()
    scene = GameScene(game)
    
    initial_y = scene.spaceship.rect.y
    
    # Simulate UP key press
    pygame.key.get_pressed = lambda: {pygame.K_UP: True, pygame.K_DOWN: False, 
                                       pygame.K_LEFT: False, pygame.K_RIGHT: False}
    scene.spaceship.update()
    
    assert scene.spaceship.rect.y < initial_y

def test_spaceship_vertical_movement_down():
    """Test spaceship can move down"""
    game = MockGame()
    scene = GameScene(game)
    
    initial_y = scene.spaceship.rect.y
    
    # Simulate DOWN key press
    pygame.key.get_pressed = lambda: {pygame.K_UP: False, pygame.K_DOWN: True, 
                                       pygame.K_LEFT: False, pygame.K_RIGHT: False}
    scene.spaceship.update()
    
    assert scene.spaceship.rect.y > initial_y

def test_spaceship_vertical_boundary_top():
    """Test spaceship cannot move above screen boundary"""
    game = MockGame()
    scene = GameScene(game)
    
    # Move spaceship to top
    scene.spaceship.rect.y = 0
    
    # Try to move up
    pygame.key.get_pressed = lambda: {pygame.K_UP: True, pygame.K_DOWN: False, 
                                       pygame.K_LEFT: False, pygame.K_RIGHT: False}
    scene.spaceship.update()
    
    assert scene.spaceship.rect.y == 0

def test_spaceship_vertical_boundary_bottom():
    """Test spaceship cannot move below screen boundary"""
    from src.config import SCREEN_HEIGHT, SPACESHIP_HEIGHT
    game = MockGame()
    scene = GameScene(game)
    
    # Move spaceship to bottom
    scene.spaceship.rect.y = SCREEN_HEIGHT - SPACESHIP_HEIGHT
    
    # Try to move down
    pygame.key.get_pressed = lambda: {pygame.K_UP: False, pygame.K_DOWN: True, 
                                       pygame.K_LEFT: False, pygame.K_RIGHT: False}
    scene.spaceship.update()
    
    assert scene.spaceship.rect.y == SCREEN_HEIGHT - SPACESHIP_HEIGHT

def test_invincibility_activation():
    """Test that spaceship becomes invincible after taking damage"""
    game = MockGame()
    scene = GameScene(game)
    
    assert not scene.spaceship.is_invincible
    
    # Take damage
    result = scene.spaceship.take_damage()
    
    assert result is True  # Damage was applied
    assert scene.spaceship.is_invincible

def test_invincibility_prevents_damage():
    """Test that spaceship cannot take damage while invincible"""
    game = MockGame()
    scene = GameScene(game)
    
    # First damage activates invincibility
    result1 = scene.spaceship.take_damage()
    assert result1 is True
    assert scene.spaceship.is_invincible
    
    # Second damage should be prevented
    result2 = scene.spaceship.take_damage()
    assert result2 is False

def test_invincibility_expires():
    """Test that invincibility expires after 2 seconds"""
    game = MockGame()
    scene = GameScene(game)
    
    # Activate invincibility
    scene.spaceship.take_damage()
    assert scene.spaceship.is_invincible
    
    # Mock time advancement (2000ms = 2 seconds)
    scene.spaceship.invincibility_start_time = pygame.time.get_ticks() - 2000
    scene.spaceship.update()
    
    assert not scene.spaceship.is_invincible
    assert scene.spaceship.visible is True

def test_invincibility_blinking_effect():
    """Test that spaceship blinks during invincibility"""
    game = MockGame()
    scene = GameScene(game)
    
    # Activate invincibility
    scene.spaceship.take_damage()
    
    # Check blinking at different time intervals
    # At 0ms: visible
    scene.spaceship.invincibility_start_time = pygame.time.get_ticks()
    scene.spaceship.update()
    assert scene.spaceship.visible is True
    
    # At 100ms: not visible (first blink)
    scene.spaceship.invincibility_start_time = pygame.time.get_ticks() - 100
    scene.spaceship.update()
    assert scene.spaceship.visible is False
    
    # At 200ms: visible
    scene.spaceship.invincibility_start_time = pygame.time.get_ticks() - 200
    scene.spaceship.update()
    assert scene.spaceship.visible is True

def test_collision_with_invincibility():
    """Test that collision damage is prevented during invincibility"""
    game = MockGame()
    scene = GameScene(game)
    
    initial_lives = scene.lives
    
    # Activate invincibility
    scene.spaceship.take_damage()
    scene.lives = initial_lives  # Reset lives for test
    
    # Create and add an asteroid
    from src.entities.asteroid import Asteroid
    asteroid = Asteroid(game.asset_manager.assets['asteroid_images'][0], 5)
    asteroid.rect.center = scene.spaceship.rect.center  # Position for collision
    scene.asteroids.add(asteroid)
    scene.all_sprites.add(asteroid)
    
    # Update to process collision
    scene.update()
    
    # Lives should not decrease because of invincibility
    assert scene.lives == initial_lives

def test_spaceship_speed_at_level_1():
    """Test that spaceship has base speed at level 1"""
    from src.config import SPACESHIP_BASE_SPEED
    game = MockGame()
    scene = GameScene(game)
    
    assert scene.spaceship.level == 1
    assert scene.spaceship.speed == SPACESHIP_BASE_SPEED

def test_spaceship_speed_increases_with_level():
    """Test that spaceship speed increases when upgrading"""
    from src.config import SPACESHIP_BASE_SPEED, SPACESHIP_SPEED_PER_LEVEL
    game = MockGame()
    scene = GameScene(game)
    
    initial_speed = scene.spaceship.speed
    
    # Upgrade to level 2
    scene.spaceship.upgrade()
    assert scene.spaceship.level == 2
    expected_speed = SPACESHIP_BASE_SPEED + (2 - 1) * SPACESHIP_SPEED_PER_LEVEL
    assert scene.spaceship.speed == expected_speed
    assert scene.spaceship.speed > initial_speed

def test_spaceship_speed_decreases_with_downgrade():
    """Test that spaceship speed decreases when downgrading"""
    game = MockGame()
    scene = GameScene(game)
    
    # Upgrade to level 3
    scene.spaceship.upgrade()
    scene.spaceship.upgrade()
    level_3_speed = scene.spaceship.speed
    
    # Downgrade to level 2
    scene.spaceship.downgrade()
    assert scene.spaceship.level == 2
    assert scene.spaceship.speed < level_3_speed

def test_spaceship_speed_at_max_level():
    """Test that spaceship has maximum speed at level 5"""
    from src.config import SPACESHIP_BASE_SPEED, SPACESHIP_SPEED_PER_LEVEL, SPACESHIP_LEVEL_MAX
    game = MockGame()
    scene = GameScene(game)
    
    # Upgrade to max level
    while scene.spaceship.level < SPACESHIP_LEVEL_MAX:
        scene.spaceship.upgrade()
    
    assert scene.spaceship.level == SPACESHIP_LEVEL_MAX
    expected_max_speed = SPACESHIP_BASE_SPEED + (SPACESHIP_LEVEL_MAX - 1) * SPACESHIP_SPEED_PER_LEVEL
    assert scene.spaceship.speed == expected_max_speed

def test_spaceship_speed_progression():
    """Test speed progression through all levels"""
    from src.config import SPACESHIP_BASE_SPEED, SPACESHIP_SPEED_PER_LEVEL
    game = MockGame()
    scene = GameScene(game)
    
    # Test progression: Level 1 -> 2 -> 3 -> 4 -> 5
    expected_speeds = [
        SPACESHIP_BASE_SPEED + (i - 1) * SPACESHIP_SPEED_PER_LEVEL 
        for i in range(1, 6)
    ]
    
    for i, expected_speed in enumerate(expected_speeds, start=1):
        assert scene.spaceship.level == i
        assert scene.spaceship.speed == expected_speed
        if i < 5:
            scene.spaceship.upgrade()

