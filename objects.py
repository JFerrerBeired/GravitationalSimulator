import pygame
import math
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLANET_COLOR, PLANET_MIN_RADIUS, PLANET_MAX_RADIUS, PLANET_MAX_DISTANCE,
    ARROW_COLOR, ARROW_MAX_LENGTH, ARROW_HALF_THICKNESS, ARROW_CAP_LENGTH, ARROW_CAP_ANGLE
)
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
        
        self.vel = [0, 0]
        self.pos = [position[0], position[1]]
        
    def set_velocity(self, vel):
        self.vel[0] = vel[0]
        self.vel[1] = vel[1]
        
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.rect.center = (self.pos[0], self.pos[1])
        
        #if it gets too far away, gets destroyed
        if utilities.get_distance((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 
                                  (self.rect.centerx, self.rect.centery)) > PLANET_MAX_DISTANCE:
            self.kill()
        
        
class Arrow(pygame.sprite.Sprite):
    containers = []
    
    def __init__(self, ini_pos, end_pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        length = utilities.get_distance(ini_pos, end_pos)
        if length > ARROW_MAX_LENGTH:
            end_pos = ((end_pos[0] - ini_pos[0]) / length * ARROW_MAX_LENGTH + ini_pos[0], 
                        (end_pos[1] - ini_pos[1]) / length * ARROW_MAX_LENGTH + ini_pos[1])
        length = utilities.get_distance(ini_pos, end_pos)
        
        thickness = 1 + 2*math.floor(ARROW_HALF_THICKNESS)
        
        #Calculate angle of rotation. Note the inversion of order in the y parameter bc of the inverter positivity of the Y axis
        arrow_angle = math.atan2(ini_pos[1] - end_pos[1], end_pos[0] - ini_pos[0])
        cap_angle = utilities.normalize_angle(math.radians(ARROW_CAP_ANGLE))
        offset = math.ceil(ARROW_CAP_LENGTH * math.sin(cap_angle))  #Worst case scenario. Adds this quantity to the size of rect
        
        self.component = (length * math.cos(arrow_angle), length * math.sin(arrow_angle))
        projection = (math.fabs(math.ceil(self.component[0])), 
                      math.fabs(math.ceil(self.component[1])))
        
        width = math.fabs(projection[0]) + 2*offset
        height = math.fabs(projection[1]) + 2*offset
        
        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
      #  self.image = pygame.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        
        quadrant = utilities.get_quadrant(arrow_angle)
        if quadrant == 1:  #first quadrant
            ini_arrow = (offset, projection[1] + offset)
            end_arrow = (projection[0] + offset, offset)
            self.rect.bottomleft = (ini_pos[0] - offset, ini_pos[1] + offset)
        elif quadrant == 2:  #second quadrant
            ini_arrow = (projection[0] + offset, projection[1] + offset)
            end_arrow = (offset, offset)
            self.rect.bottomright = (ini_pos[0] + offset, ini_pos[1] + offset)         
        elif quadrant == 3:  #third quadrant
            ini_arrow = (projection[0] + offset, offset)
            end_arrow = (offset, projection[1] + offset)
            self.rect.topright = (ini_pos[0] + offset, ini_pos[1] - offset)           
        else:  #fourth quadrant
            ini_arrow = (offset, offset)
            end_arrow = (projection[0] + offset, projection[1] + offset)
            self.rect.topleft = (ini_pos[0] - offset, ini_pos[1] - offset)
            
        pygame.draw.line(self.image, ARROW_COLOR, ini_arrow, end_arrow, thickness)
        pygame.draw.lines(self.image, ARROW_COLOR, False,  #draw the cap (basic trigonometry)
                          ((end_arrow[0] - ARROW_CAP_LENGTH*math.cos(cap_angle - arrow_angle),
                           end_arrow[1] - ARROW_CAP_LENGTH*math.sin(cap_angle - arrow_angle)),
                           end_arrow,
                          (end_arrow[0] - ARROW_CAP_LENGTH*math.cos(cap_angle + arrow_angle),
                           end_arrow[1] + ARROW_CAP_LENGTH*math.sin(cap_angle + arrow_angle))), 
                          thickness)
        