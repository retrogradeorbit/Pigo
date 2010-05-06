from unittest import TestCase, main
from Texture import Texture
import sys

from OpenGL.GL import *

# autodetect our backend
try:
	from SDL import *
	BACKEND = 'sdl'
except ImportError, ie:
	try:
		import pygame
		BACKEND = 'pygame'
	except ImportError, ie:
		raise Exception("no backend found")

import PIL

class TextureTest(TestCase):
        
    def testNameOnly(self):
        a = Texture( filename="Test name" )
        self.assert_( a.filename == "Test name" )
        
        # see that we have an id
        self.assert_( a.GetID() == None )
        self.assert_( a.GetID() == a.glid )
        self.assert_( a.width == a.GetWidth() == 0 )
        self.assert_( a.height == a.GetHeight() == 0 )
        
    def testNameAndImage(self):
        for mode in ["RGB","RGBA"]:
            for size in [ (8,8), (32,32), (128,128), (512,512), (8,512), (512,8) ]:
                image = PIL.Image.new(mode, size)
        
                texture = Texture( image=image, filename="Image %d by %d"%size )
                
                self.assert_( texture.image == texture.GetImage() )
                self.assert_( texture.image.size == size )
                self.assert_( texture.glid > 0 )
                
    def testImageScaleUp(self):
        for mode in ["RGB","RGBA"]:
            for size, scaled in [ 
                (   (9,13), (16,16)     ),
                (   (3,156), (4,256)    ),
                (   (45,18), (64,32)    ),
                (   (323,276), (512,512)  ),
                (   (643,576), (1024,1024) ),
            ]:
                image = PIL.Image.new(mode, size)
                
                texture = Texture( image=image, filename="Image %d by %d"%size)
                
                self.assert_( texture.image == texture.GetImage() )
                self.assert_( texture.image.size == scaled )
                self.assert_( texture.glid > 0 )
                
    def testMakeNonResidentEnsureResident(self):
        for mode in ["RGB","RGBA"]:
            for size in [ (8,8), (32,32), (128,128), (512,512), (8,512), (512,8), (1024,4) ]:
                image = PIL.Image.new(mode, size)
        
                texture = Texture( image=image, filename="Image %d by %d"%size )
                
                self.assert_( texture.image == texture.GetImage() )
                self.assert_( texture.image.size == size )
                self.assert_( texture.glid > 0 )
                
                for i in range(1000):
                    texture.MakeNonResident()
                    self.assert_( texture.glid == None )
                    texture.EnsureResident()
                    self.assert_( texture.glid > 0 )
					
					
if BACKEND == 'sdl':
	class SDLTestCase(TextureTest):	
		def setUp(self):
			# initialise the opengl
			if SDL_Init(SDL_INIT_VIDEO) < 0:
				print "Unable to init SDL: %s\n", SDL_GetError()
				sys.exit(1)
        
			SDL_ShowCursor(0)
			SDL_WM_SetCaption(str(self.__class__),str(self.__class__))
        
			self.screen = SDL_SetVideoMode(320, 200, 24, SDL.SDL_OPENGL)
			assert(self.screen != None)
        
			# on OSX Leopard, enables sync to vsync. UPDATE, no it doesn't
			SDL_GL_SetAttribute(SDL_GL_SWAP_CONTROL, 1)
        
		def tearDown(self):
			SDL_Quit()
                
elif BACKEND == 'pygame':
	class PygameTestCase(TextureTest):
		def setUp(self):
			# initialise opengl
			success, fail = pygame.init()
			if fail:
				print "Unable to init pygame: %s\n", pygame.get_error()
				sys.exit(1)
				
			pygame.display.init()
			pygame.display.set_mode( (320,200), pygame.OPENGL, 24 )
			pygame.mouse.set_visible( False )
			pygame.display.set_caption(str(self.__class__),str(self.__class__))

		def tearDown(self):
			pygame.quit()


if __name__ == '__main__':
    main()
