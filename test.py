import numpy as np
from scipy.spatial import distance
import time
import pygame

def draw():
    print(xBall, yBall)
    if wait:
        
    stuck = False
    screen.fill((0, 0, 0))
    screen.blit(text, textRect)
    pygame.draw.circle(screen, (255, 0, 0), (xBall, yBall), radius)
    pygame.draw.line(screen, (0, 0, 255), (xObs, yObs), (xFinal, yFinal))
    pygame.draw.line(screen, (0, 255, 0), (xObs, yObs), (xObs+500, yObs))
    pygame.draw.line(screen, (255, 0, 255), (xObs, yObs), (xCol, yCol))
    pygame.draw.line(screen, (0, 255, 255), (xObs, yObs), (xBall, yBall))

xObs, yObs = 200, 200
xFinal, yFinal = 700, 700
xBall, yBall = 450, 160
radius = 100

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
running = True
stuck = False
yVel = 0.5
xVel = 0

pygame.display.set_caption('Test')

font = pygame.font.Font('freesansbold.ttf', 32)

text = font.render('Test', True, (0, 255, 0), (0, 0, 255))

textRect = text.get_rect()

textRect.center = (800, 800)

wait = True
while running:
    # for event in pygame.event.get():
    #     if event.type==pygame.QUIT:
    #         running = False
    #     pygame.key.set_repeat(10, 10)

    #     if event.type == pygame.KEYDOWN:
    #         keys = pygame.key.get_pressed()
    #         if keys[pygame.K_UP]:
    #             yBall -= 2
    #         if keys[pygame.K_DOWN]:
    #             yBall += 2
    #         if keys[pygame.K_RIGHT]:
    #             xBall += 2
    #         if keys[pygame.K_LEFT]:
    #             xBall -= 2
    #         if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
    #             xBall += 2
    #             yBall -= 2
    #         if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
    #             xBall -= 2
    #             yBall -= 2
    #         if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
    #             xBall += 2
    #             yBall += 2
    #         if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
    #             xBall -= 2
    #             yBall += 2

    yBall += yVel
    xBall += xVel
    dis = distance.euclidean([xObs, yObs], [xBall, yBall])
    theta = 135*np.pi/180
    if not stuck:
        xCol, yCol = xBall + 100*np.cos(theta), yBall + 100*np.sin(theta)
    else:
        xBallNext, yBallNext = xBall + 100*np.cos(theta), yBall + 100*np.sin(theta)
        thetaCol = np.arctan((yBallNext-yObs)/(xBallNext-xObs))*180/np.pi
        if xBallNext-xObs < 0:
            thetaCol += 180
        if thetaCol < 45:
            xCol, yCol = xBallNext, yBallNext            
        else:
            # xBall, yBall = xBallStuck, yBallStuck
            pass
    thetaCol = np.arctan((yCol-yObs)/(xCol-xObs))*180/np.pi
    if xCol-xObs < 0:
        thetaCol += 180


    # if thetaCol <= -90:
    #     if dis <= radius:
    #         print("Time: {}. COLLISION".format(time.time()))
    #         stuck = True
    #         xBallStuck, yBallStuck = xBall, yBall
    #     else:
    #         draw()
    if thetaCol < 45:
        xVel, yVel = 0, 0.5
    else:
        stuck = True
        xBallStuck, yBallStuck = xBall, yBall
        tmpVel = 0.5*np.cos(np.pi/4)
        xVel, yVel = tmpVel * np.cos(np.pi/4), tmpVel * np.cos(np.pi/4)
        xBall += xVel
        yBall += yVel
    
    draw()
    pygame.display.flip()
    time.sleep(0.01)

