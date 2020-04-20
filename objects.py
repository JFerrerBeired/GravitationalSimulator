import pygame
import math
from constants import (
    PLANET_COLOR, PLANET_MIN_RADIUS, PLANET_MAX_RADIUS,
    ARROW_COLOR, ARROW_MAX_LENGTH, ARROW_WIDTH, ARROW_CAP_LENGTH, ARROW_CAP_ANGLE)
import utilities


class CelestialObject(pygame.sprite.Sprite):
    containers = []
    
    def __init__(self, position, radius, density):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        if radius > PLANET_MAX_RADIUS:
            self.radius = PLANET_MAX_RADIUS
        elif radius < PLANET_MIN_RADIUS:
            self.radius = PLANET_MIN_RADIUS
        else:
            self.radius = radius
        
        self.mass = density*radius**3 #not real mass, but proportional to it (missing 4/3*PI)
        size = 2*self.radius + 1
        
        #self.image = pygame.Surface((size, size)).convert()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        
        pygame.draw.circle(self.image, PLANET_COLOR, 
                           (self.radius, self.radius), self.radius)
        
    def set_velocity(self, vel):
        self.vel_x = vel[0]
        self.vel_y = vel[1]
        
class Arrow(pygame.sprite.Sprite):
    containers = []
    
    height = 2*ARROW_CAP_LENGTH * math.tan(math.radians(ARROW_CAP_ANGLE))
    half_height = math.ceil(height/2) #in case it is odd, gets the central height

    def __init__(self, initialPos, finalPos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        width = utilities.get_distance(initialPos, finalPos)
       #height calculated only once in class definition since it's not meant to change
       
        if width > ARROW_MAX_LENGTH:
            finalPos = ((finalPos[0] - initialPos[0]) / width * ARROW_MAX_LENGTH + initialPos[0], 
                        (finalPos[1] - initialPos[1]) / width * ARROW_MAX_LENGTH + initialPos[1])
            width = utilities.get_distance(initialPos, finalPos)
       
        self.image = pygame.Surface((width, self.height), pygame.SRCALPHA).convert_alpha()
       # self.image = pygame.Surface((width, self.height)).convert()
       
        #draws an horizontal arrow (it's easier to calculate) and then rotate it
        pygame.draw.line(self.image, ARROW_COLOR, (0, self.half_height), 
                         (width, self.half_height), ARROW_WIDTH)
        pygame.draw.lines(self.image, ARROW_COLOR, False, 
                          ((width - ARROW_CAP_LENGTH, 0), (width, self.half_height),
                           (width - ARROW_CAP_LENGTH, self.height)), ARROW_WIDTH)
        #Calculate angle of rotation. Note the inversion of order in the y parameter bc of the inverter positivity of the Y axis
        angle = math.degrees(math.atan2(initialPos[1] - finalPos[1], 
                                        finalPos[0] - initialPos[0])) 
        if angle < 0: angle += 360 #TODO: Think about why doesn't get the rotation if I don't translate it to the [0, 360] interval
        self.image = pygame.transform.rotate(self.image, angle)
      
        self.rect = self.image.get_rect()
        
        #set rect position according to the quadrant
        
        #TODO: Get this with the correct offset
        if angle < 90: #first quadrant
            self.rect.bottomleft = initialPos
        elif angle < 180: #second quadrant
            self.rect.bottomright = initialPos
        elif angle < 270: #third quadrant
            self.rect.topright = initialPos
        else: #you get the idea
            self.rect.topleft = initialPos
        

               
    
        
        