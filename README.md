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
![Screenshot 1](https://github.com/user-attachments/assets/ebfa4677-dc23-46ca-9d6d-ba52535eea75)
![Screenshot 2](https://github.com/user-attachments/assets/b77670cd-7397-44d2-994c-130f80eaa9b6)

## Gameplay
![space_travel_gameplay](https://github.com/user-attachments/assets/b9dfaa6b-3107-43ed-878c-4b9d96d7aca0)


Enjoy the game! 🚀
