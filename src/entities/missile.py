import pygame
import math
from src.entities.entity import Entity
from src.config import *

class Missile(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = 12
        self.exploded = False
        self.trail_timer = 0
        # Optional: distance threshold to consider "reached center"
        self.explosion_distance = 20

    def get_viewport_center(self, camera_offset_x=0, camera_offset_y=0):
        """
        Calculate the center of the current viewport.
        
        Args:
            camera_offset_x: Horizontal camera offset (for panning/scrolling)
            camera_offset_y: Vertical camera offset (for panning/scrolling)
            
        Returns:
            Tuple (center_x, center_y) representing the viewport center
        """
        viewport_center_x = (SCREEN_WIDTH // 2) + camera_offset_x
        viewport_center_y = (SCREEN_HEIGHT // 2) + camera_offset_y
        return viewport_center_x, viewport_center_y

    def update(self, camera_offset_x=0, camera_offset_y=0):
        """
        Update missile position to move toward viewport center.
        
        Args:
            camera_offset_x: Optional horizontal camera offset
            camera_offset_y: Optional vertical camera offset
        """
        # Dynamically calculate the center of the current viewport
        # This accounts for any camera movement, panning, or zooming
        viewport_center_x, viewport_center_y = self.get_viewport_center(camera_offset_x, camera_offset_y)
        
        # Calculate distance to viewport center
        dx = viewport_center_x - self.rect.centerx
        dy = viewport_center_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        # Check if missile has reached the center
        if distance <= self.explosion_distance:
            self.exploded = True
        else:
            # Move towards the viewport center
            # Normalize the direction vector
            if distance > 0:
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed
                
                self.rect.x += move_x
                self.rect.y += move_y
