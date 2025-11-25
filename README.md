# Space Travel Game

A retro-style space shooter game built with Pygame.

## Features
- **Spaceship Control**: Navigate your ship horizontally and vertically to avoid obstacles.
  - **Movement**: Use arrow keys for full directional control (left, right, up, down)
  - **Speed Scaling**: Movement speed increases with spaceship level (faster at higher levels)
  - **Invincibility**: 2-second invincibility period after taking damage with blinking visual effect
- **Shooting**: Blast asteroids with your laser.
- **Dynamic Visuals**: Immersive space environment with:
  - **Animated Star Field**: Multi-layered parallax stars with realistic twinkling effects
  - **Meteor Showers**: Dynamic meteors streaking across the screen with gradient tails
  - **Nebula Effects**: Semi-transparent cosmic clouds drifting in the background
  - **Responsive Design**: All UI elements scale proportionally with screen dimensions (currently 1600x900)
- **Spaceship Upgrades**: Level up your spaceship to unlock powerful bullet patterns (up to Level 5 with angled shots).
- **Missile System**: Collect and fire missiles (Press 'M') to clear the screen of enemies.
  - Missiles dynamically target the viewport center, accounting for camera movement
  - Visual rotation: missile sprite rotates to face its direction of travel
  - Launch sound effect plays when fired
  - Fullscreen explosion effect covers entire viewport with expanding wave animation
  - Clear all asteroids, bosses, and enemy projectiles on detonation
- **Power-ups**: Collect health, ammo, upgrades, and rare missiles.
- **Boss Battles**: Face off against challenging bosses with unique attack patterns.
  - **Score-Based Spawning**: Bosses spawn at score milestones (200, 400, 600, 800, etc.)
  - **Visual Difficulty Indicators**: Bosses are color-coded (Green = Weak, Orange = Medium, Red = Strong)
  - **Dynamic Difficulty**: Boss strength scales with health and projectile count
- **HUD Display**: Real-time numeric displays centered inside progress bars showing health, ammo, and ship level values (e.g., "3/5", "12/20").
- **High Scores**: Compete for the top spot on the leaderboard (MongoDB).
- **Progressive Difficulty**: Game gets harder as you progress through levels.

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up environment variables:
    - Create a `.env` file based on `.env.example`.
    - Add your `MONGODB_URI`.

## Running the Game

Run the game using the main entry point:
```bash
python main.py
```

## Building the Executable

You can build a standalone executable using PyInstaller. First, ensure PyInstaller is installed:

```bash
pip install pyinstaller
```

### Windows

```bash
pyinstaller --clean --onefile --noconsole --icon="assets/space_travel.ico" --add-data "assets;assets" --add-data ".env;." main.py
```

### macOS / Linux

Note: The path separator for `--add-data` is `:` on Unix-like systems.

```bash
pyinstaller --clean --onefile --noconsole --icon="assets/space_travel.ico" --add-data "assets:assets" --add-data ".env:." main.py
```

**Important Note on Database**:
This game uses MongoDB. The executable bundles the connection string from your `.env` file.
- If you use a **cloud database** (e.g., MongoDB Atlas), the executable will work on any machine with internet access.
- If you use a **local database** (localhost), the executable will only work on machines that have a MongoDB server running locally.

## Project Structure

The project is organized into a modular structure:
- `src/core`: Core game loop and state management.
- `src/entities`: Game objects (Spaceship, Asteroid, etc.).
- `src/scenes`: Game scenes (Welcome, Game, GameOver).
- `src/ui`: UI components.
- `src/utils`: Helper functions and asset management.
- `src/database`: Database connection logic.

## Controls
- **Arrow Keys**: Move spaceship (left, right, up, down).
- **Space**: Shoot.
- **M**: Fire missile (when available).
- **P**: Pause/Unpause game.
- **Enter**: Start game / Submit initials.

## Screenshots
<img width="1599" height="928" alt="Screenshot 2025-11-25 143151" src="https://github.com/user-attachments/assets/6370c3c3-7fe0-49a2-bd91-adf47fbcee86" />
<img width="1595" height="926" alt="Screenshot 2025-11-25 143209" src="https://github.com/user-attachments/assets/53eb7c85-eb74-4843-8cd3-9690a775e796" />
<img width="1596" height="929" alt="Screenshot 2025-11-25 143443" src="https://github.com/user-attachments/assets/bc688336-acac-4f8f-ae45-b3a58246b0f0" />

## Gameplay
![game play](https://github.com/user-attachments/assets/07ebbafb-ad33-42cb-8b22-394664729632)

Enjoy the game! 🚀
