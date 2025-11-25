import pygame
from src.config import *

class HUD:
    def __init__(self, asset_manager):
        self.assets = asset_manager.assets
        self.font = pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.04))  # ~36px at 900p

    def draw_glass_bar(self, screen, x, y, width, height, fill_percent, color, label=None, numeric_text=None):
        # Background (Glass)
        bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, GLASS_BG, (0, 0, width, height), border_radius=10)
        pygame.draw.rect(bg_surface, GLASS_BORDER, (0, 0, width, height), 2, border_radius=10)
        screen.blit(bg_surface, (int(x), int(y)))

        # Fill
        if fill_percent > 0:
            fill_width = int((width - 10) * fill_percent)
            fill_rect = pygame.Rect(int(x + 5), int(y + 5), fill_width, height - 10)
            pygame.draw.rect(screen, color, fill_rect, border_radius=8)

        # Numeric text inside the bar
        if numeric_text:
            numeric_surf = self.font.render(numeric_text, True, WHITE)
            numeric_rect = numeric_surf.get_rect()
            # Position text inside the bar, centered both horizontally and vertically
            text_x = x + (width - numeric_rect.width) // 2
            text_y = y + (height - numeric_rect.height) // 2
            screen.blit(numeric_surf, (int(text_x), int(text_y)))

        # Label
        if label:
            label_surf = self.font.render(label, True, WHITE)
            screen.blit(label_surf, (int(x + 10), int(y - 25)))

    def draw(self, screen, lives, max_lives, available_bullets, max_bullets, score, level, missiles, max_missiles):
        # Bar dimensions based on screen size
        bar_width = int(SCREEN_WIDTH * 0.125)  # 12.5% of screen width (~200px at 1600px)
        bar_height = int(SCREEN_HEIGHT * 0.033)  # 3.3% of screen height (~30px at 900px)
        margin = int(SCREEN_WIDTH * 0.0125)  # 1.25% margin (~20px at 1600px)
        
        # Health Bar (Top Left) - at 2.2% from top
        health_text = f"{lives}/{max_lives}"
        health_y = int(SCREEN_HEIGHT * 0.022)
        self.draw_glass_bar(screen, margin, health_y, bar_width, bar_height, lives / max_lives, RED, "Health", health_text)
        
        # Level Bar (Below Health) - at 8.9% from top
        level_text = f"{level}/{SPACESHIP_LEVEL_MAX}"
        level_y = int(SCREEN_HEIGHT * 0.089)
        self.draw_glass_bar(screen, margin, level_y, bar_width, bar_height, level / SPACESHIP_LEVEL_MAX, LEVEL_BAR_COLOR, "Ship Level", level_text)

        # Ammo Bar (Bottom Left) - at 93.3% from top
        ammo_text = f"{available_bullets}/{max_bullets}"
        ammo_y = SCREEN_HEIGHT - bar_height - margin * 2
        self.draw_glass_bar(screen, margin, ammo_y, bar_width, bar_height, available_bullets / max_bullets, BLUE, "Ammo", ammo_text)

        # Missile Display (Bottom Right) - at 93.3% from top
        missile_text = f"{missiles}/{max_missiles}"
        missile_x = SCREEN_WIDTH - bar_width - margin
        missile_y = SCREEN_HEIGHT - bar_height - margin * 2
        self.draw_glass_bar(screen, missile_x, missile_y, bar_width, bar_height, missiles / max_missiles, MISSILE_COLOR, "Missiles (M)", missile_text)

        # Score (Top Right)
        score_text = f"Score: {score}"
        text_surf = self.font.render(score_text, True, WHITE)
        text_width = text_surf.get_width() + int(SCREEN_WIDTH * 0.025)  # 2.5% padding
        score_height = int(SCREEN_HEIGHT * 0.056)  # ~50px at 900p
        
        bg_surface = pygame.Surface((text_width, score_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, GLASS_BG, (0, 0, text_width, score_height), border_radius=10)
        pygame.draw.rect(bg_surface, GLASS_BORDER, (0, 0, text_width, score_height), 2, border_radius=10)
        
        score_x = SCREEN_WIDTH - text_width - margin
        score_y = int(SCREEN_HEIGHT * 0.022)
        screen.blit(bg_surface, (int(score_x), score_y))
        screen.blit(text_surf, (int(SCREEN_WIDTH - text_width), int(score_y + (score_height - text_surf.get_height()) // 2)))
