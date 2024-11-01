import pygame
from utils import resource_path


def load_assets():
    screen_width, screen_height = 800, 600
    assets = {}

    # Constants
    assets['SCREEN_WIDTH'] = screen_width
    assets['SCREEN_HEIGHT'] = screen_height
    assets['SPACESHIP_WIDTH'] = 50
    assets['SPACESHIP_HEIGHT'] = 50
    assets['ASTEROID_WIDTH'] = 50
    assets['ASTEROID_HEIGHT'] = 50
    assets['BULLET_WIDTH'] = 5
    assets['BULLET_HEIGHT'] = 10

    # Colors
    assets['WHITE'] = (255, 255, 255)
    assets['BLACK'] = (0, 0, 0)
    assets['YELLOW'] = (255, 255, 150)
    assets['RED'] = (200, 0, 50)
    assets['GREEN'] = (0, 200, 50)
    assets['BLUE'] = (50, 50, 200)

    # Load logo image
    assets['logo_img'] = pygame.image.load(resource_path('naro_chan_logo.png'))
    assets['logo_img'] = pygame.transform.scale(assets['logo_img'], (400, 300))  # Scale logo

    # Load spaceship image
    assets['spaceship_img'] = pygame.image.load(resource_path('space_ship.png'))
    assets['spaceship_img'] = pygame.transform.scale(assets['spaceship_img'], (80, 70))

    # Load asteroid images
    asteroid_files = ['asteroid_1.png', 'asteroid_2.png', 'asteroid_3.png']
    assets['asteroid_images'] = [
        pygame.transform.scale(pygame.image.load(resource_path(f)), (50, 50)) for f in asteroid_files
    ]

    # Load background images
    background_files = [
        'background-1.jpg', 'background-2.jpg', 'background-4.jpg', 'background-5.jpg', 'background-6.jpg',
        'background-7.jpg'
    ]
    assets['background_images'] = [
        pygame.transform.scale(pygame.image.load(resource_path(f)),
                               (screen_width, screen_height)) for f in background_files
    ]

    # Load sounds
    assets['fire_sound'] = pygame.mixer.Sound(resource_path('fire.aiff'))
    assets['asteroid_hit_sound'] = pygame.mixer.Sound(resource_path('asteroid_hit.wav'))
    assets['crash_sound'] = pygame.mixer.Sound(resource_path('crash.wav'))
    assets['end_bomb_sound'] = pygame.mixer.Sound(resource_path('end_bomb.wav'))

    # Load music
    pygame.mixer.music.load(resource_path('drive-breakbeat.mp3'))
    pygame.mixer.music.play(-1)

    return assets


def draw_health_bar(screen, lives, max_lives, assets):
    bar_width = 20
    bar_spacing = 5
    x_offset = 10
    y_offset = 10

    for i in range(max_lives):
        color = assets['RED'] if i < lives else assets['BLACK']
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(x_offset + i * (bar_width + bar_spacing), y_offset, bar_width, 15),
            border_radius=5
        )


def draw_bullet_bar(screen, available_bullets, max_bullets, assets):
    bar_width = 15
    bar_spacing = 5
    x_offset = 10
    y_offset = 35

    for i in range(max_bullets):
        color = assets['BLUE'] if i < available_bullets else assets['BLACK']
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(x_offset + i * (bar_width + bar_spacing), y_offset, bar_width, 10),
            border_radius=3
        )


def draw_score_display(screen, score, assets):
    font = pygame.font.SysFont(None, 36)
    shadow_color = (50, 50, 50)  # Dark color for shadow
    score_text = font.render(f"Score: {score}", True, assets['WHITE'])
    # score_shadow = font.render(f"Score: {score}", True, shadow_color)

    # Rounded box background for score
    # score_rect = pygame.Rect(assets['SCREEN_WIDTH'] - 160, 10, 150, 30)
    # pygame.draw.rect(screen, assets['BLACK'], score_rect, border_radius=8)

    # Draw shadow (slightly offset)
    # screen.blit(score_shadow, (assets['SCREEN_WIDTH'] - 148, 17))  # Shadow offset by (2, 2)

    # Draw main score text
    screen.blit(score_text, (assets['SCREEN_WIDTH'] - 150, 15))


def draw_button(screen, text, x, y, width, height, font_size=36, idle_color=(100, 100, 100),
                hover_color=(150, 150, 150), text_color=(255, 255, 255)):
    """
    Draws a button with hover effects and rounded corners. Draws directly on the passed 'screen'.
    """
    font = pygame.font.SysFont(None, font_size)
    mouse_pos = pygame.mouse.get_pos()

    # Detect if mouse is hovering over the button
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        color = hover_color
    else:
        color = idle_color

    # Draw button background with rounded corners
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect, border_radius=10)  # Use rounded corners

    # Draw text on the button
    text_render = font.render(text, True, text_color)
    screen.blit(text_render, (x + (width - text_render.get_width()) // 2, y + (height - text_render.get_height()) // 2))

    return button_rect
