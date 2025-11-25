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
- **Spaceship**: Player character with upgrade levels (1-5) and weapon systems.
  - **Level 1**: Light blue hull, single orange engine
  - **Level 2**: Medium blue hull, enhanced side wings, single red engine
  - **Level 3**: Deep blue hull, extra cannons, single bright red engine
  - **Level 4**: Purple hull, hexagonal armor plating, shield emitters, dual cyan engines
  - **Level 5**: Elite deep purple/gold hull, energy cores, advanced wing structure, triple gold engines
- **Asteroid**: Obstacles with varying sizes and speeds.
- **Bullet**: Projectiles fired by the spaceship.
- **Missile**: Screen-clearing projectiles that dynamically target the viewport center.
  - **Dynamic Trajectory**: Calculates viewport center on each update, accounting for camera movement
  - **Movement**: Uses normalized vector math to travel toward the center at constant speed
  - **Visual Rotation**: Sprite rotates to face its direction of travel for realistic appearance
  - **Launch Sound**: Plays dedicated missile.wav sound effect on launch
  - **Explosion**: Triggers when reaching within 20 pixels of viewport center
  - **Fullscreen Effect**: Explosion covers entire viewport with expanding wave animation
- **PowerUp**: Collectible items (health, ammo, upgrade, missile).
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
  - Score-based boss spawning (every 200 points: at scores 200, 400, 600, etc.)
  - Multiple simultaneous boss battles
  - Pause functionality
  - Progressive difficulty scaling
  - **HUD**: Glassmorphic UI with real-time numeric displays inside the progress bars:
    - Health: current/max (e.g., "3/5") - centered inside health bar
    - Ammo: current/max (e.g., "12/20") - centered inside ammo bar
    - Ship Level: current/max (e.g., "2/5") - centered inside level bar
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
