import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import numpy as np

def init():
    pygame.init()
    mywindow = (500, 500)
    pygame.display.set_mode(mywindow, DOUBLEBUF|OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)

    glBegin(GL_POINTS)
    
    glVertex2f(0.0, 0.0)

    glEnd()
    glFlush()

def draw():
    glClear(GL_COLOR_BUFFER_BIT)

       

def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        draw()
        pygame.display.flip()
        pygame.time.wait(10)



main()



