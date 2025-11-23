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

    # Create Power-up Assets
    # Health Power-up (Red Cross)
    health_pu_size = 30
    health_pu_surf = pygame.Surface((health_pu_size, health_pu_size), pygame.SRCALPHA)
    pygame.draw.circle(health_pu_surf, (255, 255, 255), (health_pu_size // 2, health_pu_size // 2), health_pu_size // 2)
    pygame.draw.rect(health_pu_surf, assets['RED'], (health_pu_size // 2 - 4, 5, 8, 20))
    pygame.draw.rect(health_pu_surf, assets['RED'], (5, health_pu_size // 2 - 4, 20, 8))
    assets['health_powerup_img'] = health_pu_surf

    # Ammo Power-up (Yellow Bullet Icon)
    ammo_pu_size = 30
    ammo_pu_surf = pygame.Surface((ammo_pu_size, ammo_pu_size), pygame.SRCALPHA)
    pygame.draw.circle(ammo_pu_surf, (50, 50, 50), (ammo_pu_size // 2, ammo_pu_size // 2), ammo_pu_size // 2)
    # Draw simplified bullet shape
    pygame.draw.rect(ammo_pu_surf, assets['YELLOW'], (10, 8, 10, 14))
    pygame.draw.polygon(ammo_pu_surf, assets['YELLOW'], [(10, 8), (20, 8), (15, 2)])
    assets['ammo_powerup_img'] = ammo_pu_surf

    assets['POWERUP_WIDTH'] = 30
    assets['POWERUP_HEIGHT'] = 30

    # Missile Asset
    missile_surf = pygame.Surface((20, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(missile_surf, (255, 165, 0), (5, 0, 10, 30)) # Body
    pygame.draw.polygon(missile_surf, (200, 50, 50), [(5, 20), (0, 35), (5, 30)]) # Left Fin
    pygame.draw.polygon(missile_surf, (200, 50, 50), [(15, 20), (20, 35), (15, 30)]) # Right Fin
    assets['missile_img'] = missile_surf

    # Missile Powerup
    missile_pu_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(missile_pu_surf, (50, 50, 100), (15, 15), 15)
    # Draw 'M'
    font_pu = pygame.font.SysFont(None, 24)
    m_surf = font_pu.render("M", True, (255, 165, 0))
    missile_pu_surf.blit(m_surf, (15 - m_surf.get_width()//2, 15 - m_surf.get_height()//2))
    assets['missile_powerup_img'] = missile_pu_surf

    # Upgrade Powerup (Green Up Arrow)
    upgrade_pu_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(upgrade_pu_surf, (50, 200, 50), (15, 15), 15)
    pygame.draw.polygon(upgrade_pu_surf, (255, 255, 255), [(15, 5), (5, 20), (25, 20)])
    assets['upgrade_powerup_img'] = upgrade_pu_surf

    # Bullet Levels
    assets['bullet_levels'] = []
    colors = [(255, 255, 255), (255, 255, 200), (255, 200, 100), (255, 100, 100), (255, 50, 255)]
    for i in range(5):
        surf = pygame.Surface((5 + i, 10 + i*2), pygame.SRCALPHA)
        pygame.draw.rect(surf, colors[i], (0, 0, 5 + i, 10 + i*2), border_radius=2)
        assets['bullet_levels'].append(surf)
    # Add one more for safety if index is 5 (1-based level)
    assets['bullet_levels'].append(assets['bullet_levels'][-1])

    # Spaceship Levels (Reuse image but maybe add glow or something? For now just reuse)
    assets['spaceship_levels'] = [assets['spaceship_img']] * 6 # 0-5

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
