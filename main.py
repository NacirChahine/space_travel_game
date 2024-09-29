import pygame
from game_assets import load_assets
from screens import show_welcome_screen
from game_logic import game_loop

# Initialize Pygame and assets
pygame.init()
pygame.mixer.init()


def main():
    # Load all assets
    assets = load_assets()

    # Show welcome screen
    show_welcome_screen(assets)

    # Start the game loop
    game_loop(assets)


if __name__ == "__main__":
    main()
