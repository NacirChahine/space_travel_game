import pygame
import random
import os
import sys
import struct

# Initialize Pygame and the mixer for sound
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
ASTEROID_WIDTH, ASTEROID_HEIGHT = 50, 50
POWERUP_WIDTH, POWERUP_HEIGHT = 30, 30
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
POWERUP_LIFE = 1
POWERUP_SPEED = 2
POWERUP_POINTS = 3
HIGHSCORE_FILE = 'highscore.dat'

# Helper function to get the resource path (needed when bundled as a one-file .exe)
def resource_path(relative_path):
    """ Get the absolute path to a resource. Works for development and PyInstaller packaging. """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load spaceship image
spaceship_img = pygame.image.load(resource_path('space_ship.png'))
spaceship_img = pygame.transform.scale(spaceship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Load asteroid images and randomly assign one during each asteroid spawn
asteroid_images = [
    pygame.image.load(resource_path('asteroid_1.png')),
    pygame.image.load(resource_path('asteroid_2.png')),
    pygame.image.load(resource_path('asteroid_3.png'))
]
asteroid_images = [pygame.transform.scale(img, (ASTEROID_WIDTH, ASTEROID_HEIGHT)) for img in asteroid_images]

# Load power-up images
powerup_images = {
    POWERUP_LIFE: pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT)),
    POWERUP_SPEED: pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT)),
    POWERUP_POINTS: pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT))
}
powerup_images[POWERUP_LIFE].fill((0, 255, 0))  # Green power-up for life
powerup_images[POWERUP_SPEED].fill((255, 255, 0))  # Yellow power-up for speed
powerup_images[POWERUP_POINTS].fill((255, 0, 0))  # Red power-up for extra points

# Load background images for different levels
background_images = [
    pygame.image.load(resource_path('background-1.jpg')),
    pygame.image.load(resource_path('background-2.jpg')),
    pygame.image.load(resource_path('background-4.jpg')),
    pygame.image.load(resource_path('background-5.jpg')),
    pygame.image.load(resource_path('background-6.jpg')),
    pygame.image.load(resource_path('background-7.jpg'))
]
background_images = [pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)) for img in background_images]

# Load and loop background music
pygame.mixer.music.load(resource_path('drive-breakbeat.mp3'))
pygame.mixer.music.play(-1)  # Loop indefinitely

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Game")

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
def draw_asteroid(x, y, img):
    screen.blit(img, (x, y))

# Function to draw multiple asteroids
def draw_asteroids(asteroids):
    for asteroid in asteroids:
        draw_asteroid(asteroid['x'], asteroid['y'], asteroid['img'])

# Function to draw power-ups
def draw_powerups(powerups):
    for powerup in powerups:
        screen.blit(powerup['img'], (powerup['x'], powerup['y']))

# Function to draw bullets
def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet['x'], bullet['y'], BULLET_WIDTH, BULLET_HEIGHT))

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
    shield_active = False
    shield_duration = 300  # Shield lasts for 5 seconds (300 frames at 60fps)

    num_asteroids = 3
    asteroids = [{'x': random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH), 'y': -ASTEROID_HEIGHT, 'speed': 5, 'img': random.choice(asteroid_images)} for _ in range(num_asteroids)]
    powerups = []
    bullets = []
    bullet_speed = 7
    lives = 3
    score = 0
    level = 1
    max_score_to_win = 500
    game_over = False
    player_won = False
    paused = False

    high_score = load_high_score()

    # Game loop
    while not game_over:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        show_pause_screen()
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                if event.key == pygame.K_SPACE and not paused:
                    bullets.append({'x': spaceship_x + SPACESHIP_WIDTH // 2 - BULLET_WIDTH // 2, 'y': spaceship_y})

        if paused:
            continue

        # Spaceship movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_x > 0:
            spaceship_x -= spaceship_speed + extra_speed
        if keys[pygame.K_RIGHT] and spaceship_x < SCREEN_WIDTH - SPACESHIP_WIDTH:
            spaceship_x += spaceship_speed + extra_speed

        # Bullet movement
        bullets = [{'x': b['x'], 'y': b['y'] - bullet_speed} for b in bullets if b['y'] > 0]

        # Asteroid movement
        for asteroid in asteroids:
            asteroid['y'] += asteroid['speed']
            if asteroid['y'] > SCREEN_HEIGHT:
                asteroid['y'] = -ASTEROID_HEIGHT
                asteroid['x'] = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
                score += 1
                if score % 5 == 0:
                    level += 1
                    asteroid['speed'] += 1

        # Power-up movement
        for powerup in powerups:
            powerup['y'] += 3

        # Collision detection between spaceship and asteroids
        for asteroid in asteroids:
            if (
                spaceship_y < asteroid['y'] + ASTEROID_HEIGHT and
                spaceship_y + SPACESHIP_HEIGHT > asteroid['y'] and
                spaceship_x < asteroid['x'] + ASTEROID_WIDTH and
                spaceship_x + SPACESHIP_WIDTH > asteroid['x']
            ):
                if not shield_active:
                    lives -= 1
                asteroid['y'] = -ASTEROID_HEIGHT
                asteroid['x'] = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
                if lives == 0:
                    game_over = True

        # Collision detection between bullets and asteroids
        for bullet in bullets:
            for asteroid in asteroids:
                if (
                    bullet['y'] < asteroid['y'] + ASTEROID_HEIGHT and
                    bullet['y'] + BULLET_HEIGHT > asteroid['y'] and
                    bullet['x'] < asteroid['x'] + ASTEROID_WIDTH and
                    bullet['x'] + BULLET_WIDTH > asteroid['x']
                ):
                    asteroid['y'] = -ASTEROID_HEIGHT
                    asteroid['x'] = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
                    bullets.remove(bullet)
                    score += 1
                    break

        # Collision detection between spaceship and power-ups
        for powerup in powerups:
            if (
                spaceship_y < powerup['y'] + POWERUP_HEIGHT and
                spaceship_y + SPACESHIP_HEIGHT > powerup['y'] and
                spaceship_x < powerup['x'] + POWERUP_WIDTH and
                spaceship_x + SPACESHIP_WIDTH > powerup['x']
            ):
                if powerup['type'] == POWERUP_LIFE:
                    lives += 1
                elif powerup['type'] == POWERUP_SPEED:
                    extra_speed = 3  # Speed boost
                    shield_duration = 300
                elif powerup['type'] == POWERUP_POINTS:
                    score += 10
                powerups.remove(powerup)

        # Check if player won
        if score >= max_score_to_win:
            player_won = True
            game_over = True

        # Update the background based on level
        current_background = background_images[(level - 1) % len(background_images)]
        screen.blit(current_background, (0, 0))

        # Draw objects
        draw_spaceship(spaceship_x, spaceship_y)
        draw_asteroids(asteroids)
        draw_bullets(bullets)
        draw_powerups(powerups)

        # Display score, level, and lives
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
        draw_lives(lives)

        pygame.display.flip()
        clock.tick(60)

    # High score update
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    if player_won:
        show_end_screen(high_score)
    else:
        show_game_over_screen(score, high_score)

    pygame.quit()

# Start the game
if __name__ == "__main__":
    game_loop()
