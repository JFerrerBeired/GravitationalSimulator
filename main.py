import pygame
import modes
import settings

pygame.init()

global_controller = settings.GlobalController()
running_mode = modes.MainMenu(global_controller)

while running_mode.running:
    running_mode = running_mode.main_loop()
    
pygame.quit()