import os.path
import pygame
import logging
from pygame.locals import RLEACCEL
logger = logging.getLogger("Loader")
def setDebug():
    logger.setLevel(logging.DEBUG)
__IMAGES__ = dict()

def load_image(name, colorKey = None):
    "Pure loading function"
    #if __IMAGES__.has_key(name): return __IMAGES__[name]

    fullname = os.path.abspath(os.path.join('data', name))
    logger.debug("Loading {}".format(fullname))
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error, message:
        logger.fatal("Can't load {}".format(name))
        raise SystemExit, message
    if colorKey is not None:
        if colorKey is -1:
            colorKey = image.get_at((0,0))
        image.set_colorkey(colorKey, RLEACCEL)
    img = __IMAGES__[name] = (image, image.get_rect())
    return img

def avg(*args):
    if not args: return None

    return sum(args)* 1.0/len(args)

def bound(x, up, dn):
    return max(min(x, dn), up)

THECOLORS = dict(
        black = pygame.color.Color(0,0,0,255),
        green = pygame.color.Color(0,255,0,255)
        )

dt = 0.02
MIN_X, MAX_X = 0, 640
MIN_Y, MAX_Y = 0, 480
