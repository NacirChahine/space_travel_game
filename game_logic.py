import sys
import pygame
import random
from screens import show_end_screen, get_player_initials
from database import save_high_score, load_top_scores
from game_assets import draw_health_bar, draw_bullet_bar, draw_score_display


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
    max_lives = 5
    max_bullets = 10  # Define max bullets for the bar
    asteroid_speed = 5
    background_index = 0

    # Player starts with 5 bullets
    available_bullets = 5

    asteroid_event = pygame.USEREVENT + 1
    pygame.time.set_timer(asteroid_event, 1000)

    powerup_event = pygame.USEREVENT + 2
    pygame.time.set_timer(powerup_event, 5000)  # Spawn power-up every 5 seconds

    powerups = []

    while True:
        # Render the current background
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
                if event.key == pygame.K_SPACE and available_bullets > 0:
                    # Fire bullet if the player has bullets left
                    assets['fire_sound'].play()
                    bullets.append({'x': x + assets['SPACESHIP_WIDTH'] // 2 - assets['BULLET_WIDTH'] // 2, 'y': y})
                    available_bullets -= 1  # Decrease bullet count when fired

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

            if event.type == powerup_event:
                powerup_type = random.choice(['health', 'ammo'])
                img = assets['health_powerup_img'] if powerup_type == 'health' else assets['ammo_powerup_img']
                powerups.append({
                    'x': random.randint(0, assets['SCREEN_WIDTH'] - assets['POWERUP_WIDTH']),
                    'y': -assets['POWERUP_HEIGHT'],
                    'type': powerup_type,
                    'img': img
                })

        # Update spaceship movement based on key states
        if right_key and left_key:
            x_change = 0  # No movement
        elif left_key:
            x_change = -5  # Move left
        elif right_key:
            x_change = 5  # Move right
        else:
            x_change = 0  # No movement

        # Update spaceship position
        x += x_change
        x = max(0, min(x, assets['SCREEN_WIDTH'] - assets['SPACESHIP_WIDTH']))

        # Bullet movement
        bullets = [{'x': b['x'], 'y': b['y'] - 5} for b in bullets if b['y'] > 0]

        # Asteroid movement and collision
        for asteroid in asteroids[:]:
            asteroid['y'] += asteroid_speed
            if asteroid['y'] > assets['SCREEN_HEIGHT']:
                asteroids.remove(asteroid)
                score += 1  # Increment score when asteroid passes

            if spaceship_hits_asteroid(x, y, asteroid):
                assets['crash_sound'].play()
                asteroids.remove(asteroid)
                lives -= 1
                if lives == 0:
                    # Load the top 5 scores (returns empty list if database unavailable)
                    top_scores = load_top_scores()

                    # Check if the player's score qualifies for the top 5
                    if len(top_scores) < 5 or score > top_scores[-1]['high_score']:
                        # Prompt the player to enter initials if they qualify for the top 5
                        player_initials = get_player_initials(assets)
                        # Try to save the high score (gracefully handles database failures)
                        save_high_score(score, player_initials)

                    # Show the end screen with the high score and top 5
                    action = show_end_screen(score, assets)

                    if action == "replay":
                        game_loop(assets)  # Restart game
                    else:
                        pygame.quit()
                        sys.exit()

        # Bullet-Asteroid collision
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if bullet_hits_asteroid(bullet, asteroid):
                    assets['asteroid_hit_sound'].play()
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 10  # Increment score for shooting an asteroid
                    available_bullets += 1  # Add a bullet back to the player's inventory
                    break

        # Power-up movement and collision
        for powerup in powerups[:]:
            powerup['y'] += 3  # Power-ups move slower than asteroids
            if powerup['y'] > assets['SCREEN_HEIGHT']:
                powerups.remove(powerup)
            
            elif spaceship_hits_powerup(x, y, powerup, assets):
                if powerup['type'] == 'health':
                    if lives < max_lives:
                        lives += 1
                elif powerup['type'] == 'ammo':
                    if available_bullets < max_bullets:
                        available_bullets = min(max_bullets, available_bullets + 3)
                powerups.remove(powerup)

        # Level up and background/asteroid speed-up logic
        if score // 50 > background_index:
            background_index = min(len(assets['background_images']) - 1, background_index + 1)
            asteroid_speed = min(15, asteroid_speed + 1)

        # Draw spaceship, asteroids, and bullets
        screen.blit(assets['spaceship_img'], (x, y))
        for bullet in bullets:
            pygame.draw.rect(screen, assets['WHITE'], (bullet['x'], bullet['y'], assets['BULLET_WIDTH'], assets['BULLET_HEIGHT']))
        for asteroid in asteroids:
            screen.blit(asteroid['img'], (asteroid['x'], asteroid['y']))
        for powerup in powerups:
            screen.blit(powerup['img'], (powerup['x'], powerup['y']))

        # Display custom health, bullet bars, and score display
        draw_health_bar(screen, lives, max_lives, assets)
        draw_bullet_bar(screen, available_bullets, max_bullets, assets)
        draw_score_display(screen, score, assets)

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


def spaceship_hits_powerup(x, y, powerup, assets):
    spaceship_rect = pygame.Rect(x, y, assets['SPACESHIP_WIDTH'], assets['SPACESHIP_HEIGHT'])
    powerup_rect = pygame.Rect(powerup['x'], powerup['y'], assets['POWERUP_WIDTH'], assets['POWERUP_HEIGHT'])
    return spaceship_rect.colliderect(powerup_rect)
