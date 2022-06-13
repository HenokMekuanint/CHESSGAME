
import numpy as np
import pygame as pg
import pyrr
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from cube import Cube
from render import RenderObj

class App:
    def __init__(self):
        #initialise pygame
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((640,480), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        #initialise opengl
        glClearColor(0.1, 0.2, 0.2, 1)
        self.shader = self.createShader("vertex.txt", "fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        glEnable(GL_DEPTH_TEST)


        # self.wood_texture = Material("d.jpg")
        # self.cube_mesh = Mesh("new22.obj")
        # self.black_bishop_mesh = Mesh("blackpices/blackBishop.obj")


        self.cube = Cube(
            
            position = [0,-0.7,-3],
            eulers = [0,0,0]
        )

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 640/480, 
            near = 0.1, far = 10, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader,"projection"),
            1, GL_FALSE, projection_transform
        )
        self.modelMatrixLocation = glGetUniformLocation(self.shader,"model")
        self.mainLoop()

    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader

    def mainLoop(self):
        running = True
        while (running):
            #check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            
            #update cube
            self.cube.eulers[2] += 0.25
            if self.cube.eulers[2] > 360:
                self.cube.eulers[2] -= 360
            
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)

            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            """
                pitch: rotation around x axis
                roll:rotation around z axis
                yaw: rotation around y axis
            """
            # model_transform = pyrr.matrix44.multiply(
            #     m1=model_transform, 
            #     m2=pyrr.matrix44.create_from_eulers(
            #         eulers=np.radians(self.cube.eulers), dtype=np.float32
            #     )
            # )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform, 
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array(self.cube.position),dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation,1,GL_FALSE,model_transform)

            RenderObj("new22.obj", "d.jpg")
            RenderObj("blackpices/blackBishop.obj", "black.jpeg")
            # glBindVertexArray(self.cube_mesh.vao)
            # glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

            # glBindVertexArray(self.black_bishop_mesh.vao)
            # glDrawArrays(GL_TRIANGLES, 0, self.black_bishop_mesh.vertex_count)

            # glBindVertexArray(self.black_king_mesh.vao)
            # glDrawArrays(GL_TRIANGLES, 0, self.black_king_mesh.vertex_count)

            pg.display.flip()            # self.wood_texture.use()


            #timing
            self.clock.tick(60)
        self.quit()

    def quit(self):
        # self.cube_mesh.destroy()
        # self.wood_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


if __name__ == '__main__':
    App()


