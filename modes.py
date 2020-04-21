import math
import pygame
from pygame.locals import (
    QUIT, 
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN,
    K_SPACE
)
from constants import (
    FPS_CAP, 
    PLANET_DEFAULT_DENSITY,
    ARROW_TO_VELOCITY_RATIO
)
import objects
import utilities


def init_mode(self, global_controller):
    self.clock = pygame.time.Clock()
    self.running = True
    self.GC = global_controller

class MainMenu(): #By now it's just a dummy class that send you to draw mode
    def __init__(self, global_controller):
        init_mode(self, global_controller)
        
    def main_loop(self):
        return DrawMode(self.GC)

class DrawMode():
    def __init__(self, global_controller):
        init_mode(self, global_controller)
        
        self.sel_radius = False
        self.sel_arrow = False
    
    def new_object(self):
        self.sel_radius = True
        center = pygame.mouse.get_pos()
        aux_obj = objects.CelestialObject(center, 0, PLANET_DEFAULT_DENSITY) #set radius to 0 so the initializer will set PLANET_MIN_RADIUS
        aux_arrow = pygame.sprite.Sprite() #dummy sprite that can get killed
        
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.event.post(event) #I put it back in so it can exit cleanly in the main loop
                    return
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.sel_arrow = False
                    aux_obj.set_velocity((ARROW_TO_VELOCITY_RATIO * aux_arrow.component[0],
                                          - ARROW_TO_VELOCITY_RATIO * aux_arrow.component[1]))
                    aux_arrow.kill()
                    return
 
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    self.sel_radius = False
                    self.sel_arrow = True

            if self.sel_radius: #modifies the radius of the celestial object
                radius = math.floor(utilities.get_distance(center, 
                                                           pygame.mouse.get_pos()))
                # Kills the previously generated sprite and create a new one
                aux_obj.kill()
                aux_obj = objects.CelestialObject(center,
                radius, PLANET_DEFAULT_DENSITY)
            
            if self.sel_arrow: #creates an arrow to set the velocity
                aux_arrow.kill()
                aux_arrow = objects.Arrow(center, pygame.mouse.get_pos())

            
            self.GC.screen.blit(self.GC.background, (0, 0))
            self.GC.all.draw(self.GC.screen)
            
            pygame.display.flip()
            
            self.clock.tick(FPS_CAP)
    
    def main_loop(self):
        while self.running:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = 0
                    return self
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.new_object()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    for sprite in self.GC.all:
                        sprite.kill()
                        
            self.GC.all.update()            
            
            self.GC.screen.blit(self.GC.background, (0, 0))
            self.GC.all.draw(self.GC.screen)
            
            pygame.display.flip()
            
            self.clock.tick(FPS_CAP)
        