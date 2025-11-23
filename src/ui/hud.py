import pygame
from src.config import *

class HUD:
    def __init__(self, asset_manager):
        self.assets = asset_manager.assets
        self.font = pygame.font.SysFont(None, 36)

    def draw_glass_bar(self, screen, x, y, width, height, fill_percent, color, label=None):
        # Background (Glass)
        bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, GLASS_BG, (0, 0, width, height), border_radius=10)
        pygame.draw.rect(bg_surface, GLASS_BORDER, (0, 0, width, height), 2, border_radius=10)
        screen.blit(bg_surface, (x, y))

        # Fill
        if fill_percent > 0:
            fill_width = int((width - 10) * fill_percent)
            fill_rect = pygame.Rect(x + 5, y + 5, fill_width, height - 10)
            pygame.draw.rect(screen, color, fill_rect, border_radius=8)

        # Label
        if label:
            label_surf = self.font.render(label, True, WHITE)
            screen.blit(label_surf, (x + 10, y - 25))

    def draw(self, screen, lives, max_lives, available_bullets, max_bullets, score, level):
        # Health Bar
        self.draw_glass_bar(screen, 20, 40, 200, 30, lives / max_lives, RED, "Health")
        
        # Ammo Bar
        self.draw_glass_bar(screen, 20, 100, 200, 30, available_bullets / max_bullets, BLUE, "Ammo")

        # Level Bar
        self.draw_glass_bar(screen, 20, 160, 200, 30, level / SPACESHIP_LEVEL_MAX, LEVEL_BAR_COLOR, "Ship Level")

        # Score (Glass box)
        score_text = f"Score: {score}"
        text_surf = self.font.render(score_text, True, WHITE)
        text_width = text_surf.get_width() + 40
        
        bg_surface = pygame.Surface((text_width, 50), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, GLASS_BG, (0, 0, text_width, 50), border_radius=10)
        pygame.draw.rect(bg_surface, GLASS_BORDER, (0, 0, text_width, 50), 2, border_radius=10)
        
        screen.blit(bg_surface, (SCREEN_WIDTH - text_width - 20, 20))
        screen.blit(text_surf, (SCREEN_WIDTH - text_width, 32))
