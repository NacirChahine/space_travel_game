import pygame
import random
from src.config import *
from src.utils.graphics import GraphicsGenerator

class Background:
    def __init__(self):
        self.stars = []
        self.layers = 3
        
        # Initialize stars
        for i in range(self.layers):
            num_stars = 50 * (i + 1)
            speed = (i + 1) * 0.5
            layer_stars = []
            for _ in range(num_stars):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                size = random.randint(1, 3)
                brightness = random.randint(150, 255)
                # Create star surface once
                img = GraphicsGenerator.draw_star(size, brightness)
                layer_stars.append({'x': x, 'y': y, 'speed': speed, 'img': img})
            self.stars.append(layer_stars)
            
        # Nebula/Dust (simple transparent shapes)
        self.nebulas = []
        for _ in range(3):
            w = random.randint(200, 400)
            h = random.randint(200, 400)
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            color = (random.randint(0, 50), random.randint(0, 50), random.randint(50, 100), 30)
            pygame.draw.ellipse(surf, color, (0, 0, w, h))
            self.nebulas.append({'x': random.randint(0, SCREEN_WIDTH), 'y': random.randint(0, SCREEN_HEIGHT), 'img': surf, 'speed': 0.2})

    def update(self):
        # Update stars
        for layer in self.stars:
            for star in layer:
                star['y'] += star['speed']
                if star['y'] > SCREEN_HEIGHT:
                    star['y'] = 0
                    star['x'] = random.randint(0, SCREEN_WIDTH)
                    
        # Update nebulas
        for nebula in self.nebulas:
            nebula['y'] += nebula['speed']
            if nebula['y'] > SCREEN_HEIGHT:
                nebula['y'] = -nebula['img'].get_height()
                nebula['x'] = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        screen.fill((10, 10, 20)) # Dark blue-black background
        
        # Draw nebulas
        for nebula in self.nebulas:
            screen.blit(nebula['img'], (nebula['x'], nebula['y']))
            
        # Draw stars
        for layer in self.stars:
            for star in layer:
                screen.blit(star['img'], (star['x'], star['y']))
