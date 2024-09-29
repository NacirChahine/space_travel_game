# Spaceship Game 🚀

A simple 2D spaceship game built with Python and Pygame. The player controls a spaceship to avoid falling asteroids, progressing through increasingly challenging levels. Each level increases the speed and number of asteroids.

## Features
- Multiple Asteroids: As the player progresses, the number of asteroids increases, adding to the challenge.
- Weapon System: Allow the player to shoot bullets at the asteroids.
- Lives System: The player starts with 3 lives. Colliding with an asteroid reduces lives. The game ends when all lives are lost.

## How to Play
- Use the **Left** and **Right Arrow Keys** to move the spaceship.
- Use the **Space Key** to shoot asteroids.
- Avoid getting hit by the asteroids.
- Survive as long as you can and score higher!

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NacirChahine/spaceship-game.git
   cd spaceship-game
   ```
2. Install the required dependencies:
   ```bash
    pip install -r requirements.txt
   ```
3. Copy .env.example to .env:
   ```bash
    cp .env.example .env
   ```
4. Update the .env file:

   Open the .env file and replace the placeholder MONGODB_URI with your real MongoDB connection URI.
5. Run the game:
   ```bash
    python main.py
   ```
## Requirements
- Python 3.x
- Pygame
- pymongo
- python-dotenv

## Screenshots
![Screenshot 1](https://github.com/user-attachments/assets/ebfa4677-dc23-46ca-9d6d-ba52535eea75)
![Screenshot 2](https://github.com/user-attachments/assets/b77670cd-7397-44d2-994c-130f80eaa9b6)


Enjoy the game! 🚀
