import pygame
from game_assets import load_assets
from screens import show_welcome_screen
from game_logic import game_loop
from utils import resource_path

# Initialize Pygame and assets
pygame.init()
pygame.mixer.init()

# Set the window title
pygame.display.set_caption("Space Travel | Naro Chan Dev")

# Load and set the window icon
icon = pygame.image.load(resource_path('space_ship.png'))
pygame.display.set_icon(icon)


def main():
    # Load all assets
    assets = load_assets()

    # Show welcome screen
    show_welcome_screen(assets)

    # Start the game loop
    game_loop(assets)


if __name__ == "__main__":
    main()
