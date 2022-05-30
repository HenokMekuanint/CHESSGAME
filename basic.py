import glfw
import OpenGL.GL.shaders
import pyrr
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import numpy as np
import os


class Cube:
    def __init__(self):
        # initialize glfw
        if not glfw.init():
            return
        window = glfw.create_window(800, 600, "CHESS GAME", None, None)
        if not window:
            glfw.terminate()
            return

        glfw.make_context_current(window)
        #        positions        colors
        cube = [-0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
                0.5, -0.5, 0.5, 0.0, 1.0, 0.5,
                0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
                -0.5, 0.5, 0.5, 1.0, 1.0, 0.0,

                -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                0.5, -0.5, -0.5, 0.0, 1.0, 0.5,
                0.5, 0.5, -0.5, 0.0, 0.0, 1.0,
                -0.5, 0.5, -0.5, 1.0, 1.0, 1.0]

        cube = np.array(cube, dtype=np.float32)

        indices = [0, 1, 2, 2, 3, 0,
                   4, 5, 6, 6, 7, 4,
                   4, 5, 1, 1, 0, 4,
                   6, 7, 3, 3, 2, 6,
                   5, 6, 2, 2, 1, 5,
                   7, 4, 0, 0, 3, 7]

        indices = np.array(indices, dtype=np.uint32)

        vertex_shader = """
           #version 330
           in vec3 position;
           in vec3 color;
           uniform mat4 transform;
           out vec3 newColor;
           void main()
           {
               gl_Position = transform * vec4(position, 1.0f);
               newColor = color;
           }
           """

        fragement_shader = """
           #version 330
           in vec3 newColor;
           out vec4 outColor;
           void main()
           {
               outColor = vec4(newColor, 1.0f);
           }
           """
        shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                                  OpenGL.GL.shaders.compileShader(fragement_shader, GL_FRAGMENT_SHADER))

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, 192, cube, GL_STATIC_DRAW)

        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 144, indices, GL_STATIC_DRAW)

        position = glGetAttribLocation(shader, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        color = glGetAttribLocation(shader, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        glUseProgram(shader)

        glClearColor(0.2, 0.3, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        while not glfw.window_should_close(window):
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            rot_x = pyrr.Matrix44.from_x_rotation(0.5)
            rot_y = pyrr.Matrix44.from_y_rotation(1)

            transformLoc = glGetUniformLocation(shader, "transform")
            glUniformMatrix4fv(transformLoc, 1, GL_FALSE, rot_x * rot_y)

            glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

            glfw.swap_buffers(window)

        glfw.terminate()

    def getFileContents(self, filename):
        p = os.path.join(os.getcwd(), "shaders", filename)
        return open(p, 'r').read()


if __name__ == "__main__":
    Cube()
