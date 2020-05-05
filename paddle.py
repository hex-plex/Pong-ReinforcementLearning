import pygame
import math
BLACK = (0,0,0)
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color ,width ,height , lev=2):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.height=height
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0,0,width,height])
        if lev==3:
            self.div=1
            self.vel=10
        elif lev==2:
            self.div=10
            self.vel=8
        else:
            self.div=25
            self.vel=5
        self.rect = self.image.get_rect()
    def dist(self,x1,x2,y1,y2,alpha):
        d=math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return math.exp(-d*alpha)


    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y =0
    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
            self.rect.y = 400
    def AI(self, ballpos):
        diff = ballpos.y - self.rect.y-(self.height/2)
        if self.div==1:
            diff*=self.dist(ballpos.x,self.rect.x+(self.height/2),ballpos.y,self.rect.y,10**-2)
        if(diff>0):
            self.moveDown(min(abs(diff/(self.div)),self.vel))
        else:
            self.moveUp(min(abs(diff/(self.div)),self.vel))
