import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
from OpenGL.GLU import *
import numpy as np
import pyrr
import pywavefront as pwf
from assets import *

pg.font.init()
# font = pg.font.SysFont("Grobold", 20)  # Assign it to a variable font


pg.init()

display = (800, 800)
screen = pg.display.set_mode(display,pg.OPENGL|pg.DOUBLEBUF)
clock = pg.time.Clock()

font = pg.font.Font('freesansbold.ttf', 32)

texts, textsRect = [], []
for i in range(5):
	texts.append(font.render("Game starts in {}...".format(i+1), True, (255, 255, 255)))
	textsRect.append(texts[-1].get_rect())
	textsRect[-1].center = (100, 100)


glClearColor(0.1, 0.2, 0.3, 1)

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
BOARD_MODEL = ObjModel("/home/thanasis/marble_maze/maze3D/models/board.obj")
BALL_MODEL = ObjModel("models/ball.obj")
WALL_MODELS = [ObjModel("models/wall.obj"), ObjModel("models/wall_half_1_big.obj"),
				ObjModel("models/wall_half_2_big.obj"), ObjModel("models/wall_half_corner_1_big.obj"),
				ObjModel("models/wall_half_corner_2_big.obj")]
HOLE_MODEL = ObjModel("/home/thanasis/marble_maze/maze3D/models/hole.obj")
TEXT_MODEL = ObjModel("models/text.obj")
########################TEXTURES####################################
BOARD = Texture("/home/thanasis/marble_maze/maze3D/textures/board_white.png")
WALL = Texture("/home/thanasis/marble_maze/maze3D/textures/wall_simple.jpg")
BALL = Texture("/home/thanasis/marble_maze/maze3D/textures/glass.png")
HOLE = Texture("/home/thanasis/marble_maze/maze3D/textures/green.png")
TEXT = [Texture("textures/5_secs.png"), Texture("textures/4secs.png"), Texture("textures/3secs.png"), 
		Texture("textures/2secs.png"), Texture("textures/1secs.png"), Texture("textures/play.png")]
####################################################################

#(field of view, aspect ratio,near,far)

# cameraPos = pyrr.Vector3([0,0,600])
# up = pyrr.Vector3([0.0,1.0,0.0]) 
# cameraRight = pyrr.vector.normalise(pyrr.vector3.cross(up, cameraPos))
# cameraUp = pyrr.vector3.cross(cameraPos, cameraRight)
# viewMatrix = pyrr.matrix44.create_look_at(cameraPos, pyrr.Vector3([0,0,0]), cameraUp)
# projection = pyrr.matrix44.create_perspective_projection_matrix(45,display[0]/display[1],320,1500)
# glUniformMatrix4fv(PROJ_LOC,1,GL_FALSE,projection)
# glUniformMatrix4fv(VIEW_LOC,1,GL_FALSE,viewMatrix)

# lightPosition = pyrr.Vector3([-400.0,200.0,300.0])
# glUniform3f(LIGHT_LOC,-400.0,200.0,300.0)

# control cameraPos, viewMatrix, projection for better 3D view adjusting
cameraPos = pyrr.Vector3([80, 80, 500])
up = pyrr.Vector3([0.0, 1.0, 0.0])
viewMatrix = pyrr.matrix44.create_look_at(cameraPos, pyrr.Vector3([80, 80, 0]), up)
glUniformMatrix4fv(VIEW_LOC, 1, GL_FALSE, viewMatrix)
projection = pyrr.matrix44.create_perspective_projection_matrix(80, 800 / 800, 1, 7000)
glUniformMatrix4fv(PROJ_LOC, 1, GL_FALSE, projection)
glUniform3f(LIGHT_LOC, -400, 200, 300)