import pygame
from pygame.sprite import collide_mask
from paddle import Paddle
from ball import Ball
from random import randint
import cv2
import numpy as np
class Pong:
    pygame.mixer.pre_init(44100, -16, 1, 128)
    pygame.init()
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    size = (700,500)
    def __init__(self,levelodiff=2):
        self.levelodiff = levelodiff
        self.conti=0
        if self.levelodiff=="":
            self.levelodiff=1
        else:
            try:self.levelodiff=int(self.levelodiff)
            except:self.levelodiff = 2
        if self.levelodiff==4:
            self.levelodiff=3
            self.conti=1
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pong")
        self.paddleA = Paddle(self.WHITE,10, 100,self.levelodiff)
        self.paddleA.rect.x = 0
        self.paddleA.rect.y = 200

        self.paddleB = Paddle(self.WHITE , 10 , 100, self.levelodiff)
        self.paddleB.rect.x = 690
        self.paddleB.rect.y = 200

        self.ball = Ball(WHITE, 10, 10)
        self.ball.rect.x = 345
        self.ball.rect.y = 195

        self.all_sprites_list = pygame.sprite.Group()

        self.all_sprites_list.add(paddleA)
        self.all_sprites_list.add(paddleB)
        self.all_sprites_list.add(ball)
    self.carryOn = True

    def start(self):
        self.clock = pygame.time.Clock()

        flag=0
        flagrem=0
        no=0

        self.scoreA = 0
        self.scoreB = 0
        effect = pygame.mixer.Sound('Sounds/button-16-1.wav')
        while self.carryOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.carryOn = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        self.carryOn = False


            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.paddleA.moveUp(5)
            if keys[pygame.K_s]:
                self.paddleA.moveDown(5)
            if keys[pygame.K_UP]:
                self.paddleA.moveUp(5)
            if keys[pygame.K_DOWN]:
                self.paddleA.moveDown(5)

            if self.conti==1:
                self.paddleA.AI(ball.posi())

            self.paddleB.AI(ball.posi())

            self.all_sprites_list.update()


            if self.ball.rect.x>=690 and flag==0:
                effect.play()
                self.scoreA+=1
                self.ball.velocity[0] = -abs(self.ball.velocity[0])
                if abs(self.ball.velocity[0])<1:
                    self.ball.velocity[0] = randint(-5,-1)
                self.flag=1

            if self.ball.rect.x<=0 and flag==0:
                effect.play()
                self.scoreB+=1
                self.ball.velocity[0] = abs(self.ball.velocity[0])
                if abs(self.ball.velocity[0])<1:
                    self.ball.velocity[0] = randint(1,5)
                flag=1
            if self.ball.rect.y>=490 and flagrem==0:
                effect.play()
                self.ball.velocity[1] *= -1
                flagrem=1

            if self.ball.rect.y<=0 and flagrem==0:
                effect.play()
                self.ball.velocity[1] *= -1
                flagrem=1


            if ((collide_mask(self.ball,self.paddleA) or collide_mask(self.ball,self.paddleB)) and flag==0):
                effect.play()
                self.ball.bounce()
                flag=1
            #print(no,"ITS happeneing now")
                no+=1
            if self.ball.rect.x>11 and self.ball.rect.x<679:
                flag=0

            if self.ball.rect.y>10 and self.ball.rect.y<480:
                flagrem=0

            self.screen.fill(self.BLACK)
            pygame.draw.line(self.screen, self.WHITE, [349,0], [349,500], 5)
            self.all_sprites_list.draw(self.screen)

    ###Feed for the net###
            self.feed=np.array(pygame.PixelArray(screen),dtype=np.uint8)
            self.feed=feed.T
            self.feed=feed.reshape([500,700,1])

            cv2.imshow('hello',self.feed)
    ######################

            font = pygame.font.Font(None, 74)
            text = font.render(str(self.scoreA), 1 ,self.WHITE)
            self.screen.blit(text , (250,10))
            text = font.render(str(self.scoreB), 1 ,self.WHITE)
            self.screen.blit(text, (420,10))


            pygame.display.flip()
    #cv2.imshow("Hello",np.array(feed,dtype=np.uint8))
    #print(feed.shape)
    #print(np.array(feed,dtype=np.uint8).sum())
    ##this can be used for screen capturing
            cv2.waitKey(1)
            self.clock.tick(60)

    def close(self):pygame.quit()
if __name__=="__main__":
    print("ENTER DIFFICULTY")
    print("EASY     --> 1")
    print("MODERATE --> 2")
    print("HARD     --> 3")
    levelodiff=input()
    game = Pong(levelodiff)
