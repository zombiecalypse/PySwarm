import pygame
import pygame.display
import pygame.time
import logging

from .swarm import SwarmElement, Swarm
from .helpers import *

def main(options = dict()):
    logging.basicConfig()
    pygame.init()
    pygame.display.set_mode((MAX_X,MAX_Y), pygame.DOUBLEBUF)
    
    swarm = Swarm(100, 130, 50)

    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    bg = pygame.Surface(screen.get_size()).convert()
    bg.fill((250,250,250))

    while True:
        swarm.update()
        screen.blit(bg, (0,0))
        swarm.draw(screen)
        pygame.display.flip()
        clock.tick(10)
