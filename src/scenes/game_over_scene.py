import pygame
import sys
from src.scenes.scene import Scene
from src.ui.components import Button
from src.core.background import Background
from src.config import *

class GameOverScene(Scene):
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score
        self.assets = self.game.asset_manager.assets
        self.font = pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.061))  # ~55px at 900p
        self.small_font = pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.044))  # ~40px at 900p
        
        # Background
        self.background = Background()
        
        # Button positioned at ~57.8% from top, 12.5% width, centered
        button_width = int(SCREEN_WIDTH * 0.125)
        button_height = int(SCREEN_HEIGHT * 0.056)
        self.replay_button = Button(
            SCREEN_WIDTH // 2 - button_width // 2, 
            int(SCREEN_HEIGHT * 0.578), 
            button_width, 
            button_height, 
            "Replay", 
            int(SCREEN_HEIGHT * 0.044),  # Font size ~40px at 900p
            (80, 80, 200), 
            (100, 100, 250)
        )
        
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
        # Update background
        self.background.update()
        
        if not self.getting_initials:
            self.replay_button.update(pygame.mouse.get_pos())

    def render(self, screen):
        # Draw background with stars and meteors
        self.background.draw(screen)
        
        if self.getting_initials:
            self._render_initials_input(screen)
        else:
            self._render_game_over(screen)

    def _render_initials_input(self, screen):
        # Position at ~11% from top
        instruction_text = self.font.render("Enter Your Initials:", True, WHITE)
        instruction_y = int(SCREEN_HEIGHT * 0.111)
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, instruction_y))

        # Initials at ~22% from top
        initials_text = self.font.render(self.initials, True, WHITE)
        initials_y = int(SCREEN_HEIGHT * 0.222)
        screen.blit(initials_text, (SCREEN_WIDTH // 2 - initials_text.get_width() // 2, initials_y))

        # Instructions at ~33% from top
        if len(self.initials) == 3:
            submit_text = self.small_font.render("Press Enter to Submit", True, WHITE)
        else:
            submit_text = self.small_font.render("Enter 3 Letters", True, WHITE)
        submit_y = int(SCREEN_HEIGHT * 0.333)
        screen.blit(submit_text, (SCREEN_WIDTH // 2 - submit_text.get_width() // 2, submit_y))

    def _render_game_over(self, screen):
        # Game Over title at ~5.6% from top
        title_text = self.font.render("Game Over!", True, RED)
        title_y = int(SCREEN_HEIGHT * 0.056)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, title_y))

        # Score at ~16.7% from top
        score_text = self.font.render(f"Your Score: {self.score}", True, WHITE)
        score_y = int(SCREEN_HEIGHT * 0.167)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, score_y))

        # Top scores title at ~27.8% from top
        top_scores_title = self.small_font.render("Top 5 High Scores", True, YELLOW)
        top_scores_y = int(SCREEN_HEIGHT * 0.278)
        screen.blit(top_scores_title, (SCREEN_WIDTH // 2 - top_scores_title.get_width() // 2, top_scores_y))

        # Leaderboard starting at ~33% from top
        leaderboard_start_y = int(SCREEN_HEIGHT * 0.333)
        line_spacing = int(SCREEN_HEIGHT * 0.044)  # ~40px at 900p
        
        if self.top_scores:
            for i, entry in enumerate(self.top_scores):
                initials = entry.get('initials', 'N/A')
                high_score = entry.get('high_score', 0)
                score_line = self.small_font.render(f"{i+1}. {initials} - {high_score}", True, WHITE)
                screen.blit(score_line, (SCREEN_WIDTH // 2 - score_line.get_width() // 2, leaderboard_start_y + i * line_spacing))
        else:
            unavailable_text = self.small_font.render("Leaderboard unavailable", True, WHITE)
            screen.blit(unavailable_text, (SCREEN_WIDTH // 2 - unavailable_text.get_width() // 2, leaderboard_start_y + line_spacing))

        self.replay_button.draw(screen)
