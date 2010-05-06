"""
This is a library that attempts to autoload and somewhat abstract away a window/platform api. Idea is to support SDL(ctypes), pygame and pyglet in beginning.

Module autodetects as much as it can as it goes along

"""

module = None

try:
	import SDL
	import SDL_ttf

	module_name = 'sdl'
	module = SDL
except ImportError, ie:
	# no sdl ctypes. Try pygame
	try:
		import pygame
		pygame.init()
		
		module_name = 'pygame'
		module = pygame
		
		import pygame.font
		pygame.font.init()
			
		
	except ImportError, ie:
		# no pygame, try pyglet
		try:
			import pyglet
			
			module_name = 'pyglet'
			module = pyglet
			
		except ImportError, ie:
			raise Exception("No viable backend. Tried sdl, pygame, pyglet.")
			
class PigoFont(object):
    #
    # pigo convenience methods
    #
    def RenderSet(self, charset=u"abcdefghijklmonpqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=`~[]{};':\",.<>/?\|"):
    #def RenderSet(self, charset=u"abcdefghijklmonpqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=`"):
        #just read in charsets characteristics
        self.metrics={}
        for ch in charset:
            self.metrics[ch]=self.GlyphMetrics(ch)
        self.charset=charset
        
    def CalculateRenderHeight(self, width):
        # just scan as a calculation and work out the height
        metrics=self.metrics
        fontheight=self.GetHeight()
        x,y=0.,0.
        for ch in self.charset:
            w=metrics[ch][1]-metrics[ch][0]
            nx=x+w
            if nx>width:
                #new line
                y+=fontheight
                x=0
            x+=w
            
        y+=fontheight
        return y
            
    def CalculateOptimalSize(self, allowedwidths=[32,64,128,256,512,1024,2048,4096]):
        """Work out the font rendering in width and height gfx, that takes up the minimal space"""
        upscale = lambda y: 1 if y<1 else 2 if y <2 else 4 if y<4 else 8 if y<8 else 16 if y<16 else 32 if y < 32 else 64 if y < 64 else 128 if y < 128 else 256 if y < 256 else 512 if y < 512 else 1024 if y<1024 else 2048 if y<2048 else 4096
        
        minsize=9999999999999
        mindimensions=(None,None)
        for maxwidth in allowedwidths:
            height=self.CalculateRenderHeight(maxwidth)
            if height<=maxwidth:
                #upscale 'height' to even 2 power texture size
                height=upscale(height)
                size=height*maxwidth
                if size<minsize:
                    minsize=size
                    mindimensions=(maxwidth,height)
                    
        return mindimensions,minsize
			
if module_name == 'sdl':
	class Font(PigoFont):
		def __init__(self, filename, size):
			self.font=TTF_OpenFont( filename, size )
			print "FONT",self.font
        
		def __del__(self):
			TTF_CloseFont( self.font )
			
		def RenderSolid(self, text, colour):
			return TTF_RenderText_Solid(self.font, text, colour)
			
		def RenderBlended(self, text, colour):
			return TTF_RenderText_Blended(self.font, text, colour)
		
		def RenderShaded(self, text, fg, bg):
			return TTF_RenderText_Shaded(self.font, text, fg, bg)
		
		def SetStyle(self, style):
			#TTF_STYLE_BOLD
			#TTF_STYLE_ITALIC
			#TTF_STYLE_UNDERLINE
			TTF_SetFontStyle(font, style)
			
		def GetHeight(self):
			return TTF_FontHeight(self.font)
		
		def GetAscent(self):
			return TTF_FontAscent(self.font)
		
		def GetDescent(self):
			return TTF_FontDescent(self.font)
		
		def GlyphMetrics(self, ch):
			"""returns minx, maxx, miny, maxy, advance"""
			return Metric(*TTF_GlyphMetrics(self.font, ch))
			
		def SizeText(self, text):
			return TTF_SizeText(self.font, text)
		
		def FaceIsFixedWidth(self):
			return TTF_FontFaceIsFixedWidth(self.font)
		
		def RenderGlyphSolid(self, ch, colour):
			return TTF_RenderGlyph_Solid(self.font, ch, colour)
			
		def RenderGlyphBlended(self, ch, colour):
			return TTF_RenderGlyph_Blended(self.font, ch, colour)
		
		def RenderGlyphShaded(self, ch, fg, bg):
			return TTF_RenderGlyph_Shaded(self.font, ch, fg, bg)
			
		def SDLRender(self, colour=SDL_Color(255,255,255)):
			dimensions, size=self.CalculateOptimalSize()
			
			width,height=dimensions
			depth=32
			flags=0
			masks=(0xff << 16, 0xff << 8, 0xff, 0)
			#print "create"
			image = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, depth, masks[0], masks[1], masks[2], masks[3])
			#print "created",image
			
			metrics=self.metrics
			fontheight=self.GetHeight()
			x,y=0,0
			extents={}
			for ch in self.charset:
				w=metrics[ch][1]-metrics[ch][0]
				nx=x+w
				if nx>width:
					#new line
					y+=fontheight
					x=0
					
				#draw glyph
				#print "glyph",ch,x,y,metrics[ch],fontheight,self.GetAscent(),self.GetDescent()
				surface=self.RenderGlyphBlended(ch,colour)
				#print "glyphed",surface
				
				# source and dest for blit
				sourcerect = SDL_Rect(0, 0, w, fontheight)
				destrect = SDL_Rect(0, 0, w, fontheight)
				destrect.x = x
				destrect.y = y + self.GetAscent()-metrics[ch][3]

				# save the rectangle for later lookup
				extents[ch]=(x,y,w,fontheight)
				
				#SDL_SetAlpha(surface, 0, SDL_ALPHA_OPAQUE);
				SDL_SetAlpha(surface, SDL_SRCALPHA, 0);
				SDL_FillRect(image, destrect, SDL_MapRGBA(image.format, 0, 0, 0, 0));
	#SDL_FreeSurface(source);
	#SDL_FreeSurface(destination);

				#print "blit"
				result = SDL_BlitSurface(surface, sourcerect, image, destrect)
				#print "blitted",result
				
				#step
				x+=w
			
			return image, extents

		def Render(self, colour=(255,255,255)):
			image,extents=self.SDLRender(SDL_Color(255,255,255))
			
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
			
			TTF_Init()
			
		def tearDown(self):
			SDL_Quit()
			
elif module_name == 'pygame':
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
			
			
