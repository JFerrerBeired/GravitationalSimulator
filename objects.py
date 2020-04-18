import pygame
import math
from constants import (
    PLANET_COLOR,
    ARROW_COLOR)


class CelestialObject(pygame.sprite.Sprite):
    def __init__(self, position, radius, density):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.radius = radius
        self.mass = density*radius**3 #not real mass, but proportional to it (missing 4/3*PI)
        size = 2*radius + 1
        
        #self.image = pygame.Surface((size, size)).convert()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        
        pygame.draw.circle(self.image, PLANET_COLOR, (radius, radius), radius)
        
    def set_velocity(self, vel):
        self.vel_x = vel[0]
        self.vel_y = vel[1]
        
class Arrow(pygame.sprite.Sprite):#TODO: thick line parameter and take it into account to change the surface size
    def __init__(self, initialPos, finalPos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        width = math.fabs(initialPos[0]-finalPos[0])
        height = math.fabs(initialPos[1]-finalPos[1])

        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
      #  self.image = pygame.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        
        if initialPos[0] < finalPos[0]:
           if initialPos[1] > finalPos[1]: #First cuadrant
               self.rect.bottomleft = initialPos
               pygame.draw.line(self.image, ARROW_COLOR, (0, height), (width, 0), 3)
               
    
        
        