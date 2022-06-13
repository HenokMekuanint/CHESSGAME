from OpenGL.GL import *
from material import Material
from mesh import Mesh


class RenderObj:
    def __init__(self, objFile, texture):
        self.objFile=objFile
        self.texture=texture
        self.renderObj()
    def renderObj(self):
        obj=Mesh(self.objFile)
        texture=Material(self.texture)

        glBindVertexArray(obj.vao)
        glDrawArrays(GL_TRIANGLES, 0, obj.vertex_count)