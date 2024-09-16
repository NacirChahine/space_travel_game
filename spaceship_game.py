import pygame
import random
import os
import struct

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
ASTEROID_WIDTH, ASTEROID_HEIGHT = 50, 50
POWERUP_WIDTH, POWERUP_HEIGHT = 30, 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
POWERUP_LIFE = 1
POWERUP_SPEED = 2
HIGHSCORE_FILE = 'highscore.dat'

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Game")

# Improved spaceship (triangular shape)
spaceship_img = pygame.Surface((SPACESHIP_WIDTH, SPACESHIP_HEIGHT), pygame.SRCALPHA)
pygame.draw.polygon(spaceship_img, (0, 128, 255), [(SPACESHIP_WIDTH // 2, 0), (0, SPACESHIP_HEIGHT), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)])

# Improved asteroid (circular shape)
asteroid_img = pygame.Surface((ASTEROID_WIDTH, ASTEROID_HEIGHT), pygame.SRCALPHA)
pygame.draw.circle(asteroid_img, (128, 128, 128), (ASTEROID_WIDTH // 2, ASTEROID_HEIGHT // 2), ASTEROID_WIDTH // 2)

# Placeholder power-up images (improved shapes)
powerup_img_life = pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT))
powerup_img_life.fill((0, 255, 0))

powerup_img_speed = pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT))
powerup_img_speed.fill((255, 0, 0))

# Game clock
clock = pygame.time.Clock()

# List of random space facts
space_facts = [
    "Space is completely silent.",
    "The hottest planet in our solar system is Venus.",
    "A full NASA space suit costs $12 million.",
    "Neutron stars can spin 600 times per second.",
    "One day on Venus is longer than one year on Earth.",
    "There are more stars in the universe than grains of sand on Earth.",
    "The Sun accounts for 99.86% of the mass in the Solar System.",
    "There could be 500 million planets capable of supporting life in our galaxy.",
]

# Load high score from binary file
def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, 'rb') as file:
            return struct.unpack('I', file.read())[0]
    return 0

# Save high score to binary file
def save_high_score(score):
    with open(HIGHSCORE_FILE, 'wb') as file:
        file.write(struct.pack('I', score))

# Function to draw the spaceship
def draw_spaceship(x, y):
    screen.blit(spaceship_img, (x, y))

# Function to draw the asteroid
def draw_asteroid(x, y):
    screen.blit(asteroid_img, (x, y))

# Function to draw the power-up
def draw_powerup(x, y, powerup_type):
    if powerup_type == POWERUP_LIFE:
        screen.blit(powerup_img_life, (x, y))
    elif powerup_type == POWERUP_SPEED:
        screen.blit(powerup_img_speed, (x, y))

# Function to draw multiple asteroids
def draw_asteroids(asteroids):
    for asteroid in asteroids:
        draw_asteroid(asteroid['x'], asteroid['y'])

# Display lives on screen
def draw_lives(lives):
    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 50))

# Display the game over screen with space facts
def show_game_over_screen(score, high_score):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    text = font.render("Game Over!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2))

    # Pick a random space fact
    random_fact = random.choice(space_facts)
    fact_font = pygame.font.SysFont(None, 30)
    fact_text = fact_font.render(f"Space Fact: {random_fact}", True, WHITE)
    screen.blit(fact_text, (SCREEN_WIDTH // 2 - fact_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

    pygame.display.flip()
    pygame.time.delay(5000)  # Show the screen for 5 seconds before closing

# Display the victory screen
def show_end_screen(high_score):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    text = font.render("Spaceship Arrived at Destination!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    astronaut_text = font.render("Astronaut Safe!", True, WHITE)
    screen.blit(astronaut_text, (SCREEN_WIDTH // 2 - astronaut_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

    pygame.display.flip()
    pygame.time.delay(5000)  # Show the screen for 5 seconds before closing

# Display the pause screen
def show_pause_screen():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    text = font.render("Game Paused", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    resume_text = font.render("Press 'P' to Resume", True, WHITE)
    screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()

# Game loop
def game_loop():
    spaceship_x = (SCREEN_WIDTH - SPACESHIP_WIDTH) // 2
    spaceship_y = SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10
    spaceship_speed = 5
    extra_speed = 0

    num_asteroids = 3
    asteroids = [{'x': random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH), 'y': -ASTEROID_HEIGHT, 'speed': 5} for _ in range(num_asteroids)]
    lives = 3
    score = 0
    level = 1
    paused = False
    max_score_to_win = 150
    game_over = False
    player_won = False

    high_score = load_high_score()

    while not game_over:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused

        # Pause the game when 'P' is pressed
        if paused:
            show_pause_screen()
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        paused = False
                clock.tick(5)
            continue

        # Spaceship movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_x > 0:
            spaceship_x -= spaceship_speed + extra_speed
        if keys[pygame.K_RIGHT] and spaceship_x < SCREEN_WIDTH - SPACESHIP_WIDTH:
            spaceship_x += spaceship_speed + extra_speed

        # Asteroid movement
        for asteroid in asteroids:
            asteroid['y'] += asteroid['speed']
            if asteroid['y'] > SCREEN_HEIGHT:
                asteroid['y'] = -ASTEROID_HEIGHT
                asteroid['x'] = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
                score += 1
                if score % 5 == 0:
                    level += 1
                    for ast in asteroids:
                        ast['speed'] += 1

        # Check for collision
        for asteroid in asteroids:
            if (
                spaceship_y < asteroid['y'] + ASTEROID_HEIGHT and
                spaceship_y + SPACESHIP_HEIGHT > asteroid['y'] and
                spaceship_x < asteroid['x'] + ASTEROID_WIDTH and
                spaceship_x + SPACESHIP_WIDTH > asteroid['x']
            ):
                lives -= 1
                asteroid['y'] = -ASTEROID_HEIGHT
                asteroid['x'] = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
                if lives == 0:
                    game_over = True

        # Check if the player has won
        if score >= max_score_to_win:
            player_won = True
            game_over = True

        # Fill the screen with black
        screen.fill(BLACK)

        # Draw spaceship, asteroids, and power-ups
        draw_spaceship(spaceship_x, spaceship_y)
        draw_asteroids(asteroids)

        # Display the score, level, and lives
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
        draw_lives(lives)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Update high score and show appropriate end screen
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    if player_won:
        show_end_screen(high_score)
    else:
        show_game_over_screen(score, high_score)

    # End the game
    pygame.quit()

# Start the game
if __name__ == "__main__":
    game_loop()
