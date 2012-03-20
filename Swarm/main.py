import pygame
import pygame.display
import pygame.time
import logging

import pymunk as pm

from .swarm import generate_swarm
from .helpers import *

def main(options = dict()):
    logging.basicConfig()
    pygame.init()
    pygame.display.set_mode((MAX_X,MAX_Y), pygame.DOUBLEBUF)
    
    swarm = generate_swarm(space)

    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()


    bg = pygame.Surface(screen.get_size()).convert()
    bg.fill((200,200,200))

    while True:
        space.step(dt)
        swarm.update()
        screen.blit(bg, (0,0))
        swarm.draw(screen)
        pygame.display.flip()
        clock.tick(int(1.0/dt))
