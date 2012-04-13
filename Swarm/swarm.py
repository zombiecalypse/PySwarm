from random import Random
from pygame.sprite import Sprite, RenderUpdates
from pygame.surface import Surface
from pygame.draw import circle
from pygame.locals import *
from time import sleep
from .helpers import *
import logging
import pyswarm

logger = logging.getLogger('Swarm')

def setDebug():
    logger.setLevel(logging.DEBUG)

class SwarmGroup(RenderUpdates):
    def __init__(self, swarm):
        RenderUpdates.__init__(self)
        self.swarm = swarm
        for i in range(len(list(swarm.elements))):
            SwarmElementSprite(self, swarm[i])

    def update(self):
        #self.swarm.update()
        RenderUpdates.update(self)


class SwarmElementSprite(Sprite):
    DIM = (20,20)
    def translate(self, position):
        return (100 + position[0]*10, 100+position[1]*10)
    def __init__(self, group, body):
        Sprite.__init__(self, group)
        self.body = body
        self.image = Surface(self.DIM, SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.translate(self.body.position)
        circle(self.image, THECOLORS['black'], (self.rect.width/2,
            self.rect.height/2), self.rect.width/2)
    def update(self):
        self.rect.center = self.translate(self.body.position)

def generate_swarm():
    nelt = 100
    swarm = pyswarm.Swarm()
    for i in range(nelt):
        swarm.add_random()
    return SwarmGroup(swarm)
