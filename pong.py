import pygame
from pygame.sprite import collide_mask
from paddle import Paddle
from ball import Ball
pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)
size = (700,500)
print("ENTER DIFFICULTY")
print("EASY     --> 1")
print("MODERATE --> 2")
print("HARD     --> 3")
levelodiff=input()
conti=0
if levelodiff=="":
    levelodiff=1
else:
    levelodiff=int(levelodiff)
if levelodiff==4:
    levelodiff=3
    conti=1
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
paddleA = Paddle(WHITE,10, 100,levelodiff)
paddleA.rect.x = 0
paddleA.rect.y = 200

paddleB = Paddle(WHITE , 10 , 100, levelodiff)
paddleB.rect.x = 690
paddleB.rect.y = 200

ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
carryOn = True

clock = pygame.time.Clock()

scoreA = 0
scoreB = 0
effect = pygame.mixer.Sound('Sounds/button-16-1.wav')
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carryOn = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
    if keys[pygame.K_UP]:
        paddleA.moveUp(5)
    if keys[pygame.K_DOWN]:
        paddleA.moveDown(5)

    if conti==1:
        paddleA.AI(ball.posi())

    paddleB.AI(ball.posi())

    all_sprites_list.update()

    if ball.rect.x>=690 :
        effect.play()
        scoreA+=1
        ball.velocity[0] *= -1
    if ball.rect.x<=0:
        effect.play()
        scoreB+=1
        ball.velocity[0] *= -1

    if ball.rect.y>490:
        effect.play()
        ball.velocity[1] *= -1

    if ball.rect.y<0:
        effect.play()
        ball.velocity[1] *= -1


    if collide_mask(ball,paddleA) or collide_mask(ball, paddleB):
        effect.play()
        ball.bounce()



    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [349,0], [349,500], 5)
    all_sprites_list.draw(screen)

    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1 , WHITE)
    screen.blit(text , (250,10))
    text = font.render(str(scoreB), 1 ,WHITE)
    screen.blit(text, (420,10))

    #print(pygame.PixelArray(screen)) ##this can be used for screen capturing
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
