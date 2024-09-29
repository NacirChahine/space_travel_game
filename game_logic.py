import sys
import pygame
import random
from screens import show_end_screen, get_player_initials
from database import save_high_score, load_top_scores


def game_loop(assets):
    screen = pygame.display.set_mode((assets['SCREEN_WIDTH'], assets['SCREEN_HEIGHT']))
    clock = pygame.time.Clock()

    # Initial spaceship position
    x, y = assets['SCREEN_WIDTH'] // 2, assets['SCREEN_HEIGHT'] - assets['SPACESHIP_HEIGHT'] - 10
    x_change = 0  # Movement change
    left_key, right_key = False, False  # Track key states for left and right movement
    bullets = []
    asteroids = []
    score = 0
    lives = 3
    asteroid_speed = 5
    background_index = 0

    asteroid_event = pygame.USEREVENT + 1
    pygame.time.set_timer(asteroid_event, 1000)

    while True:
        screen.blit(assets['background_images'][background_index], (0, 0))

        # Handle events
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
                    assets['fire_sound'].play()
                    bullets.append({'x': x + assets['SPACESHIP_WIDTH'] // 2 - assets['BULLET_WIDTH'] // 2, 'y': y})

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_key = False
                if event.key == pygame.K_RIGHT:
                    right_key = False

            if event.type == asteroid_event:
                asteroids.append({
                    'x': random.randint(0, assets['SCREEN_WIDTH'] - assets['ASTEROID_WIDTH']),
                    'y': 0,
                    'img': random.choice(assets['asteroid_images'])
                })

        # Update spaceship movement based on key states
        if right_key & left_key:
            x_change = 0  # No movement
        elif left_key:
            x_change = -5  # Move left
        elif right_key:
            x_change = 5  # Move right
        else:
            x_change = 0  # No movement

        # Update spaceship position
        x += x_change
        if x < 0:
            x = 0  # Prevent moving off the left side of the screen
        elif x > assets['SCREEN_WIDTH'] - assets['SPACESHIP_WIDTH']:
            x = assets['SCREEN_WIDTH'] - assets['SPACESHIP_WIDTH']  # Prevent moving off the right side

        # Bullet movement
        bullets = [{'x': b['x'], 'y': b['y'] - 5} for b in bullets if b['y'] > 0]

        # Asteroid movement and collision detection
        for asteroid in asteroids:
            asteroid['y'] += asteroid_speed
            if asteroid['y'] > assets['SCREEN_HEIGHT']:
                asteroids.remove(asteroid)
                score += 1
            if spaceship_hits_asteroid(x, y, asteroid):
                assets['crash_sound'].play()
                asteroids.remove(asteroid)
                lives -= 1
                if lives == 0:
                    # Load the top 5 scores
                    top_scores = load_top_scores()

                    # Check if the player's score qualifies for the top 5
                    if len(top_scores) < 5 or score > top_scores[-1]['high_score']:
                        # Prompt the player to enter initials if they qualify for the top 5
                        player_initials = get_player_initials(assets)
                        save_high_score(score, player_initials)  # Save the new high score with initials

                    # Show the end screen with the high score and top 5
                    action = show_end_screen(score, assets)

                    if action == "replay":
                        game_loop(assets)  # Restart game
                    else:
                        pygame.quit()
                        sys.exit()

        # Bullet-Asteroid collision
        for bullet in bullets:
            for asteroid in asteroids:
                if bullet_hits_asteroid(bullet, asteroid):
                    assets['asteroid_hit_sound'].play()
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 10
                    break

        # Draw spaceship, asteroids, and bullets
        screen.blit(assets['spaceship_img'], (x, y))
        for bullet in bullets:
            pygame.draw.rect(screen, assets['WHITE'], (bullet['x'], bullet['y'], assets['BULLET_WIDTH'], assets['BULLET_HEIGHT']))
        for asteroid in asteroids:
            screen.blit(asteroid['img'], (asteroid['x'], asteroid['y']))

        # Display lives and score
        font = pygame.font.SysFont(None, 36)
        lives_text = font.render(f"Lives: {lives}", True, assets['WHITE'])
        screen.blit(lives_text, (10, 10))
        score_text = font.render(f"Score: {score}", True, assets['WHITE'])
        screen.blit(score_text, (assets['SCREEN_WIDTH'] - 150, 10))

        pygame.display.update()
        clock.tick(60)  # Limit the frame rate to 60 FPS


# Collision detection functions
def spaceship_hits_asteroid(x, y, asteroid):
    spaceship_rect = pygame.Rect(x, y, 50, 50)
    asteroid_rect = pygame.Rect(asteroid['x'], asteroid['y'], 50, 50)
    return spaceship_rect.colliderect(asteroid_rect)


def bullet_hits_asteroid(bullet, asteroid):
    bullet_rect = pygame.Rect(bullet['x'], bullet['y'], 5, 10)
    asteroid_rect = pygame.Rect(asteroid['x'], asteroid['y'], 50, 50)
    return bullet_rect.colliderect(asteroid_rect)
