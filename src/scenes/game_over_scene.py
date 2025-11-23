import pygame
import sys
from src.scenes.scene import Scene
from src.ui.components import Button
from src.config import *

class GameOverScene(Scene):
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score
        self.assets = self.game.asset_manager.assets
        self.font = pygame.font.SysFont(None, 55)
        self.small_font = pygame.font.SysFont(None, 40)
        
        self.replay_button = Button(SCREEN_WIDTH // 2 - 100, 520, 200, 50, "Replay", 40, (80, 80, 200), (100, 100, 250))
        
        # Load top scores
        self.top_scores = self.game.db_manager.load_top_scores()
        
        # Check if we need to get initials
        self.getting_initials = False
        self.initials = ""
        if len(self.top_scores) < 5 or (len(self.top_scores) > 0 and self.score > self.top_scores[-1]['high_score']):
            self.getting_initials = True

    def process_input(self, events):
        for event in events:
            if self.getting_initials:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(self.initials) == 3:
                        self.game.db_manager.save_high_score(self.score, self.initials)
                        self.getting_initials = False
                        self.top_scores = self.game.db_manager.load_top_scores() # Reload scores
                    elif event.key == pygame.K_BACKSPACE:
                        self.initials = self.initials[:-1]
                    elif len(self.initials) < 3 and event.unicode.isalpha():
                        self.initials += event.unicode.upper()
            else:
                if self.replay_button.is_clicked(event):
                    from src.scenes.game_scene import GameScene
                    self.game.state_manager.change_scene(GameScene(self.game))

    def update(self):
        if not self.getting_initials:
            self.replay_button.update(pygame.mouse.get_pos())

    def render(self, screen):
        screen.fill(BLACK)
        
        if self.getting_initials:
            self._render_initials_input(screen)
        else:
            self._render_game_over(screen)

    def _render_initials_input(self, screen):
        instruction_text = self.font.render("Enter Your Initials:", True, WHITE)
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 100))

        initials_text = self.font.render(self.initials, True, WHITE)
        screen.blit(initials_text, (SCREEN_WIDTH // 2 - initials_text.get_width() // 2, 200))

        if len(self.initials) == 3:
            submit_text = self.small_font.render("Press Enter to Submit", True, WHITE)
        else:
            submit_text = self.small_font.render("Enter 3 Letters", True, WHITE)
        screen.blit(submit_text, (SCREEN_WIDTH // 2 - submit_text.get_width() // 2, 300))

    def _render_game_over(self, screen):
        title_text = self.font.render("Game Over!", True, RED)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        score_text = self.font.render(f"Your Score: {self.score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150))

        top_scores_title = self.small_font.render("Top 5 High Scores", True, YELLOW)
        screen.blit(top_scores_title, (SCREEN_WIDTH // 2 - top_scores_title.get_width() // 2, 250))

        if self.top_scores:
            for i, entry in enumerate(self.top_scores):
                initials = entry.get('initials', 'N/A')
                high_score = entry.get('high_score', 0)
                score_line = self.small_font.render(f"{i+1}. {initials} - {high_score}", True, WHITE)
                screen.blit(score_line, (SCREEN_WIDTH // 2 - score_line.get_width() // 2, 300 + i * 40))
        else:
            unavailable_text = self.small_font.render("Leaderboard unavailable", True, WHITE)
            screen.blit(unavailable_text, (SCREEN_WIDTH // 2 - unavailable_text.get_width() // 2, 320))

        self.replay_button.draw(screen)
