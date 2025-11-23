import pygame
import random
from src.scenes.scene import Scene
from src.utils.helpers import split_text
from src.config import *

class WelcomeScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.assets = self.game.asset_manager.assets
        self.font = pygame.font.SysFont(None, 30)
        self.title_font = pygame.font.SysFont(None, 50)
        
        self.space_facts = [
            "The Milky Way galaxy contains over 100 billion stars.",
            "The Andromeda Galaxy is the closest large galaxy to ours.",
            "The Hubble Space Telescope has been orbiting Earth since 1990.",
            "The International Space Station is the size of a football field.",
            "The Moon is slowly moving away from Earth.",
            "Mars is often called the Red Planet.",
            "Jupiter has the Great Red Spot, a giant storm that has been raging for centuries.",
            "Saturn is known for its beautiful rings, made of ice and rock.",
            "Pluto was reclassified as a dwarf planet in 2006.",
            "The Voyager 1 spacecraft is the farthest human-made object from Earth.",
            "Black holes are regions of space where gravity is so strong that nothing can escape.",
            "Comets are made of ice, dust, and rock.",
            "Asteroids are rocky objects in space.",
            "The universe is billions of years old.",
            "The Big Bang theory explains the origin of the universe.",
            "There may be life on other planets in the universe.",
            "Space suits protect astronauts from the harsh conditions of space.",
            "The first artificial satellite was Sputnik 1, launched in 1957.",
            "The Apollo 11 mission was the first to land humans on the Moon.",
            "The International Space Station is a joint project of many countries.",
            "Space is completely silent.",
            "The hottest planet in our solar system is Venus.",
            "A full NASA space suit costs $12 million.",
            "Neutron stars can spin 600 times per second.",
            "One day on Venus is longer than one year on Earth.",
            "There are more stars in the universe than grains of sand on Earth.",
            "The Sun accounts for 99.86% of the mass in the Solar System.",
            "There could be 500 million planets capable of supporting life in our galaxy.",
            "The Earth is a tiny speck in the vastness of space.",
            "The Milky Way galaxy is about 100,000 light-years across.",
            "The International Space Station orbits Earth at a speed of about 17,500 miles per hour.",
            "The Sun is about 4.6 billion years old.",
            "The Moon is about 4.5 billion years old.",
            "The Sun's surface temperature is about 5,500 degrees Celsius.",
            "The Sun's core temperature is about 15 million degrees Celsius."
        ]
        self.random_fact = random.choice(self.space_facts)
        self.wrapped_fact_lines = split_text(self.random_fact, self.font, 760)
        
        self.blink = True
        self.blink_timer = pygame.time.get_ticks()

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                from src.scenes.game_scene import GameScene
                self.game.state_manager.change_scene(GameScene(self.game))

    def update(self):
        if pygame.time.get_ticks() - self.blink_timer > 500:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def render(self, screen):
        screen.fill(BLACK)
        
        # Logo
        logo = self.assets['logo_img']
        screen.blit(logo, (SCREEN_WIDTH // 2 - logo.get_width() // 3, 110))

        # Fact
        for i, line in enumerate(self.wrapped_fact_lines):
            fact_text = self.font.render(line, True, YELLOW)
            fact_text_x = SCREEN_WIDTH // 2 - fact_text.get_width() // 2
            screen.blit(fact_text, (fact_text_x, 500 + i * 30))

        # Title
        title_text = self.title_font.render("Welcome to Spaceship Game!", True, WHITE)
        title_text_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2
        screen.blit(title_text, (title_text_x, 50))

        # Blink text
        if self.blink:
            enter_text = self.title_font.render("Press ENTER to Start", True, RED)
            enter_text_x = SCREEN_WIDTH // 2 - enter_text.get_width() // 2
            screen.blit(enter_text, (enter_text_x, 440))
