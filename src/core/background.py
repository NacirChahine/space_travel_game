import pygame
import random
import math
from src.config import *
from src.utils.graphics import GraphicsGenerator

class Background:
    def __init__(self):
        self.stars = []
        self.layers = 3
        
        # Initialize stars with twinkling effect
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
                layer_stars.append({
                    'x': x, 
                    'y': y, 
                    'speed': speed, 
                    'img': img,
                    'brightness': brightness,
                    'size': size,
                    'twinkle_timer': random.randint(0, 100),
                    'twinkle_speed': random.uniform(0.02, 0.08)
                })
            self.stars.append(layer_stars)
            
        # Nebula/Dust (simple transparent shapes) - positioned relative to screen size
        self.nebulas = []
        for _ in range(3):
            w = random.randint(int(SCREEN_WIDTH * 0.125), int(SCREEN_WIDTH * 0.25))
            h = random.randint(int(SCREEN_HEIGHT * 0.22), int(SCREEN_HEIGHT * 0.44))
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            color = (random.randint(0, 50), random.randint(0, 50), random.randint(50, 100), 30)
            pygame.draw.ellipse(surf, color, (0, 0, w, h))
            self.nebulas.append({
                'x': random.randint(0, SCREEN_WIDTH), 
                'y': random.randint(0, SCREEN_HEIGHT), 
                'img': surf, 
                'speed': 0.2
            })
        
        # Meteors - dynamic effects
        self.meteors = []
        self.meteor_spawn_timer = 0
        self.meteor_spawn_interval = random.randint(3000, 6000)  # Spawn every 3-6 seconds

    def spawn_meteor(self):
        """Spawn a meteor at a random position"""
        # Start from top or right side
        if random.random() < 0.5:
            # From top
            x = random.randint(int(SCREEN_WIDTH * 0.2), int(SCREEN_WIDTH * 0.8))
            y = -20
        else:
            # From right side
            x = SCREEN_WIDTH + 20
            y = random.randint(0, int(SCREEN_HEIGHT * 0.5))
        
        # Meteor properties
        length = random.randint(30, 80)
        width = random.randint(3, 8)
        speed_x = random.uniform(-2, -8)
        speed_y = random.uniform(2, 6)
        
        # Create meteor surface
        meteor_surf = pygame.Surface((length, width), pygame.SRCALPHA)
        
        # Gradient from bright white to orange/yellow
        # Draw with Head at Right (length) and Tail at Left (0)
        for i in range(length):
            # Alpha increases towards the head (Right)
            alpha = int(255 * (i / length))
            
            if i > length * 0.7:
                color = (255, 255, 255, alpha)  # White core (Head)
            elif i > length * 0.4:
                color = (255, 200, 100, alpha)  # Yellow
            else:
                color = (255, 150, 50, alpha)   # Orange tail
            pygame.draw.line(meteor_surf, color, (i, width // 2), (i, width // 2))
        
        self.meteors.append({
            'x': x,
            'y': y,
            'speed_x': speed_x,
            'speed_y': speed_y,
            'img': meteor_surf,
            # Calculate angle for rotation (negative Y because screen Y is down)
            'angle': math.degrees(math.atan2(-speed_y, speed_x))
        })

    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Update stars with twinkling
        for layer in self.stars:
            for star in layer:
                star['y'] += star['speed']
                if star['y'] > SCREEN_HEIGHT:
                    star['y'] = 0
                    star['x'] = random.randint(0, SCREEN_WIDTH)
                
                # Twinkling effect
                star['twinkle_timer'] += star['twinkle_speed']
                twinkle_brightness = int(star['brightness'] * (0.7 + 0.3 * math.sin(star['twinkle_timer'])))
                star['img'] = GraphicsGenerator.draw_star(star['size'], twinkle_brightness)
                    
        # Update nebulas
        for nebula in self.nebulas:
            nebula['y'] += nebula['speed']
            if nebula['y'] > SCREEN_HEIGHT:
                nebula['y'] = -nebula['img'].get_height()
                nebula['x'] = random.randint(0, SCREEN_WIDTH)
        
        # Spawn meteors
        if current_time - self.meteor_spawn_timer > self.meteor_spawn_interval:
            self.spawn_meteor()
            self.meteor_spawn_timer = current_time
            self.meteor_spawn_interval = random.randint(3000, 6000)
        
        # Update meteors
        meteors_to_remove = []
        for meteor in self.meteors:
            meteor['x'] += meteor['speed_x']
            meteor['y'] += meteor['speed_y']
            
            # Remove if off screen
            if meteor['x'] < -100 or meteor['y'] > SCREEN_HEIGHT + 100:
                meteors_to_remove.append(meteor)
        
        for meteor in meteors_to_remove:
            self.meteors.remove(meteor)

    def draw(self, screen):
        # Dark space background
        screen.fill((10, 10, 20))
        
        # Draw nebulas
        for nebula in self.nebulas:
            screen.blit(nebula['img'], (int(nebula['x']), int(nebula['y'])))
            
        # Draw stars
        for layer in self.stars:
            for star in layer:
                screen.blit(star['img'], (int(star['x']), int(star['y'])))
        
        # Draw meteors
        for meteor in self.meteors:
            # Rotate and draw
            rotated = pygame.transform.rotate(meteor['img'], meteor['angle'])
            rect = rotated.get_rect(center=(int(meteor['x']), int(meteor['y'])))
            screen.blit(rotated, rect)
