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
        
        
        
# base library functions
def Init():
    pygame.init()
    pygame.font.init()
	
def Quit():
	pygame.quit()
    
def Flip():
	pygame.display.flip()
	
def Poll():
	event = pygame.event.poll()
	return None if event.type == pygame.NOEVENT else event

def iskey(event,key):
	return event.key == key
		
def isquit(event):
	return event.type == pygame.QUIT

KEY_KP_PLUS = pygame.K_KP_PLUS
KEY_PLUS = pygame.K_KP_PLUS
KEY_KP_MINUS = pygame.K_KP_MINUS
KEY_MINUS = pygame.K_MINUS
KEY_ESCAPE = pygame.K_ESCAPE
KEY_EQUALS = pygame.K_EQUALS
KEY_F11 = pygame.K_F11

KEY_a = pygame.K_a
KEY_b = pygame.K_b
KEY_c = pygame.K_c
KEY_d = pygame.K_d
KEY_e = pygame.K_e
KEY_f = pygame.K_f
KEY_g = pygame.K_g
KEY_h = pygame.K_h
KEY_i = pygame.K_i
KEY_j = pygame.K_j
KEY_k = pygame.K_k
KEY_l = pygame.K_l
KEY_m = pygame.K_m
KEY_n = pygame.K_n
KEY_o = pygame.K_o
KEY_p = pygame.K_p
KEY_q = pygame.K_q
KEY_r = pygame.K_r
KEY_s = pygame.K_s
KEY_t = pygame.K_t
KEY_u = pygame.K_u
KEY_v = pygame.K_v
KEY_w = pygame.K_w
KEY_x = pygame.K_x
KEY_y = pygame.K_y
KEY_z = pygame.K_z


KEYTYPE = pygame.KEYDOWN

	
def ShowCursor(boolean=True):
    pygame.mouse.set_visible(boolean)
    
def SetAppIcon(filename):
    surf = pygame.image.load(filename)
    pygame.display.set_icon(surf)
    
def SetWindowTitle(title, short=None):
    pygame.display.set_caption(title, short or title)
	
def ListModes(depth=0):
    return pygame.display.list_modes(depth,pygame.FULLSCREEN|pygame.OPENGL|pygame.HWSURFACE|pygame.DOUBLEBUF)
    
def SetVideoMode(w,h,depth=24,fullscreen=False):
    return pygame.display.set_mode( (w,h), pygame.FULLSCREEN|pygame.OPENGL|pygame.HWSURFACE|pygame.DOUBLEBUF if fullscreen else pygame.OPENGL|pygame.HWSURFACE|pygame.DOUBLEBUF, depth)
    