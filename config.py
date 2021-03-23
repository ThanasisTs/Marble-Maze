import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
from OpenGL.GLU import *
import numpy as np
import pyrr
import pywavefront as pwf
from assets import *

pg.init()

display = (600, 600)
screen = pg.display.set_mode(display,pg.OPENGL|pg.DOUBLEBUF)
clock = pg.time.Clock()

glClearColor(0,0.0,0.0,1)

with open("shaders/vertex.txt",'r') as f:
    vertex_src = f.readlines()
with open("shaders/fragment.txt",'r') as f:
    fragment_src = f.readlines()
shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),
                        compileShader(fragment_src,GL_FRAGMENT_SHADER))
glUseProgram(shader)

#get a handle to the rotation matrix from the shader
MODEL_LOC = glGetUniformLocation(shader,"model")
VIEW_LOC = glGetUniformLocation(shader,"view")
PROJ_LOC = glGetUniformLocation(shader,"projection")
LIGHT_LOC = glGetUniformLocation(shader,"lightPos")

glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_CULL_FACE)

########################MODELS######################################
BOARD_MODEL = ObjModel("models/board.obj")
BALL_MODEL = ObjModel("models/ball.obj")
WALL_MODELS = [ObjModel("models/wall.obj"), ObjModel("models/wall_half_1_big.obj"),
				ObjModel("models/wall_half_2_big.obj"), ObjModel("models/wall_half_corner_1_big.obj"),
				ObjModel("models/wall_half_corner_2_big.obj")]

########################TEXTURES####################################
BOARD = Texture("textures/board.jpg")
WALL = Texture("textures/wall.jpg")
BALL = Texture("textures/glass.png")
####################################################################

#(field of view, aspect ratio,near,far)

cameraPos = pyrr.Vector3([0,0,600])
up = pyrr.Vector3([0.0,1.0,0.0]) 
cameraRight = pyrr.vector.normalise(pyrr.vector3.cross(up, cameraPos))
cameraUp = pyrr.vector3.cross(cameraPos, cameraRight)
viewMatrix = pyrr.matrix44.create_look_at(cameraPos, pyrr.Vector3([0,0,0]), cameraUp)
projection = pyrr.matrix44.create_perspective_projection_matrix(45,display[0]/display[1],320,1500)
glUniformMatrix4fv(PROJ_LOC,1,GL_FALSE,projection)
glUniformMatrix4fv(VIEW_LOC,1,GL_FALSE,viewMatrix)

lightPosition = pyrr.Vector3([-400.0,200.0,300.0])
glUniform3f(LIGHT_LOC,-400.0,200.0,300.0)