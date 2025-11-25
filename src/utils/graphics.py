import pygame
import random
import math
from src.config import *

class GraphicsGenerator:
    @staticmethod
    def draw_spaceship(width, height, level=1):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Colors based on level
        if level == 1:
            hull_color = (200, 200, 255)
            engine_color = (255, 100, 0)
        elif level == 2:
            hull_color = (150, 150, 255)
            engine_color = (255, 50, 0)
        elif level == 3:
            hull_color = (100, 100, 255)
            engine_color = (255, 0, 0)
        elif level == 4:
            # Advanced sleek design with purple tones
            hull_color = (150, 100, 255)
            engine_color = (0, 255, 255)  # Cyan engine
        else:  # Level 5
            # Elite design with deep purple and gold accents
            hull_color = (100, 50, 200)
            engine_color = (255, 215, 0)  # Gold engine
            
        cockpit_color = (0, 255, 255)
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
        
        # Additional details for higher levels
        if level >= 2:
            # Side wings
            pygame.draw.polygon(surface, hull_color, [(0, height-20), (-10, height), (10, height-10)])
            pygame.draw.polygon(surface, hull_color, [(width, height-20), (width+10, height), (width-10, height-10)])
            
        if level >= 3:
            # Extra cannons
            pygame.draw.rect(surface, detail_color, (center_x - 15, height - 15, 4, 15))
            pygame.draw.rect(surface, detail_color, (center_x + 11, height - 15, 4, 15))
        
        if level >= 4:
            # Advanced armor plating (hexagonal patterns)
            armor_color = (180, 150, 255) if level == 4 else (150, 100, 255)
            pygame.draw.polygon(surface, armor_color, [(center_x - 8, 15), (center_x + 8, 15), (center_x + 12, 25), (center_x + 8, 35), (center_x - 8, 35), (center_x - 12, 25)])
            # Shield emitters on wings
            pygame.draw.circle(surface, (100, 200, 255), (8, height - 25), 4)
            pygame.draw.circle(surface, (100, 200, 255), (width - 8, height - 25), 4)
            
        if level >= 5:
            # Elite features: Energy cores
            core_color = (255, 215, 0)
            pygame.draw.circle(surface, core_color, (center_x - 10, height // 2), 3)
            pygame.draw.circle(surface, core_color, (center_x + 10, height // 2), 3)
            # Advanced wing structure
            pygame.draw.polygon(surface, hull_color, [(5, height - 30), (0, height - 10), (15, height - 20)])
            pygame.draw.polygon(surface, hull_color, [(width - 5, height - 30), (width, height - 10), (width - 15, height - 20)])
            # Extra detail lines
            pygame.draw.line(surface, (200, 150, 255), (center_x - 5, 20), (center_x - 5, height - 30), 1)
            pygame.draw.line(surface, (200, 150, 255), (center_x + 5, 20), (center_x + 5, height - 30), 1)

        # Cockpit
        cockpit_rect = pygame.Rect(center_x - 5, height // 2 - 10, 10, 15)
        pygame.draw.ellipse(surface, cockpit_color, cockpit_rect)
        
        # Wings details
        pygame.draw.line(surface, detail_color, (center_x, 10), (10, height - 5), 2)
        pygame.draw.line(surface, detail_color, (center_x, 10), (width - 10, height - 5), 2)
        
        # Engine Glow (varies by level)
        if level == 4:
            # Dual engine configuration
            pygame.draw.ellipse(surface, engine_color, (center_x - 10, height - 8, 8, 8))
            pygame.draw.ellipse(surface, engine_color, (center_x + 2, height - 8, 8, 8))
        elif level == 5:
            # Triple engine configuration
            pygame.draw.ellipse(surface, engine_color, (center_x - 12, height - 8, 7, 8))
            pygame.draw.ellipse(surface, engine_color, (center_x - 3, height - 8, 7, 8))
            pygame.draw.ellipse(surface, engine_color, (center_x + 6, height - 8, 7, 8))
        else:
            # Single engine for levels 1-3
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
    def draw_bullet(width, height, level=1):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Colors based on level
        if level == 1:
            glow_color = (255, 255, 0, 100)
            core_color = (255, 255, 255)
        elif level == 2:
            glow_color = (0, 255, 255, 100)
            core_color = (200, 255, 255)
        else:
            glow_color = (255, 0, 255, 100)
            core_color = (255, 200, 255)

        # Glowing effect
        # Outer glow
        pygame.draw.rect(surface, glow_color, (0, 0, width, height), border_radius=2)
        # Inner core
        pygame.draw.rect(surface, core_color, (1, 1, width - 2, height - 2), border_radius=2)
        
        return surface

    @staticmethod
    def draw_boss(width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Boss Colors
        body_color = (100, 0, 0)
        detail_color = (200, 50, 50)
        core_color = (255, 0, 0)
        
        center_x, center_y = width // 2, height // 2
        
        # Main Body (Hexagon-ish)
        points = [
            (center_x, 0),
            (width, height // 3),
            (width, height * 2 // 3),
            (center_x, height),
            (0, height * 2 // 3),
            (0, height // 3)
        ]
        pygame.draw.polygon(surface, body_color, points)
        pygame.draw.polygon(surface, detail_color, points, 3)
        
        # Glowing Core
        pygame.draw.circle(surface, core_color, (center_x, center_y), width // 4)
        pygame.draw.circle(surface, (255, 100, 100), (center_x, center_y), width // 6)
        
        # Weapon Mounts
        pygame.draw.circle(surface, detail_color, (10, height // 2), 8)
        pygame.draw.circle(surface, detail_color, (width - 10, height // 2), 8)
        
        return surface

    @staticmethod
    def draw_enemy_projectile(width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 0, 0), (width // 2, height // 2), width // 2)
        pygame.draw.circle(surface, (255, 255, 0), (width // 2, height // 2), width // 4)
        return surface
    
    @staticmethod
    def draw_star(size, brightness):
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2)
        return surface

    @staticmethod
    def draw_missile(width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Missile Body
        body_color = (255, 165, 0) # Orange
        fin_color = (200, 50, 50) # Red
        
        center_x = width // 2
        
        # Body (Ellipse)
        pygame.draw.ellipse(surface, body_color, (center_x - 5, 0, 10, height - 10))
        
        # Fins
        # Left Fin
        pygame.draw.polygon(surface, fin_color, [(center_x - 5, height - 15), (0, height), (center_x - 5, height - 5)])
        # Right Fin
        return surface

    @staticmethod
    def draw_explosion_frame(radius, color_core, color_outer):
        size = radius * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (radius, radius)
        
        # Outer glow
        pygame.draw.circle(surface, color_outer, center, radius)
        # Inner core
        pygame.draw.circle(surface, color_core, center, radius * 0.7)
        
        return surface
