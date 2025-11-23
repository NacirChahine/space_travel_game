import pygame
import random
import math
from src.config import *

class GraphicsGenerator:
    @staticmethod
    def draw_spaceship(width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Colors
        hull_color = (200, 200, 255)
        cockpit_color = (0, 255, 255)
        engine_color = (255, 100, 0)
        detail_color = (100, 100, 150)
        
        center_x = width // 2
        
        # Main Hull (Triangle shape)
        points = [
            (center_x, 0),  # Nose
            (width, height),  # Bottom Right
            (center_x, height - 10), # Bottom Center (Engine recess)
            (0, height)   # Bottom Left
        ]
        pygame.draw.polygon(surface, hull_color, points)
        pygame.draw.polygon(surface, detail_color, points, 2) # Outline
        
        # Cockpit
        cockpit_rect = pygame.Rect(center_x - 5, height // 2 - 10, 10, 15)
        pygame.draw.ellipse(surface, cockpit_color, cockpit_rect)
        
        # Wings details
        pygame.draw.line(surface, detail_color, (center_x, 10), (10, height - 5), 2)
        pygame.draw.line(surface, detail_color, (center_x, 10), (width - 10, height - 5), 2)
        
        # Engine Glow
        engine_rect = pygame.Rect(center_x - 8, height - 8, 16, 8)
        pygame.draw.ellipse(surface, engine_color, engine_rect)
        
        return surface

    @staticmethod
    def draw_asteroid(width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Base color variations
        gray_val = random.randint(100, 180)
        base_color = (gray_val, gray_val, gray_val)
        shadow_color = (gray_val - 40, gray_val - 40, gray_val - 40)
        
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2
        
        # Generate irregular polygon for asteroid shape
        num_points = random.randint(8, 12)
        points = []
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            # Vary radius slightly for irregularity
            r = radius * random.uniform(0.8, 1.0)
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.append((x, y))
            
        pygame.draw.polygon(surface, base_color, points)
        pygame.draw.polygon(surface, shadow_color, points, 2)
        
        # Add craters
        num_craters = random.randint(2, 5)
        for _ in range(num_craters):
            crater_r = random.randint(3, 8)
            crater_x = random.randint(center_x - radius // 2, center_x + radius // 2)
            crater_y = random.randint(center_y - radius // 2, center_y + radius // 2)
            pygame.draw.circle(surface, shadow_color, (crater_x, crater_y), crater_r)
            
        return surface

    @staticmethod
    def draw_bullet(width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Glowing effect
        # Outer glow
        pygame.draw.rect(surface, (255, 255, 0, 100), (0, 0, width, height), border_radius=2)
        # Inner core
        pygame.draw.rect(surface, (255, 255, 255), (1, 1, width - 2, height - 2), border_radius=2)
        
        return surface
    
    @staticmethod
    def draw_star(size, brightness):
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2)
        return surface
