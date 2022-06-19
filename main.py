
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



    def __init__(self):

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((WIDTH, HEIGHT), pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)



        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.2, 0.2, 1)
        self.shader = self.createShader("vertex.txt", "fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        glEnable(GL_DEPTH_TEST)
        self.wood_texture = Material("textures/d.jpg")
        self.cube_mesh = Mesh("models/finalbord.obj")

        self.one = Material("textures/black.jpg")
        self.two = Material("textures/white.jpg")
        self.table_Texure=Material("table/woodred.jpg")
        #the below are the whitepices
        
        self.solider_1_right = Mesh("whitepices/finalsoliderrightup1.obj")
        self.solider_2_right = Mesh("whitepices/finalsoliderrightup2.obj")
        self.solider_3_right = Mesh("whitepices/finalsoliderrightup3.obj")
        self.solider_4_right = Mesh("whitepices/finalsoliderrightup4.obj")
        self.solider_5_right = Mesh("whitepices/finalsoliderrightup5.obj")
        self.solider_6_right = Mesh("whitepices/finalsoliderrightup6.obj")
        self.solider_7_right = Mesh("whitepices/finalsoliderrightup7.obj")
        self.solider_8_right = Mesh("whitepices/finalsoliderrightup8.obj")
        self.final_wall_right_far = Mesh("whitepices/finalwall.obj")
        self.final_diagonal_right_far = Mesh("whitepices/finaldiagonalfar.obj")
        self.final_horse_right_far = Mesh("whitepices/finalhorsefar.obj")
        self.final_queen_right_far = Mesh("whitepices/finalqueenrrightup8.obj")
        self.final_king_right_far = Mesh("whitepices/finalking.obj")
        self.finalhorsenear = Mesh("whitepices/finalhorsenear.obj")
        self.final_wall_near = Mesh("whitepices/finalwallnear.obj")
        self.final_diagonal_near = Mesh("whitepices/finaldiagonalnear.obj")


        #the below are the left elements

        self.solider_8_left = Mesh("blackpices/finalsoliiderleft1.obj")
        self.solider_7_left = Mesh("blackpices/finalsoliiderleft2.obj")
        self.solider_5_left = Mesh("blackpices/finalsoliiderleft3.obj")
        self.solider_4_left = Mesh("blackpices/finalsoliiderleft4.obj")
        self.solider_3_left = Mesh("blackpices/finalsoliiderleft5.obj")
        self.solider_6_left = Mesh("blackpices/finalsoliiderleft6.obj")
        self.solider_2_left = Mesh("blackpices/finalsoliiderleft7.obj")
        self.solider_1_left = Mesh("blackpices/finalsoliiderleft8.obj")

        self.final_wall_left_near = Mesh("blackpices/finalwallfar.obj")
        self.final_wall_far_left = Mesh("blackpices/finalwallnear.obj")

        self.final_diagonal_left_near = Mesh("blackpices/finaldiagonalfar.obj")
        self.final_diagonal_far_left = Mesh("blackpices/finaldiagonalnear.obj")

        self.final_horse_left_near = Mesh("blackpices/finalhorsefar.obj")
        self.finalhorsenear_left = Mesh("blackpices/finalhorsenear.obj")

        self.final_queen_left = Mesh("blackpices/finalqueennear.obj")
        self.final_king_left = Mesh("blackpices/finalkingnear.obj")


        #the below is the table
        self.table=Mesh("table/untitled.obj")
        
        #below is the environment
        # self.=Mesh("newenv/env.obj")
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
        proj_loc = glGetUniformLocation(self.shader, "projection")
        view_loc = glGetUniformLocation(self.shader, "view")
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)

        running = True
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        while (running):
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
                    
            self.cube.eulers[2] += 0.25
            if self.cube.eulers[2] > 360:
                self.cube.eulers[2] -= 360
            ct = pg.time.get_ticks() / 1000

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            view = cam.get_view_matrix()
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)

            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.create_from_translation([0, 0, -11])

            #the below is the chess boared

            glUniformMatrix4fv(self.modelMatrixLocation,1,GL_FALSE,model_transform)
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)
            self.one.use()

            #the below are the white pices

            glBindVertexArray(self.solider_1_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_1_right.vertex_count)
            self.one.use()

            glBindVertexArray(self.solider_2_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_2_right.vertex_count)
            self.one.use()

            glBindVertexArray(self.solider_3_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_3_right.vertex_count)
            self.one.use()

            glBindVertexArray(self.solider_4_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_4_right.vertex_count)
            self.one.use()

            glBindVertexArray(self.solider_5_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_5_right.vertex_count)
            self.one.use()


            # self.one.use()

            glBindVertexArray(self.solider_6_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_6_right.vertex_count)
            self.one.use()

            glBindVertexArray(self.solider_7_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_7_right.vertex_count)
            self.one.use()

            glBindVertexArray(self.solider_8_right.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.solider_8_right.vertex_count)
            self.one.use()

            glBindVertexArray(self.final_wall_right_far.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_wall_right_far.vertex_count)
            self.one.use()

            glBindVertexArray(self.final_diagonal_right_far.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_diagonal_right_far.vertex_count)
            self.one.use()

            glBindVertexArray(self.final_queen_right_far.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_queen_right_far.vertex_count)
            self.one.use()
           
            glBindVertexArray(self.final_king_right_far.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_king_right_far.vertex_count)
            self.one.use()

            glBindVertexArray(self.final_horse_right_far.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_horse_right_far.vertex_count)
            self.one.use()
           
            glBindVertexArray(self.finalhorsenear.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.finalhorsenear.vertex_count)
            self.one.use()

            glBindVertexArray(self.final_diagonal_near.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_diagonal_near.vertex_count)
            self.one.use()

            glBindVertexArray(self.final_wall_near.vao)
            glDrawArrays(GL_TRIANGLES, 0,self.final_wall_near.vertex_count)
            self.one.use()

            #the left side of pices are below
            self.two.use()
            glBindVertexArray(self.solider_1_left.vao)
            glDrawArrays(GL_TRIANGLES, 0,self.solider_1_left.vertex_count)

            glBindVertexArray(self.solider_2_left.vao)
            glDrawArrays(GL_TRIANGLES, 0,self.solider_2_left.vertex_count)

            glBindVertexArray(self.solider_3_left.vao)
            glDrawArrays(GL_TRIANGLES, 0,self.solider_3_left.vertex_count)

            glBindVertexArray(self.solider_4_left.vao)
            glDrawArrays(GL_TRIANGLES, 0,self.solider_4_left.vertex_count)

            glBindVertexArray(self.solider_5_left.vao)
            glDrawArrays(GL_TRIANGLES, 0,self.solider_5_left.vertex_count)

            glBindVertexArray(self.solider_6_left.vao)
            glDrawArrays(GL_TRIANGLES, 0,self.solider_6_left.vertex_count)


            glBindVertexArray(self.solider_7_left.vao)
            glDrawArrays(GL_TRIANGLES, 0,self.solider_7_left.vertex_count)

            glBindVertexArray(self.solider_8_left.vao)
            glDrawArrays(GL_TRIANGLES, 0,self.solider_8_left.vertex_count)

            glBindVertexArray( self.final_wall_left_near.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_wall_left_near.vertex_count)

            glBindVertexArray( self.final_wall_far_left.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_wall_far_left.vertex_count)

            glBindVertexArray( self.final_diagonal_left_near.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_diagonal_left_near.vertex_count)

            glBindVertexArray(self.final_diagonal_far_left.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_diagonal_far_left.vertex_count)

            
            glBindVertexArray(self.final_horse_left_near.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_horse_left_near.vertex_count)
            
            glBindVertexArray(self.finalhorsenear_left.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.finalhorsenear_left.vertex_count)

            
            glBindVertexArray(self.final_queen_left.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.final_queen_left.vertex_count)

           
            glBindVertexArray( self.final_king_left.vao)
            glDrawArrays(GL_TRIANGLES, 0,  self.final_king_left.vertex_count)

            self.table_Texure.use()
            glBindVertexArray( self.table.vao)
            glDrawArrays(GL_TRIANGLES, 0,  self.table.vertex_count)
            self.wood_texture.use()

            ct = pg.time.get_ticks() / 1000
            view = cam.get_view_matrix()



            
            pg.display.flip()      


            #timing
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.cube_mesh.destroy()
        self.wood_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()
    def createAndAddVertexArrayData(vertexArrayObject, data, attributeIndex):
        glBindVertexArray(vertexArrayObject)
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glVertexAttribPointer(attributeIndex, len(data[0]), GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(attributeIndex)

        # Unbind the buffers again to avoid unintentianal GL state corruption (this is something that can be rather inconventient to debug)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        return buffer
def beginRedraw(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -10.0)
    glRotatef(self.rotation[0],1.0,0.0,0.0)
    glRotatef(self.rotation[1],0.0,0.0,1.0)

    glDisable(GL_COLOR_MATERIAL)

    glClearStencil(0)
    glClear(GL_STENCIL_BUFFER_BIT)
    glStencilFunc(GL_ALWAYS,0,0x1)
    glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)
    #self.drawBoardBottom()


    glStencilFunc(GL_ALWAYS,1,0x1)
    glStencilOp(GL_REPLACE,GL_REPLACE,GL_REPLACE)


def endRedraw(self):  
    glEnable(GL_COLOR_MATERIAL)
    glPushMatrix()
    glMultMatrixd(self.matrixForSchadow)

    glStencilFunc(GL_EQUAL,1,0x1)
    glStencilOp(GL_KEEP,GL_KEEP,GL_INCR)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_LIGHTING)

    glPopMatrix()
    glEnable(GL_LIGHTING)
    glDisable(GL_BLEND)

    glStencilFunc(GL_ALWAYS,1,0x1)
    glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)
    RF_Transparent = 1
    RF_AlphaTested = 2
    RF_Opaque = 4
    RF_All = RF_Opaque | RF_AlphaTested | RF_Transparent

    AA_Position = 0
    AA_Normal = 1
    AA_TexCoord = 2
    AA_Tangent = 3
    AA_Bitangent = 4

    TU_Diffuse = 0
    TU_Opacity = 1
    TU_Specular = 2
    TU_Normal = 3
    TU_Max = 4

    texturesByName = {}
    texturesById = {}

    def __init__(self, fileName):
        self.defaultTextureOne = glGenTextures(1);
        glBindTexture(GL_TEXTURE_2D, self.defaultTextureOne);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_FLOAT, [1.0, 1.0, 1.0, 1.0]);

        self.defaultNormalTexture = glGenTextures(1);
        glBindTexture(GL_TEXTURE_2D, self.defaultNormalTexture);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, 1, 1, 0, GL_RGBA, GL_FLOAT, [0.5, 0.5, 0.5, 1.0]);
        glBindTexture(GL_TEXTURE_2D, 0);

        self.overrideDiffuseTextureWithDefault = False
        self.load(fileName)

        self.defaultShader = lu.buildShader(self.defaultVertexShader, self.defaultFragmentShader, ObjModel.getDefaultAttributeBindings())
        glUseProgram(self.defaultShader)
        ObjModel.setDefaultUniformBindings(self.defaultShader)
        glUseProgram(0)

    def load(self, fileName):
        basePath,_ = os.path.split(fileName)
        with open(fileName, "r") as inFile:
            self.loadObj(inFile.readlines(), basePath)

    def loadObj(self, objLines, basePath):
        positions = []
        normals = []
        uvs = []
        materialChunks = []
        materials = {}
        
        for l in objLines:
            #1 standardize line
            if len(l) > 0 and l[:1] != "#":
                tokens = l.split()
                if len(tokens):
                    if tokens[0] == "mtllib":
                        assert len(tokens) >= 2
                        materialName = " ".join(tokens[1:])
                        materials = self.loadMaterials(os.path.join(basePath, materialName), basePath)
                    if tokens[0] == "usemtl":
                        assert len(tokens) >= 2
                        materialName = " ".join(tokens[1:])
                        if len(materialChunks) == 0 or materialChunks[-1][0]  != materialName:
                            materialChunks.append([materialName, []])
                    elif tokens[0] == "v":
                        assert len(tokens[1:]) >= 3
                        positions.append([float(v) for v in tokens[1:4]])
                    elif tokens[0] == "vn":
                        assert len(tokens[1:]) >= 3
                        normals.append([float(v) for v in tokens[1:4]])
                    elif tokens[0] == "vt":
                        assert len(tokens[1:]) >= 2
                        uvs.append([float(v) for v in tokens[1:3]])
                    elif tokens[0] == "f":
                        materialChunks[-1][1] += self.parseFace(tokens[1:])
        self.numVerts = 0
        for mc in materialChunks:
            self.numVerts += len(mc[1])
        
        self.positions = [None]*self.numVerts
        self.normals = [None]*self.numVerts
        self.uvs = [[0.0,0.0]]*self.numVerts
        self.tangents = [[0.0,1.0,0.0]]*self.numVerts
        self.bitangents = [[1.0,0.0,0.0]]*self.numVerts
        self.chunks = []

        start = 0
        end = 0
        self.materials = materials
        for matId, tris in materialChunks:
            material = materials[matId]
            renderFlags = 0
            if material["alpha"] != 1.0:
                renderFlags |= self.RF_Transparent 
            elif material["texture"]["opacity"] != -1:
                renderFlags |= self.RF_AlphaTested
            else:
                renderFlags |= self.RF_Opaque
            start = end
            end = start + int(len(tris)/3)

            chunkOffset = start * 3
            chunkCount = len(tris)

            for k in range(0,len(tris),3):
                for j in [0,1,2]:
                    p = positions[tris[k + j][0]]
                    oo = chunkOffset + k + j
                    self.positions[oo]= p
                    if tris[k + j][1] != -1:
                        self.uvs[oo] = uvs[tris[k + j][1]]
                    self.normals[oo] = normals[tris[k + j][2]]
            self.chunks.append((material, chunkOffset, chunkCount, renderFlags))
        
        self.vertexArrayObject = glGenVertexArrays(1)
        glBindVertexArray(self.vertexArrayObject)


    




if __name__ == '__main__':
    App()


