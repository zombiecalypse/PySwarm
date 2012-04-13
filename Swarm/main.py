import pygame
import pygame.display
import pygame.time
import logging

from .helpers import *
from swarm import generate_swarm

def main(options = dict()):
    logging.basicConfig()
    pygame.init()
    pygame.display.set_mode((MAX_X,MAX_Y), pygame.DOUBLEBUF)
    
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    bg = pygame.Surface(screen.get_size()).convert()
    bg.fill((200,200,200))

    swarm = generate_swarm()

    for i in range(1000):
        swarm.update()
        swarm.swarm.step()
        print "."
        screen.blit(bg, (0,0))
        swarm.draw(screen)
        pygame.display.flip()
        clock.tick(int(1.0/dt))
