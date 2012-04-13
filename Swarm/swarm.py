from random import Random
from pymunk import Body, Circle
from pygame.sprite import Sprite, RenderUpdates
from pygame.surface import Surface
from pygame.draw import circle
from pygame.locals import *
from time import sleep
from .helpers import *
import logging

logger = logging.getLogger('Swarm')

def setDebug():
    logger.setLevel(logging.DEBUG)

class Swarm(object):
    def __init__(self, space, p, n):
        rand = Random()
        self.elements = set()
        self.attractors = set()
        self.space = space
        self.running = True
        x, y = p
        for i in xrange(n):
            dx, dy = rand.normalvariate(0, 50), rand.normalvariate(0,50)
            elt = SwarmElement((x+dx, y+dy))
            self.elements.add(elt)
            elt.addTo(self.space)

    def update(self):
        for e in self.elements:
            e.update(self.elements, self.attractors)

    def add_attractor(self, p):
        self.attractors.add(Attractor(p))


class Attractor(Circle):
    def __init__(self, p):
        Circle.__init__(self, Body(1e100,100), 5, (0,0))
        self.body.position = p
        self.friction = 0.5
        self.collision_type = 2
    @property
    def position(self):
        return self.body.position
    @property
    def velocity(self):
        return self.body.velocity

def unwrap_self_update(*arg, **kwargs):
    return SwarmElement.update(*arg, **kwargs)

class SwarmElement(Circle):
    def __init__(self, p):
        Circle.__init__(self, Body(10,100), 2, (0,0))
        self.body.position = p
        self.friction = 0.5
        self.collision_type = 2
    def addTo(self, space):
        space.add(self, self.body)

    @property
    def speed(self):
        return 50

    @property
    def position(self):
        return self.body.position
    @property
    def velocity(self):
        return self.body.velocity

    @property
    def spartial_cohesion(self):
        return 0.1
    @property
    def pulsar_cohesion(self):
        return 0.05
    def weight(self, o):
        assert o!= self
        return 1.0/o.position.get_dist_sqrd(self.position)
    def weighted_by_distance(self, others):
        return [(self.weight(o), o) for o in others if o != self and
                o.position.get_distance(self.position) < 10*self.radius]
    @property
    def threshold(self):
        return .1
    def fweighted_avg(self, weighted, f):
        mapped = ((w,f(x)) for w,x in weighted)
        sum_weight, sum_val = reduce(lambda x,y: (x[0]+y[0],
            x[0]*x[1]+y[0]*y[1]), mapped, (1,0))
        return sum_val/sum_weight

    def push_from(self, others):
        for e in others:
            dpos = (self.position - e.position)/(self.radius*5)
            self.body.apply_force(dpos*pow(dpos.get_length()+1e-5,-4)
                    *self.spartial_avoidance)

    def attract_to(self, attractors):
        for a in attractors:
            dpos = a.position - self.position
            self.body.apply_force(dpos*self.attractor_attractiveness)

    @property
    def spartial_avoidance(self):
        return 100.0
    @property
    def attractor_attractiveness(self):
        return 10.0
    def update(self, others, attractors):
        weighted = self.weighted_by_distance(others)
        avg_pos = self.fweighted_avg(weighted, lambda x: x.position)
        avg_vel = self.fweighted_avg(weighted, lambda x: x.velocity)
        dpos = avg_pos - self.body.position
        if dpos > self.radius*5:
            self.body.apply_force((avg_pos - self.body.position)*self.spartial_cohesion)
        self.body.apply_force((avg_vel - self.body.velocity)*self.pulsar_cohesion)

        self.attract_to(attractors)
        self.push_from(others)

        self.body.velocity = self.body.velocity.normalized()*self.speed

class SwarmGroup(RenderUpdates):
    def __init__(self, swarm):
        RenderUpdates.__init__(self)
        self.swarm = swarm
        for s in swarm.elements:
            SwarmElementSprite(self, s)
        for s in swarm.attractors:
            AttractorSprite(self, s)

    def update(self):
        #self.swarm.update()
        RenderUpdates.update(self)

class AttractorSprite(Sprite):
    def __init__(self, group, body):
        Sprite.__init__(self, group)
        self.body = body
        bb = self.body.cache_bb()
        self.image = Surface((bb.right - bb.left,bb.top - bb.bottom), SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (avg(bb.right,bb.left), avg(bb.top, bb.bottom))
        circle(self.image, THECOLORS['green'], (self.rect.width/2,
            self.rect.height/2), self.rect.width/2)
    def update(self):
        bb = self.body.cache_bb()
        self.rect.center = (avg(bb.right,bb.left), avg(bb.top, bb.bottom))

class SwarmElementSprite(Sprite):
    def __init__(self, group, body):
        Sprite.__init__(self, group)
        self.body = body
        bb = self.body.cache_bb()
        self.image = Surface((bb.right - bb.left,bb.top - bb.bottom), SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (avg(bb.right,bb.left), avg(bb.top, bb.bottom))
        circle(self.image, THECOLORS['black'], (self.rect.width/2,
            self.rect.height/2), self.rect.width/2)
    def update(self):
        bb = self.body.cache_bb()
        self.rect.center = (avg(bb.right,bb.left), avg(bb.top, bb.bottom))

def generate_swarm(space, center = (200,200)):
    n_elt = 10
    swarm = Swarm( space, center, n_elt)
    swarm.add_attractor((150,150))
    return SwarmGroup(swarm)
