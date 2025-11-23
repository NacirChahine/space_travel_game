import pygame
from src.config import *

class HUD:
    def __init__(self, asset_manager):
        self.assets = asset_manager.assets
        self.font = pygame.font.SysFont(None, 36)

    def draw_health_bar(self, screen, lives, max_lives):
        bar_width = 20
        bar_spacing = 5
        x_offset = 10
        y_offset = 10

        for i in range(max_lives):
            color = RED if i < lives else BLACK
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(x_offset + i * (bar_width + bar_spacing), y_offset, bar_width, 15),
                border_radius=5
            )

    def draw_bullet_bar(self, screen, available_bullets, max_bullets):
        bar_width = 15
        bar_spacing = 5
        x_offset = 10
        y_offset = 35

        for i in range(max_bullets):
            color = BLUE if i < available_bullets else BLACK
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(x_offset + i * (bar_width + bar_spacing), y_offset, bar_width, 10),
                border_radius=3
            )

    def draw_score(self, screen, score):
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 15))

    def draw(self, screen, lives, max_lives, available_bullets, max_bullets, score):
        self.draw_health_bar(screen, lives, max_lives)
        self.draw_bullet_bar(screen, available_bullets, max_bullets)
        self.draw_score(screen, score)
