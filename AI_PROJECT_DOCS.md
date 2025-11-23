# AI Project Documentation

## Project Overview
This is a space shooter game developed with Pygame. It features a modular architecture to support scalability and maintainability.

## Architecture
The project follows a component-based architecture with a scene management system.

### Core Components
- **Game**: The main entry point that initializes the engine.
- **StateManager**: Manages transitions between scenes.
- **AssetManager**: Handles loading and caching of assets.
- **DBManager**: Manages MongoDB connections.

### Entities
- **Entity**: Base class for all game objects.
- **Spaceship**: Player character with upgrade levels (1-3) and weapon systems.
- **Asteroid**: Obstacles with varying sizes and speeds.
- **Bullet**: Projectiles fired by the spaceship.
- **PowerUp**: Collectible items (health, ammo, upgrade).
- **Boss**: Enemy bosses with difficulty tiers and color-coded visual indicators.
  - **Difficulty Tiers**: WEAK (green), MEDIUM (orange), STRONG (red)
  - **Scaling Attributes**: Health (3-20 HP), Projectile Count (2-4)
  - **Color Overlay**: Visual feedback indicating difficulty level
- **EnemyProjectile**: Projectiles fired by bosses.

### Scenes
- **WelcomeScene**: Start screen.
- **GameScene**: Main gameplay loop with:
  - Dynamic asteroid spawning
  - Power-up collection system
  - Multiple simultaneous boss battles
  - Pause functionality
  - Progressive difficulty scaling
- **GameOverScene**: End screen with high scores.

## Development
- **Language**: Python 3.x
- **Framework**: Pygame
- **Database**: MongoDB

## Testing
Run tests using `pytest`:
```bash
python -m pytest tests/
```
