import pygame
import sys
from src.config import *
from src.utils.asset_manager import AssetManager
from src.core.state_manager import StateManager
from src.database.db_manager import DBManager
from src.scenes.welcome_scene import WelcomeScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Travel | Naro Chan Dev")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.asset_manager = AssetManager()
        pygame.display.set_icon(self.asset_manager.get_asset('spaceship_img'))
        
        self.db_manager = DBManager()
        self.state_manager = StateManager(self)
        
        # Start music
        self.asset_manager.play_music()
        
        # Set initial scene
        self.state_manager.change_scene(WelcomeScene(self))

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    self.db_manager.close_connection()
                    pygame.quit()
                    sys.exit()
            
            if self.state_manager.current_scene:
                self.state_manager.current_scene.process_input(events)
                self.state_manager.current_scene.update()
                self.state_manager.current_scene.render(self.screen)
            
            pygame.display.update()
            self.clock.tick(FPS)
