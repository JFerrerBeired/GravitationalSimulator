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
    
    def __init__(self, ini_pos, end_pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        length = utilities.get_distance(ini_pos, end_pos)
        if length > ARROW_MAX_LENGTH:
            end_pos = ((end_pos[0] - ini_pos[0]) / length * ARROW_MAX_LENGTH + ini_pos[0], 
                        (end_pos[1] - ini_pos[1]) / length * ARROW_MAX_LENGTH + ini_pos[1])
        length = utilities.get_distance(ini_pos, end_pos)
        
        #Calculate angle of rotation. Note the inversion of order in the y parameter bc of the inverter positivity of the Y axis
        arrow_angle = math.atan2(ini_pos[1] - end_pos[1], end_pos[0] - ini_pos[0])
        cap_angle = utilities.normalize_angle(math.radians(ARROW_CAP_ANGLE))
        
        cap_projection = []
        
     #   cap_projection = max(  )
        
        width = math.fabs(math.ceil(length * math.cos(arrow_angle)))
        height = math.fabs(math.ceil(length * math.sin(arrow_angle))) #TODO: take into account the possible offset of the cap
        
        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
       # self.image = pygame.Surface((width, height)).convert()
       
       #Sets the rect to the blit position and initial and end_pos to positions relative to this surface
        self.rect = self.image.get_rect()
        
        quadrant = utilities.get_quadrant(arrow_angle)
        if quadrant == 1:  #first quadrant
            self.rect.bottomleft = ini_pos
            ini_pos = (0, height)
            end_pos = (length*math.cos(arrow_angle), 0)
        elif quadrant == 2:  #second quadrant
            self.rect.bottomright = ini_pos
            ini_pos = (width, height)
            end_pos = (0, 0)
        elif quadrant == 3:  #third quadrant
            self.rect.topright = ini_pos
            ini_pos = (width, 0)
            end_pos = (0, height)
        else:  #fourth quadrant
            self.rect.topleft = ini_pos
            ini_pos = (0, 0)
            end_pos = (width, height)
        
            
        pygame.draw.line(self.image, ARROW_COLOR, ini_pos, end_pos, ARROW_WIDTH)
        pygame.draw.lines(self.image, ARROW_COLOR, False,  #draw the cap (basic trigonometry)
                          ((end_pos[0] - ARROW_CAP_LENGTH*math.cos(cap_angle - arrow_angle),
                           end_pos[1] - ARROW_CAP_LENGTH*math.sin(cap_angle - arrow_angle)),
                          (end_pos[0], end_pos[1]),
                          (end_pos[0] - ARROW_CAP_LENGTH*math.cos(cap_angle + arrow_angle),
                           end_pos[1] + ARROW_CAP_LENGTH*math.sin(cap_angle + arrow_angle))), 
                          ARROW_WIDTH)
