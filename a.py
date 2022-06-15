
import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import pyrr
from camera import Camera
from material import  Material
from cube import Cube
from mesh import Mesh


cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True



class App:

 # |pygame.FULLSCREEN


    def __init__(self):
        #initialise pygame

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((WIDTH, HEIGHT), pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

        # pg.display.set_mode((WIDTH, HEIGHT), pg.OPENGL|pg.DOUBLEBUF)


        self.clock = pg.time.Clock()
        #initialise opengl
        glClearColor(0.1, 0.2, 0.2, 1)
        self.shader = self.createShader("vertex.txt", "fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        glEnable(GL_DEPTH_TEST)
        self.wood_texture = Material("textures/d.jpg")
        self.cube_mesh = Mesh("models/finalbord.obj")

        self.one = Material("textures/black.jpg")

        
        self.solider_1_right = Mesh("whitepices/finalsoliderrightup1.obj")
        self.solider_2_right = Mesh("whitepices/finalsoliderrightup2.obj")
        self.solider_3_right = Mesh("whitepices/finalsoliderrightup3.obj")
        self.solider_4_right = Mesh("whitepices/finalsoliderrightup4.obj")
        self.solider_5_right = Mesh("whitepices/finalsoliderrightup5.obj")
        self.solider_6_right = Mesh("whitepices/finalsoliderrightup6.obj")
        self.solider_7_right = Mesh("whitepices/finalsoliderrightup7.obj")
        self.solider_8_right = Mesh("whitepices/finalsoliderrightup8.obj")

        self.final_wall_right_far = Mesh("whitepices/finalwall.obj")
        self.final_diagonal_right_far = Mesh("whitepices/finaldiagonal.obj")
        self.final_horse_right_far = Mesh("whitepices/finalhorse.obj")
        self.final_queen_right_far = Mesh("whitepices/finalqueenrrightup8.obj")
        self.final_king_right_far = Mesh("whitepices/finalking.obj")

        self.finalhorsenear = Mesh("whitepices/finalhorsenear.obj")
        self.final_wall_near = Mesh("whitepices/finallwallnear.obj")
        self.final_diagonal_near = Mesh("whitepices/finaldiagonalnear.obj")


        self.cube = Cube(
            
            position = [-1.5,0,-20],
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
        # cube_pos = pyrr.matrix44.create_from_translation(np.array(self.cube.position*2))
        proj_loc = glGetUniformLocation(self.shader, "projection")
        view_loc = glGetUniformLocation(self.shader, "view")
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)

        running = True
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        while (running):
            #check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
                elif  event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False

                if event.type == pg.VIDEORESIZE:
                    glViewport(0, 0, event.w, event.h)
                    projection = pyrr.matrix44.create_perspective_projection_matrix(45, event.w / event.h, 0.1, 100)
                    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_a]:
                cam.process_keyboard("LEFT", 0.08)
            if keys_pressed[pg.K_d]:
                cam.process_keyboard("RIGHT", 0.08)
            if keys_pressed[pg.K_w]:
                cam.process_keyboard("FORWARD", 0.08)
            if keys_pressed[pg.K_s]:
                cam.process_keyboard("BACKWARD", 0.08)
                    
            #update cube
            self.cube.eulers[2] += 0.25
            if self.cube.eulers[2] > 360:
                self.cube.eulers[2] -= 360
            ct = pg.time.get_ticks() / 1000

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            view = cam.get_view_matrix()
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

            rot_y = pyrr.Matrix44.from_y_rotation(0.8 * ct)


            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)

            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.create_from_translation([0, 0, -11])

            #the below is the chess boared

            glUniformMatrix4fv(self.modelMatrixLocation,1,GL_FALSE,model_transform)
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)
            # self.one.use()

            #the below are the white pices

            glBindVertexArray(self.solider_1_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_1_right.vertex_count)
            # self.one.use()

            glBindVertexArray(self.solider_2_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_1_right.vertex_count)
            # self.one.use()

            glBindVertexArray(self.solider_3_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_1_right.vertex_count)
            # self.one.use()

            glBindVertexArray(self.solider_4_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_1_right.vertex_count)
            # self.one.use()

            glBindVertexArray(self.solider_5_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_1_right.vertex_count)
            # self.one.use()

            glBindVertexArray(self.solider_5_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_1_right.vertex_count)
            # self.one.use()

            glBindVertexArray(self.solider_6_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_1_right.vertex_count)
            # self.one.use()

            glBindVertexArray(self.solider_7_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_1_right.vertex_count)
            # self.one.use()

            glBindVertexArray(self.solider_8_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_1_right.vertex_count)
            # self.one.use()

            glBindVertexArray(self.final_wall_right_far.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_wall_right_far.vertex_count)
            # self.one.use()

            glBindVertexArray(self.final_diagonal_right_far.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_diagonal_right_far.vertex_count)
            # self.one.use()

            glBindVertexArray(self.final_queen_right_far.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_queen_right_far.vertex_count)
            # self.one.use()
           
            glBindVertexArray(self.final_king_right_far.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_king_right_far.vertex_count)
            # self.one.use()

            glBindVertexArray(self.final_horse_right_far.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_horse_right_far.vertex_count)
            # self.one.use()
           
            glBindVertexArray(self.finalhorsenear.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_horse_right_far.vertex_count)
            # self.one.use()

            glBindVertexArray(self.final_diagonal_near.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_horse_right_far.vertex_count)

            glBindVertexArray(self.final_wall_near.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_horse_right_far.vertex_count)
            self.wood_texture.use()

            ct = pg.time.get_ticks() / 1000
            view = cam.get_view_matrix()
            # glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)



            
            pg.display.flip()      


            #timing
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.cube_mesh.destroy()
        self.wood_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


if __name__ == '__main__':
    App()


