# -*- coding: utf-8 -*-
import pygame

from PigoFont import PigoFont

class Font(pygame.font.Font, PigoFont):
    def __init__(self, filename, size):
        pygame.font.Font.__init__(self,filename,size)
        
    def GetHeight(self):
        return pygame.font.Font.get_height(self)
        
    def GetAscent(self):
        return pygame.font.Font.get_ascent(self)
        
    def GetDescent(self):
        return pygame.font.Font.get_descent(self)
        
    def GlyphMetrics(self, st):
        return pygame.font.Font.metrics(self, st)
        
    def Render(self, colour=(255,255,255)):
        image,extents=self.render(SDL_Color(255,255,255))
        
        from PIL import Image
        import cFont
        import numpy
        
        buff=numpy.frombuffer(image.pixels.as_ctypes(), numpy.uint8)
        copy = buff.reshape((image.w,image.h,4))
        colour = numpy.array(colour,dtype=numpy.ubyte)
        cFont.create_font_image_alpha(copy,colour)
        dupe = Image.fromarray(copy,"RGBA")
        
        return dupe, extents
        


class TestCase(object):
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
        
        
