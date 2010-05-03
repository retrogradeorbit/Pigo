# -*- coding: utf-8 -*-
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