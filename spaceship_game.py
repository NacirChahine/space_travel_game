import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
ASTEROID_WIDTH, ASTEROID_HEIGHT = 50, 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Game")

# Load spaceship image
spaceship_img = pygame.Surface((SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
spaceship_img.fill((0, 128, 255))  # Placeholder blue spaceship

# Asteroid settings
asteroid_img = pygame.Surface((ASTEROID_WIDTH, ASTEROID_HEIGHT))
asteroid_img.fill((128, 128, 128))  # Placeholder gray asteroid

# Game clock
clock = pygame.time.Clock()

# Function to draw the spaceship
def draw_spaceship(x, y):
    screen.blit(spaceship_img, (x, y))

# Function to draw the asteroid
def draw_asteroid(x, y):
    screen.blit(asteroid_img, (x, y))

# Game loop
def game_loop():
    spaceship_x = (SCREEN_WIDTH - SPACESHIP_WIDTH) // 2
    spaceship_y = SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10
    spaceship_speed = 5

    asteroid_x = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
    asteroid_y = -ASTEROID_HEIGHT
    asteroid_speed = 5

    score = 0
    game_over = False

    while not game_over:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Spaceship movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_x > 0:
            spaceship_x -= spaceship_speed
        if keys[pygame.K_RIGHT] and spaceship_x < SCREEN_WIDTH - SPACESHIP_WIDTH:
            spaceship_x += spaceship_speed

        # Asteroid movement
        asteroid_y += asteroid_speed
        if asteroid_y > SCREEN_HEIGHT:
            asteroid_y = -ASTEROID_HEIGHT
            asteroid_x = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
            score += 1

        # Check for collision
        if (
            spaceship_y < asteroid_y + ASTEROID_HEIGHT and
            spaceship_y + SPACESHIP_HEIGHT > asteroid_y and
            spaceship_x < asteroid_x + ASTEROID_WIDTH and
            spaceship_x + SPACESHIP_WIDTH > asteroid_x
        ):
            game_over = True

        # Fill the screen with black
        screen.fill(BLACK)

        # Draw spaceship and asteroid
        draw_spaceship(spaceship_x, spaceship_y)
        draw_asteroid(asteroid_x, asteroid_y)

        # Display the score
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # End the game
    pygame.quit()

# Start the game
if __name__ == "__main__":
    game_loop()
