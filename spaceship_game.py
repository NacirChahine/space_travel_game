import pygame
import random
import os
import sys
import struct

# Initialize Pygame and the mixer for sound
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
ASTEROID_WIDTH, ASTEROID_HEIGHT = 50, 50
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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

# Load sound effects
fire_sound = pygame.mixer.Sound(resource_path('fire.aiff'))
asteroid_hit_sound = pygame.mixer.Sound(resource_path('asteroid_hit.wav'))
crash_sound = pygame.mixer.Sound(resource_path('crash.wav'))
end_bomb_sound = pygame.mixer.Sound(resource_path('end_bomb.wav'))

# Load logo image for welcome screen
logo_img = pygame.image.load(resource_path('naro_chan_logo.png'))
logo_img = pygame.transform.scale(logo_img, (400, 300))

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

# Function to draw buttons
def draw_button(text, x, y, width, height, font_size=36):
    font = pygame.font.SysFont(None, font_size)
    text_render = font.render(text, True, WHITE)
    pygame.draw.rect(screen, BLACK, [x, y, width, height])
    screen.blit(text_render, (x + (width - text_render.get_width()) // 2, y + (height - text_render.get_height()) // 2))
    return pygame.Rect(x, y, width, height)

# Function to show the welcome screen
def show_welcome_screen():
    random_fact = random.choice(space_facts)
    fact_font = pygame.font.SysFont(None, 30)
    
    while True:
        screen.fill(BLACK)
        screen.blit(logo_img, (SCREEN_WIDTH // 2 - logo_img.get_width() // 2, 100))

        font = pygame.font.SysFont(None, 55)
        title_text = font.render("Welcome to the Spaceship Game!", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        fact_text = fact_font.render(f"Did you know? {random_fact}", True, WHITE)
        screen.blit(fact_text, (SCREEN_WIDTH // 2 - fact_text.get_width() // 2, 450))

        start_text = font.render("Press ENTER to Start", True, WHITE)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# Function to show the end screen with replay and exit buttons
def show_end_screen(score, high_score):
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 55)
        title_text = font.render("Game Over!", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150))

        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 200))

        # Play final explosion sound once when game over
        end_bomb_sound.play()

        # Draw buttons
        replay_button = draw_button("Replay", SCREEN_WIDTH // 2 - 100, 300, 200, 50)
        exit_button = draw_button("Exit", SCREEN_WIDTH // 2 - 100, 400, 200, 50)

        pygame.display.update()

        # Event handling for buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    return "replay"
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Function to check if bullet hits an asteroid
def bullet_hits_asteroid(bullet, asteroid):
    return pygame.Rect(bullet['x'], bullet['y'], BULLET_WIDTH, BULLET_HEIGHT).colliderect(
        pygame.Rect(asteroid['x'], asteroid['y'], ASTEROID_WIDTH, ASTEROID_HEIGHT))

# Function to check if spaceship hits an asteroid
def spaceship_hits_asteroid(x, y, asteroid):
    spaceship_rect = pygame.Rect(x, y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    asteroid_rect = pygame.Rect(asteroid['x'], asteroid['y'], ASTEROID_WIDTH, ASTEROID_HEIGHT)
    return spaceship_rect.colliderect(asteroid_rect)

# Game loop
def game_loop():
    x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10
    x_change = 0
    left_key, right_key = False, False  # Track key states
    asteroids = []
    bullets = []
    score = 0
    lives = 3
    high_score = load_high_score()
    asteroid_speed = 5  # Initial speed of asteroids
    background_index = 0

    asteroid_event = pygame.USEREVENT + 1
    pygame.time.set_timer(asteroid_event, 1000)  # Add a new asteroid every 1 second

    paused = False

    while True:
        screen.blit(background_images[background_index], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_key = True
                if event.key == pygame.K_RIGHT:
                    right_key = True
                if event.key == pygame.K_SPACE:
                    # Fire bullet
                    fire_sound.play()
                    bullets.append({'x': x + SPACESHIP_WIDTH // 2 - BULLET_WIDTH // 2, 'y': y})

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_key = False
                if event.key == pygame.K_RIGHT:
                    right_key = False

            if event.type == asteroid_event:
                # Add new asteroid at random x position
                asteroids.append({'x': random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH), 'y': 0, 'img': random.choice(asteroid_images)})

        # Smooth spaceship movement logic
        if left_key:
            x_change = -5
        elif right_key:
            x_change = 5
        else:
            x_change = 0

        # Update spaceship position
        x += x_change
        if x < 0:
            x = 0
        elif x > SCREEN_WIDTH - SPACESHIP_WIDTH:
            x = SCREEN_WIDTH - SPACESHIP_WIDTH

        # Update bullet positions
        bullets = [{'x': b['x'], 'y': b['y'] - 5} for b in bullets if b['y'] > 0]

        # Update asteroid positions and check for collisions
        for asteroid in asteroids:
            asteroid['y'] += asteroid_speed
            if asteroid['y'] > SCREEN_HEIGHT:
                asteroids.remove(asteroid)
                score += 1  # Add score if asteroid goes off-screen
            if spaceship_hits_asteroid(x, y, asteroid):
                crash_sound.play()
                asteroids.remove(asteroid)
                lives -= 1
                if lives == 0:
                    # Save high score if needed
                    if score > high_score:
                        save_high_score(score)
                    # End the game if lives reach 0
                    action = show_end_screen(score, high_score)
                    if action == "replay":
                        game_loop()  # Restart game
                    else:
                        pygame.quit()
                        sys.exit()

        # Check for bullet collisions with asteroids
        for bullet in bullets:
            for asteroid in asteroids:
                if bullet_hits_asteroid(bullet, asteroid):
                    asteroid_hit_sound.play()
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 10  # Add score for hitting an asteroid
                    break

        # Level up every 50 points
        if score // 50 > background_index:
            background_index = min(len(background_images) - 1, background_index + 1)
            asteroid_speed += 1  # Increase asteroid speed every level

        # Drawing everything
        screen.blit(spaceship_img, (x, y))
        for asteroid in asteroids:
            screen.blit(asteroid['img'], (asteroid['x'], asteroid['y']))
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, (bullet['x'], bullet['y'], BULLET_WIDTH, BULLET_HEIGHT))

        font = pygame.font.SysFont(None, 36)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.update()
        clock.tick(60)

# Show welcome screen at start
show_welcome_screen()

# Start the game loop
game_loop()
