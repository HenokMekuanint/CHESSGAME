# play.py (start game here)
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Game
def main ():
  game = Game.Game ()
  game.start ()
main ()