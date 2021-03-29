from config import *
from assets import *
import math
import numpy as np
from scipy.spatial import distance

class GameBoard:
    def __init__(self,layout):
        self.walls = []
        self.layout = layout
        for row in range(len(layout)):
            self.walls.append([])
            for col in range(len(layout[0])):
                self.walls[row].append(None)
                if layout[row][col] != 0:
                    if layout[row][col] == 2:
                        self.hole = Hole(32*col - 150, 32*row - 150, self)
                    elif layout[row][col] == 3:
                        self.ball = Ball((32*col) - 150, (32*row) -150, self)
                    else:
                        self.walls[row][col] = Wall((32*col) - 160,(32*row) - 160, layout[row][col], self)


        self.rot_x = 0
        self.rot_y = 0
        self.max_x_rotation = 0.5
        self.max_y_rotation = 0.5
        self.slide = False

        self.keyMap = {1:(1,0),
                        2:(-1,0),
                        4:(0,1),5:(1,1),6:(-1,1),7:(0,1),
                        8:(0,-1),9:(1,-1),10:(-1,-1),11:(0,-1),13:(1,0),14:(-1,0)}
    
    def getBallCoords(self):
        return (self.ball.x, self.ball.y)


    def collideWall(self, test, current, x, y, velx, vely):
        # find the grid that the ball tends to enter
        xGrid = math.floor(test/32 + 5)
        yGrid = math.floor(current/32 + 5)
        biggest = max(xGrid,yGrid)
        smallest = min(xGrid,yGrid)

        # if the ball tends to get out of the board limits, then collision
        if biggest > 13 or smallest < 0:
            return 0, 0, True

        # if the grid has an object
        if self.walls[yGrid][xGrid] != None:
            # square object
            # if self.walls[yGrid][xGrid] == 1:
            #     return 0, 0, True
            
            # change reference point to be down left pixel of the grid
            xObs, yObs = 0, 0
            xBall, yBall = x-32*xGrid + 160, y-32*yGrid + 160

            # left triangle object 
            if self.layout[yGrid][xGrid] == 4:
                
                # collision angle
                theta = 225*np.pi/180
                xCol, yCol = xBall + 8*np.cos(theta), yBall + 8*np.sin(theta)
                thetaCol = np.arctan((yCol-yObs)/(xCol-32-xObs))*180/np.pi
                if thetaCol > 0:
                    return velx, vely, False
                else:
                    thetaCol += 180
                
                # if ball hits the triangle object, then collision
                # if ball touches the triangle object, then slide
                if thetaCol > 135:
                    if velx > -0.01 and vely > -0.01:
                        self.slide = True
                    if self.slide:
                        if vely <= 0:
                            tmpVel = vely*np.sin(np.pi/4)
                            return 2 * tmpVel * np.sin(-np.pi/4), 2 * tmpVel * np.cos(-np.pi/4), False
                        elif vely > 0:
                            return velx, vely, False 
                    else:
                        self.slide = False
                        return 0, 0, True
                else:
                    return velx, vely, False
            
            # right triangle
            elif self.layout[yGrid][xGrid] == 5:
                
                # collision angle
                theta = 45*np.pi/180
                xCol, yCol = xBall + 8*np.cos(theta), yBall + 8*np.sin(theta)
                thetaCol = np.arctan((yCol-yObs)/(xCol-32-xObs))*180/np.pi
                if thetaCol > 0:
                    return velx, vely, False
                else:
                    thetaCol += 180

                # if ball hits the triangle object, then collision
                # if ball touches the triangle object, then slide
                if thetaCol < 135:
                    if velx < 0.01 and vely < 0.01:
                        self.slide = True

                    if self.slide:
                        if vely >= 0:
                            tmpVel = vely*np.cos(np.pi/4)
                            return 2 * tmpVel * np.cos(3*np.pi/4), 2 * tmpVel * np.sin(3*np.pi/4), False
                        elif vely < 0:
                            return velx, vely, False
                    else:
                        self.slide =  False
                        return 0, 0, True
                else:
                    return velx, vely, False
            else:
                self.slide = False
            return 0, 0, True
        return velx, vely, False
    
    def update(self):
        #compute rotation matrix
        rot_x_m = pyrr.Matrix44.from_x_rotation(self.rot_x)
        rot_y_m = pyrr.Matrix44.from_y_rotation(self.rot_y)
        self.rotationMatrix = pyrr.matrix44.multiply(rot_x_m,rot_y_m)

        self.ball.update()
        self.hole.update()

        for row in self.walls:
            for wall in row:
                if wall != None:
                    wall.update()

    def handleKeys(self,key):
        if key in self.keyMap:
            angleIncrement = self.keyMap[key]
            self.rot_x += 0.01*angleIncrement[0]
            if self.rot_x >= self.max_x_rotation:
                self.rot_x = self.max_x_rotation
            elif self.rot_x <= -self.max_x_rotation:
                self.rot_x = -self.max_x_rotation
            self.rot_y += 0.01*angleIncrement[1]
            if self.rot_y >= self.max_y_rotation:
                self.rot_y = self.max_y_rotation
            elif self.rot_y <= -self.max_y_rotation:
                self.rot_y = -self.max_y_rotation
    
    def draw(self, mode=False, idx=0):
        glUniformMatrix4fv(MODEL_LOC,1,GL_FALSE,self.rotationMatrix)
        glBindVertexArray(BOARD_MODEL.getVAO())
        glBindTexture(GL_TEXTURE_2D,BOARD.getTexture())
        glDrawArrays(GL_TRIANGLES,0,BOARD_MODEL.getVertexCount())

        self.ball.draw()
        self.hole.draw()

        for row in self.walls:
            for wall in row:
                if wall != None:
                    wall.draw()
        if mode:
            translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 400, 0]))
            glUniformMatrix4fv(MODEL_LOC,1,GL_FALSE,pyrr.matrix44.multiply(translation, pyrr.matrix44.create_identity()))
            glBindVertexArray(TEXT_MODEL.getVAO())
            glBindTexture(GL_TEXTURE_2D,TEXT[idx].getTexture())
            glDrawArrays(GL_TRIANGLES,0,TEXT_MODEL.getVertexCount())

class Wall:
    def __init__(self,x,y,type,parent):
        self.parent = parent
        self.x = x
        self.y = y
        self.z = 0
        self.type = type-1

    def update(self):
        #first translate to position on board, then rotate with the board
        translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([self.x,self.y,self.z]))
        self.model = pyrr.matrix44.multiply(translation,self.parent.rotationMatrix)
    
    def draw(self):
        glUniformMatrix4fv(MODEL_LOC,1,GL_FALSE,self.model)
        glBindVertexArray(WALL_MODELS[self.type].getVAO())
        glBindTexture(GL_TEXTURE_2D,WALL.getTexture())
        glDrawArrays(GL_TRIANGLES,0,WALL_MODELS[self.type].getVertexCount())

class Ball:
    def __init__(self,x,y,parent):
        self.parent = parent
        self.x = x
        self.y = y
        self.z = 0
        self.velocity = [0,0]
    
    def update(self):
        #first translate to position on board, then rotate with the board
        translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([self.x,self.y,self.z]))
        self.model = pyrr.matrix44.multiply(translation,self.parent.rotationMatrix)
        acceleration = [-0.1*self.parent.rot_y,0.1*self.parent.rot_x]
        self.velocity[0] += 0.01*acceleration[0]
        self.velocity[1] += 0.01*acceleration[1]

        cmd_vel_x = self.velocity[0]
        cmd_vel_y = self.velocity[1]

        testX = self.x + self.velocity[0] + 8*np.sign(self.velocity[0])
        testY = self.y + self.velocity[1] + 8*np.sign(self.velocity[1])

        nextX = self.x + self.velocity[0]
        nextY = self.y + self.velocity[1]

        #check x direction. if collision then bounch, else move typically
        resultsColX = self.parent.collideWall(testX, self.y, nextX, nextY, cmd_vel_x, cmd_vel_y)
        if resultsColX[2]:
            self.velocity[0] *= -0.25
        else:
            self.velocity[0], self.velocity[1] = resultsColX[0], resultsColX[1]
        
        #check y direction
        resultsColY = self.parent.collideWall(self.x, testY, nextX, nextY, cmd_vel_x, cmd_vel_y)
        if resultsColY[2]:
            self.velocity[1] *= -0.25
        else:
            self.velocity[0], self.velocity[1] = resultsColY[0], resultsColY[1]

        self.x += self.velocity[0]
        self.y += self.velocity[1]
    
    def draw(self):
        glUniformMatrix4fv(MODEL_LOC,1,GL_FALSE,self.model)
        glBindVertexArray(BALL_MODEL.getVAO())
        glBindTexture(GL_TEXTURE_2D,BALL.getTexture())
        glDrawArrays(GL_TRIANGLES,0,BALL_MODEL.getVertexCount())

class Hole:
    def __init__(self, x, y, parent):
        self.parent = parent
        self.x = x
        self.y = y
        self.z = 0

    def update(self):
        # first translate to position on board, then rotate with the board
        translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([self.x, self.y, self.z]))
        self.model = pyrr.matrix44.multiply(translation, self.parent.rotationMatrix)

    def draw(self):
        glUniformMatrix4fv(MODEL_LOC, 1, GL_FALSE, self.model)
        glBindVertexArray(HOLE_MODEL.getVAO())
        glBindTexture(GL_TEXTURE_2D, HOLE.getTexture())
        glDrawArrays(GL_TRIANGLES, 0, HOLE_MODEL.getVertexCount())
