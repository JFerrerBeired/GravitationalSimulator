import pygame

from constants import (
    WINDOW_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
)

import objects

class GlobalController():
    def __init__(self):
        pygame.display.set_caption(WINDOW_TITLE)
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(BACKGROUND_COLOR)
        
        self.all = pygame.sprite.RenderUpdates()
        self.arrow = pygame.sprite.GroupSingle()
        objects.CelestialObject.containers = self.all
        objects.Arrow.containers = self.arrow
        
        