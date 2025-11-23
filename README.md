# Space Travel Game

A retro-style space shooter game built with Pygame.

## Features
- **Spaceship Control**: Navigate your ship to avoid obstacles.
- **Shooting**: Blast asteroids with your laser.
- **Power-ups**: Collect health, ammo, and upgrade power-ups.
- **Boss Battles**: Face multiple bosses simultaneously with varying difficulty levels.
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

## Project Structure

The project is organized into a modular structure:
- `src/core`: Core game loop and state management.
- `src/entities`: Game objects (Spaceship, Asteroid, etc.).
- `src/scenes`: Game scenes (Welcome, Game, GameOver).
- `src/ui`: UI components.
- `src/utils`: Helper functions and asset management.
- `src/database`: Database connection logic.

## Controls
- **Arrow Keys**: Move spaceship.
- **Space**: Shoot.
- **P**: Pause/Unpause game.
- **Enter**: Start game / Submit initials.

## Screenshots
<img width="798" height="626" alt="space_travel_game_img_1" src="https://github.com/user-attachments/assets/16fc39b4-ace3-49ec-989e-82d9ec793bdb" />
<img width="797" height="625" alt="space_travel_game_img_2" src="https://github.com/user-attachments/assets/dcfbd159-6a56-4b3e-bad5-99bfb15b6dc2" />

## Gameplay
![Recording 2025-11-23 231412](https://github.com/user-attachments/assets/aaf259ea-efcb-4a8d-a41a-e26cb8a555dc)


Enjoy the game! 🚀
