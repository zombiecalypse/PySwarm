from pygame.sprite import Sprite, RenderUpdates
from random import Random
from math import exp, log, sqrt
from .helpers import *

class Swarm(RenderUpdates):
    def __init__(self, x, y, n):
        RenderUpdates.__init__(self)
        rand = Random()
        for i in xrange(n):
            dx, dy = [rand.normalvariate(0, 50) for x in range(2)]
            elt = SwarmElement(x+dx, y+dy)
            elt.add(self)

    def update(self):
        RenderUpdates.update(self)
        for el in self.sprites():
            el.commit()

def pressure(x):
    assert x >= 0
    lx = log(x+1e-5)
    return 1.0/(lx*exp(-lx**2))

class SwarmElement(Sprite):
    SIZE = 15
    FAV_DIST = 2.0
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image, self.rect = load_image('particle.png', -1)
        self.rect.x, self.rect.y = (x,y)
        self.dx = 0
        self.dy = 0
        self.new_x = 0.0
        self.new_y = 0.0
        self.new_dx = 0.0
        self.new_dy = 0.0
    def buddies(self):
        return set(x for group in self.groups() for x in group if x != self)
    @property
    def pos(self):
        return (self.rect.x, self.rect.y)
    def d(self, o):
        return (o.rect.x - self.rect.x, o.rect.y - self.rect.y)
    def dist(self, o):
        return sqrt(sum(x*x for x in self.d(o)))
    def update_by_pressure(self, o):
        dx,dy = self.d(o)
        pres = pressure(self.dist(o) / (self.FAV_DIST *self.SIZE))
        self.new_dx += dx * pres * dt
        self.new_dy += dy * pres * dt
    def update(self):
        self.new_x, self.new_y = self.rect.x, self.rect.y
        for buddy in self.buddies():
            self.update_by_pressure(buddy)
    def commit(self):
        self.rect.x = bound(self.new_x + self.dx * dt, MIN_X, MAX_X )
        self.rect.y = bound(self.new_y + self.dx * dt, MIN_Y, MAX_Y)
        self.dx = self.new_dx
        self.dy = self.new_dy
