import numpy as np
from scipy.spatial import distance
import pygame


xObs, yObs = 100, 800
xFinal, yFinal = 800, 100
xBall, yBall = 700, 700
radius = 100

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
running = True

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
        pygame.key.set_repeat(10, 10)

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                yBall -= 2
            if keys[pygame.K_DOWN]:
                yBall += 2
            if keys[pygame.K_RIGHT]:
                xBall += 2
            if keys[pygame.K_LEFT]:
                xBall -= 2
            if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                xBall += 2
                yBall -= 2
            if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                xBall -= 2
                yBall -= 2
            if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                xBall += 2
                yBall += 2
            if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                xBall -= 2
                yBall += 2


    dis = distance.euclidean([xObs, yObs], [xBall, yBall])
    theta = min(225*np.pi/180, np.pi+np.arccos((yObs - yBall)/dis))
    print(theta*180/np.pi)
    print((np.pi+np.arccos((yObs - yBall)/dis))*180/np.pi)
    # theta = 225*np.pi/180
    xCol, yCol = xBall + 100*np.cos(theta), yBall + 100*np.sin(theta)
    # print((yCol-yObs)/(xCol-xObs))
    if (yCol-yObs)/(xCol-xObs) > -1:    
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), (xBall, yBall), radius)
        pygame.draw.line(screen, (0, 0, 255), (xObs, yObs), (xFinal, yFinal))
        pygame.draw.line(screen, (0, 255, 0), (xObs, yObs), (xBall, yBall))
        pygame.draw.line(screen, (0, 255, 0), (xObs, yObs), (xCol, yCol))

    pygame.display.flip()

# def callback_human(msg):
#     global screen, sc, xpos_r, ypos_r, xpos_b, ypos_b, key_lock, count1, initx_human, inity_human
#     if count1 == 0:
#         initx_human = int(round(sc*(msg.point.x+0.5)))
#         inity_human = int(round(sc*(-msg.point.y+0.5)))
#     count1 += 1
#     xpos_b = int(round(sc*(msg.point.x+0.5))) - initx_human + 500
#     ypos_b = int(round(sc*(-msg.point.y+0.5))) - inity_human + 500
#     # screen.fill((0, 0, 0))
#     # pygame.draw.circle(screen, (255, 0, 0), (xpos_r, ypos_r), radius)
#     # pygame.draw.circle(screen, (0, 0, 255), (xpos_b, ypos_b), radius)
#     # pygame.display.flip()


# def callback_robot(msg):
#     global screen, sc, xpos_r, ypos_r, xpos_b, ypos_b, key_lock, count2, initx_robot, inity_robot
#     if count2 == 0:
#         initx_robot = int(round(sc*(msg.pose.position.x+0.5)))
#         inity_robot = int(round(sc*(-msg.pose.position.y+0.5)))
#     count2 += 1
#     xpos_r = int(round(sc*(msg.pose.position.x+0.5))) - initx_robot + 500
#     ypos_r = int(round(sc*(-msg.pose.position.y+0.5))) - inity_robot + 500
#     # xpos_r = int(round(sc*(msg.point.x+0.5)))
#     # ypos_r = int(round(sc*(-msg.point.y+0.5)))

#     # screen.fill((0, 0, 0))
#     pygame.draw.circle(screen, (0, 0, 255), (xpos_b, ypos_b), radius)
#     pygame.draw.circle(screen, (255, 0, 0), (xpos_r, ypos_r), radius)
#     pygame.display.flip()


