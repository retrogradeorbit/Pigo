from unittest import TestCase, main
import sys, random

from OpenGL.GL import *
from SDL import *
import PIL

from Tex import Tex
from Texture import Texture

class TexTest(TestCase):
    def setUp(self):
        # initialise the opengl
        if SDL_Init(SDL_INIT_VIDEO) < 0:            print "Unable to init SDL: %s\n", SDL_GetError()            sys.exit(1)        
        SDL_ShowCursor(0)        SDL_WM_SetCaption(str(self.__class__),str(self.__class__))        
        self.screen = SDL_SetVideoMode(320, 200, 24, SDL.SDL_OPENGL)        assert(self.screen != None)        
        # on OSX Leopard, enables sync to vsync. UPDATE, no it doesn't        SDL_GL_SetAttribute(SDL_GL_SWAP_CONTROL, 1)
        
    def tearDown(self):
        SDL_Quit()
        
    def testConstructor(self):
        for size in [ (20,20), (200,200), (3,1000), (1000,3), (256,256),(32,128) ]:
            texture = Texture( PIL.Image.new( "RGBA", size ) )
            tex = Tex(texture)
            self.assert_(tex.width == size[0])
            self.assert_(tex.height == size[1])
        
    def testCoordinates(self):
        for num in range(256):
            x = 2**random.randint(0,10)
            y = 2**random.randint(0,10)
            texture = Texture( PIL.Image.new( "RGBA", (x,y) ) )
            tex = Tex(texture)
            self.assert_(tex.GetU0()==tex.GetV0()==0.0)
            self.assert_(tex.GetU1()==tex.GetV1()==1.0)
    
        for num in range(256):
            x = 2**random.randint(2,10)
            y = 2**random.randint(2,10)
            texture = Texture( PIL.Image.new( "RGBA", (x-1,y-1) ) )
            tex = Tex(texture)
            self.assert_(tex.GetU0()==tex.GetV0()==0.0)
            self.assert_(0.0<tex.GetU1()<1.0)
            self.assert_(0.0<tex.GetV1()<1.0)
    
        for num in range(256):
            x = 2**random.randint(2,10)
            y = 2**random.randint(2,10)
            texture = Texture( PIL.Image.new( "RGBA", (x/2+1,y/2+1) ) )
            tex = Tex(texture)
            self.assert_(tex.GetU0()==tex.GetV0()==0.0)
            self.assert_(0.0<tex.GetU1()<1.0)
            self.assert_(0.0<tex.GetV1()<1.0)
    
        
            
        
if __name__=="__main__":
    main()
