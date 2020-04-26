import pygame
import math
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLANET_COLOR, PLANET_MIN_RADIUS, PLANET_MAX_RADIUS, PLANET_MAX_DISTANCE,
    ARROW_COLOR_VEL, ARROW_COLOR_ACC, ARROW_MAX_LENGTH, 
    ARROW_HALF_THICKNESS, ARROW_CAP_LENGTH, ARROW_CAP_ANGLE,
    SMALL_ARROW_HALF_THICKNESS, SMALL_ARROW_CAP_LENGTH, SMALL_ARROW_CAP_ANGLE,
    ARROW_TO_VEL_RATIO, ARROW_TO_ACC_RATIO,
    DELTA_T
)
import utilities


class CelestialObject(pygame.sprite.Sprite):
    containers = []
    planets = pygame.sprite.Group() #Group that contains all planets created
    
    def __init__(self, position, radius, density):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        #Objects that are affected by this object when calculating forces. 
        #Note that the presence in the list is not reciprocal because this object will calculate the force for both of them
        self.neighbours = pygame.sprite.Group()
        self.arrow_vel = pygame.sprite.Sprite()
        self.arrow_acc = pygame.sprite.Sprite()
        
        for obj in self.planets:
            obj.neighbours.add(self)
            
        self.planets.add(self)
        
        if radius > PLANET_MAX_RADIUS:
            self.radius = PLANET_MAX_RADIUS
        elif radius < PLANET_MIN_RADIUS:
            self.radius = PLANET_MIN_RADIUS
        else:
            self.radius = radius
        
        self.mass = density*self.radius**3 #not real mass, but proportional to it (missing 4/3*PI)
        size = 2*self.radius + 1

        #self.image = pygame.Surface((size, size)).convert()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        
        pygame.draw.circle(self.image, PLANET_COLOR, 
                           (self.radius, self.radius), self.radius)
        
        self.F = [0, 0]
        self.acc = [0, 0]
        self.vel = [0, 0]
        self.pos = [position[0], position[1]]
        
    def set_velocity_from_arrow(self, vel):
        '''Takes the length of an arrow and sets the velocity proportional to it.'''
        self.vel[0] = vel[0] * ARROW_TO_VEL_RATIO
        self.vel[1] = vel[1] * ARROW_TO_VEL_RATIO
    
    def get_force(self, obj):
        '''Return the force between self and obj.'''

        vect = [obj.pos[0] - self.pos[0], obj.pos[1] - self.pos[1]]
        factor = self.mass * obj.mass / utilities.get_distance(self.pos, obj.pos)**3 #Power of 3 because the directional vector is not normalized
        
        return (vect[0] * factor, vect[1] * factor)
    
    def integration_euler(self):
        '''Calculates the new position and velocity using Euler integration method.
        
        The force is also added to the other object so it doesn't have to be 
        calculated twice.'''
        for obj in self.neighbours:
            f = self.get_force(obj)

            self.F[0] += f[0]
            self.F[1] += f[1]
            obj.F[0] -= f[0]
            obj.F[1] -= f[1]
            
        self.acc[0] = self.F[0] / self.mass
        self.acc[1] = self.F[1] / self.mass
        
        self.pos[0] += self.vel[0] * DELTA_T + 0.5 * self.acc[0] * DELTA_T
        self.pos[1] += self.vel[1] * DELTA_T + 0.5 * self.acc[1] * DELTA_T
        
        self.vel[0] += self.acc[0] * DELTA_T
        self.vel[1] += self.acc[1] * DELTA_T
        
        self.F = [0, 0] #resets force for the next iteration
        
    def update(self):
        '''Calculates new position and velocity of the object and all the calculations derived from that.'''
        self.integration_euler()
        self.rect.center = (self.pos[0], self.pos[1])
   
        self.arrow_vel.kill()
        self.arrow_acc.kill()
        
        self.arrow_vel = Arrow((self.pos[0], self.pos[1]), 
                                (self.pos[0] + self.vel[0]/ARROW_TO_VEL_RATIO, 
                                 self.pos[1] + self.vel[1]/ARROW_TO_VEL_RATIO),
                                 half_thickness = SMALL_ARROW_HALF_THICKNESS, 
                                 cap_angle = SMALL_ARROW_CAP_ANGLE, 
                                 cap_length = SMALL_ARROW_CAP_LENGTH)
        
        self.arrow_acc = Arrow((self.pos[0], self.pos[1]), 
                                (self.pos[0] + self.acc[0]/ARROW_TO_ACC_RATIO, 
                                 self.pos[1] + self.acc[1]/ARROW_TO_ACC_RATIO),
                                 color = ARROW_COLOR_ACC, 
                                 half_thickness = SMALL_ARROW_HALF_THICKNESS, 
                                 cap_angle = SMALL_ARROW_CAP_ANGLE, 
                                 cap_length = SMALL_ARROW_CAP_LENGTH)
    
        #if it gets too far away, gets destroyed
        if utilities.get_distance((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 
                                  (self.rect.centerx, self.rect.centery)) > PLANET_MAX_DISTANCE:
            self.kill()
        
        
class Arrow(pygame.sprite.Sprite):
    containers = []
    
    def __init__(self, ini_pos, end_pos, color = ARROW_COLOR_VEL, half_thickness = ARROW_HALF_THICKNESS, cap_angle = ARROW_CAP_ANGLE, cap_length = ARROW_CAP_LENGTH):
        pygame.sprite.Sprite.__init__(self, self.containers)

        length = utilities.get_distance(ini_pos, end_pos)
        if length > ARROW_MAX_LENGTH:
            end_pos = ((end_pos[0] - ini_pos[0]) / length * ARROW_MAX_LENGTH + ini_pos[0], 
                        (end_pos[1] - ini_pos[1]) / length * ARROW_MAX_LENGTH + ini_pos[1])
        length = utilities.get_distance(ini_pos, end_pos)
        
        thickness = 1 + 2*math.floor(half_thickness)
        
        #Calculate angle of rotation. Note the inversion of order in the y parameter bc of the inverter positivity of the Y axis
        arrow_angle = math.atan2(ini_pos[1] - end_pos[1], end_pos[0] - ini_pos[0])
        cap_angle = utilities.normalize_angle(math.radians(cap_angle))
        offset = math.ceil(cap_length * math.sin(cap_angle))  #Worst case scenario. Adds this quantity to the size of rect
        
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
            
        pygame.draw.line(self.image, color, ini_arrow, end_arrow, thickness)
        pygame.draw.lines(self.image, color, False,  #draw the cap (basic trigonometry)
                          ((end_arrow[0] - cap_length * math.cos(cap_angle - arrow_angle),
                           end_arrow[1] - cap_length * math.sin(cap_angle - arrow_angle)),
                           end_arrow,
                          (end_arrow[0] - cap_length * math.cos(cap_angle + arrow_angle),
                           end_arrow[1] + cap_length * math.sin(cap_angle + arrow_angle))), 
                          thickness)
        