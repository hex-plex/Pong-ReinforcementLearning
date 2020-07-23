import pygame
from random import randint
BLACK = (0,0,0)

class Ball(pygame.sprite.Sprite):

    def __init__(self, color , width ,height, twidth, theight):

        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.twidth = twidth
        self.width = width
        self.theight = theight
        self.height = height
        pygame.draw.rect(self.image,color , [0,0,width, height])

        self.velocity = [randint(4,8),randint(-8,8)]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = min(max(self.rect.x+self.velocity[0],0),self.twidth-self.width)
        ## Clipping solves a lot of glitches should have done this earlier
        self.rect.y = min(max(self.rect.y+self.velocity[1],0),self.theight-self.height)
        ## Clipping solves a lot of glitches should have done this earlier
    def bounce(self):
        self.velocity[0] *= -1
        self.velocity[1] = randint(-8,8)
    def posi(self):
        return self.rect
    def spawn(self):
        self.velocity = [randint(4,8),randint(-8,8)]
        self.rect.x = self.twidth/2
        self.rect.y = self.theight/2
        return True
