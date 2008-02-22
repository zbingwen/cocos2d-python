
#
# framework libs
#

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cocos.director import director
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.effect import TextureFilterEffect
import pyglet


class PictureLayer(Layer):

    def __init__ (self, y):
        self.x = 100
        self.y = y
        self.speed = 35
        self.img = pyglet.image.load ('ball.png')
    
    def step (self, dt):
        self.x += self.speed * dt
        if self.x > 200 and self.speed > 0: self.speed = -self.speed
        if self.x < 100 and self.speed < 0: self.speed = -self.speed
        self.img.blit (self.x, self.y)

class MyEffect (TextureFilterEffect):
    def __init__ (self, scale=1.0):
        super (MyEffect, self).__init__ ()
        self.scale=scale

    def show (self):
        self.texture.blit (0, 0, width=director.window.width*self.scale)

if __name__ == "__main__":
    director.init()
    l1 = PictureLayer(50)
    l1.set_effect (MyEffect(0.5))
    l2 = PictureLayer(100)
    director.run( Scene (l1, l2) )

