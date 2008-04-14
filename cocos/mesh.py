#
# Los Cocos: An extension for Pyglet
# http://code.google.com/p/los-cocos/
#
'''Mesh effects'''

import pyglet
from pyglet import image
from pyglet.gl import *

from director import director
import framegrabber

__all__ = ['Mesh', ]

class Mesh(object):
    """
    A Scene that takes two scenes and makes a transition between them
    """
    texture = None
    
    def __init__(self):
        super(Mesh, self).__init__()
        self.active = False

    def init( self, x_quads=4, y_quads=4 ):

        x = director.window.width
        y = director.window.height

        self.x_quads = x_quads
        self.y_quads = y_quads

        if self.texture is None:
            self.texture = image.Texture.create_for_size(
                    GL_TEXTURE_2D, x, 
                    y, GL_RGB)
        
        self.grabber = framegrabber.TextureGrabber()
        self.grabber.grab(self.texture)

        x_step = x / (x_quads)
        y_step = y / (y_quads)

#        w = float(x)/self.texture.tex_coords[3]
#        h = float(y)/self.texture.tex_coords[7]

        w = float(self.texture.width)
        h = float(self.texture.height)

        vertex_points = []
        vertex_points_idx = []
        texture_points_idx = []
        texture_points = []
        index_points = []

        for x in range(0,x_quads+1):
            for y in range(0,y_quads+1):
                vertex_points_idx += [-1,-1]
                texture_points_idx += [-1,-1]

        for x in range(0, x_quads):
            for y in range(0, y_quads):
                x1 = x*x_step 
                x2 = x1 + x_step
                y1 = y*y_step
                y2 = y1 + y_step
              

                #  d <-- c
                #        ^
                #        |
                #  a --> b 
                index_points += [ x*(x_quads+1)+y, (x+1)*(x_quads+1)+(y), (x+1) * (x_quads+1) + (y+1), x*(x_quads+1)+(y+1) ]

                vertex_points_idx[ (x * (x_quads+1) + y) * 2 ] = x1
                vertex_points_idx[ (x * (x_quads+1) + y) * 2 + 1 ] = y1
                vertex_points_idx[ ((x+1) * (x_quads+1) + y) * 2 ] = x2
                vertex_points_idx[ ((x+1) * (x_quads+1) + y) * 2 + 1 ] = y1
                vertex_points_idx[ ((x+1) * (x_quads+1) + y+1) * 2 ] = x2
                vertex_points_idx[ ((x+1) * (x_quads+1) + y+1) * 2 + 1 ] = y2
                vertex_points_idx[ (x * (x_quads+1) + y+1) * 2 ] = x1
                vertex_points_idx[ (x * (x_quads+1) + y+1) * 2 + 1 ] = y2

                texture_points_idx[ (x * (x_quads+1) + y) * 2 ] = x1/w
                texture_points_idx[ (x * (x_quads+1) + y) * 2 + 1 ] = y1/h
                texture_points_idx[ ((x+1) * (x_quads+1) + y) * 2 ] = x2/w
                texture_points_idx[ ((x+1) * (x_quads+1) + y) * 2 + 1 ] = y1/h
                texture_points_idx[ ((x+1) * (x_quads+1) + y+1) * 2 ] = x2/w
                texture_points_idx[ ((x+1) * (x_quads+1) + y+1) * 2 + 1 ] = y2/h
                texture_points_idx[ (x * (x_quads+1) + y+1) * 2 ] = x1/w
                texture_points_idx[ (x * (x_quads+1) + y+1) * 2 + 1 ] = y2/h

                vertex_points += [x1, y1, x2, y1, x2, y2, x1, y2]
                texture_points += [x1/w, y1/h, x2/w, y1/h, x2/w, y2/h, x1/w, y2/h]


#        print index_points
#        print vertex_points_idx, len(vertex_points_idx)
#        print texture_points_idx, len(texture_points_idx)
#        print texture_points, len(texture_points)

        self.vertex_list = pyglet.graphics.vertex_list(x_quads*y_quads*4, "t2f", "v2i/stream")
        self.vertex_points = vertex_points[:]
        self.vertex_list.vertices = vertex_points
        self.vertex_list.tex_coords = texture_points

        # optimization: using index vertex list
        self.vertex_list_idx = pyglet.graphics.vertex_list_indexed((x_quads+1)*(y_quads+1), index_points, "t2f", "v2i/stream")
        self.vertex_points_idx = vertex_points_idx[:]
        self.vertex_list_idx.vertices = vertex_points_idx
        self.vertex_list_idx.tex_coords = texture_points_idx

    def before_draw( self ):
        # capture before drawing
        self.grabber.before_render(self.texture)


    def after_draw( self ):
        # capture after drawingg
        self.grabber.after_render(self.texture)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.blit()

    def blit(self ):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)
        glPushAttrib(GL_COLOR_BUFFER_BIT)

        self.vertex_list.draw(pyglet.gl.GL_QUADS)
#        self.vertex_list_idx.draw(pyglet.gl.GL_QUADS)

        glPopAttrib()
        glDisable(self.texture.target)
