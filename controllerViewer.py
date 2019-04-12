import pyglet
from pyglet.gl import *


class ControllerViewer(object):
    def __init__(self, display=None):
        self.window = None
        self.isopen = False
        self.display = display
        self.image = pyglet.resource.image('controller.jpg')

    def actionshow(self, arr):
        if self.window is None:
            # height, width = image.get_texture

            self.window = pyglet.window.Window(width=190, height=190,
                                               display=self.display, vsync=False, resizable=True)
            self.width = self.window.width
            self.height = self.window.height
            self.isopen = True

            @self.window.event
            def on_resize(width, height):
                self.width = width
                self.height = height

            @self.window.event
            def on_close():
                self.isopen = False

        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        texture = self.image.get_texture()
        texture.width = self.width
        texture.height = self.height
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()

        texture.blit(0, 0)  # draw
        rr = arr[0]
        up = 255*rr[4]
        bkey = 255*rr[0]
        akey = 255*rr[1]
        dkey = 255*rr[5]
        left = 255*rr[6]
        right = 255*rr[7]
        # b

        pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_FAN,
                             ('v2i', (130, 70, 130, 90, 150, 90, 150, 70)),
                             ('c4B', (0, 0, bkey, 255) * 4))
        # a
        pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_FAN,
                             ('v2i', (110, 60, 110, 80, 130, 80, 130, 60)),
                             ('c4B', (0, akey, 0, 255) * 4))
        # down

        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLE_FAN,('v2i', (50, 60, 55, 70, 45, 70)),('c4B',(dkey, 0, 0, 255) * 3))
        # up
        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLE_FAN,
                             ('v2i', (50, 100, 55, 90, 45, 90)),
                             ('c4B', (up, 0, 0, 255) * 3))
        # left
        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLE_FAN,
                             ('v2i', (30, 80, 40, 85, 40, 75)),
                             ('c4B', (left, 0, 0, 255) * 3))
        # right
        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLE_FAN,
                             ('v2i', (70, 80, 60, 85, 60, 75)),
                             ('c4B', (right, 0, 0, 255) * 3))
        self.window.flip()

    def close(self):
        if self.isopen and sys.meta_path:
            # ^^^ check sys.meta_path to avoid 'ImportError: sys.meta_path is None, Python is likely shutting down'
            self.window.close()
            self.isopen = False

    def __del__(self):
        self.close()
