#
# Just a class to wrap the functions to do with SDL and fint management.
# This is NOT a pigo font, but is used by that kind of font in generation
#

from SDL import SDL_Color, SDL_CreateRGBSurface, SDL_SWSURFACE, SDL_Rect, SDL_SetAlpha, SDL_SRCALPHA, SDL_FillRect, SDL_MapRGBA, SDL_BlitSurface
from SDL.ttf import TTF_OpenFont,TTF_CloseFont,TTF_RenderText_Solid, TTF_RenderText_Blended,TTF_RenderText_Shaded, TTF_SetFontStyle, TTF_FontHeight, TTF_FontAscent, TTF_FontDescent, TTF_GlyphMetrics, TTF_SizeText, TTF_FontFaceIsFixedWidth, TTF_RenderGlyph_Solid, TTF_RenderGlyph_Blended, TTF_RenderGlyph_Shaded

class Metric(object):
    """A font metric structure. Canbe accessed as a list, just like SDL,
    or via named attributes"""
    KEY_LIST = ['minx','maxx','miny','maxy','advance']
    
    def __init__(self, *args, **kwargs):
        if len(args)==5:
            self.metric = args[:]
        elif len(args)==0:
            self.metric = [0,0,0,0,0]
            for num,key in enumerate( self.KEY_LIST ):
                if key in kwargs:
                    self.metric[num]=kwargs[key]
            
            # nicely report errors in keys
            err_keys = [ key for key in kwargs if key not in self.KEY_LIST ]
            if err_keys:
                raise KeyError, "Constructor passed unknown keys: %s"%(','.join(err_keys))
        else:
            # cannot construct object
            raise Exception, "Cannot parse constructor arguments"
            
    @property
    def minx(self):
        return self.metric[self.KEY_LIST.index('minx')]
    
    @property
    def maxx(self):
        return self.metric[self.KEY_LIST.index('maxx')]
    
    @property
    def miny(self):
        return self.metric[self.KEY_LIST.index('miny')]
    
    @property
    def maxy(self):
        return self.metric[self.KEY_LIST.index('maxy')]
    
    @property
    def advance(self):
        return self.metric[self.KEY_LIST.index('advance')]
        
    def __getitem__(self, item):
        #pass the list through
        return self.metric.__getitem__(item)
        
    def __unicode__(self):
        return "Metric("+(",".join(["%s=%d"%(s,d) for (s,d) in zip(self.KEY_LIST,self.metric)]))+")"
    
    def __str__(self):
        return "Metric("+(",".join(["%s=%d"%(s,d) for (s,d) in zip(self.KEY_LIST,self.metric)]))+")"
    
    def __len__(self):
        return len(self.metric)
    

class SDLFont(object):
    
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
                
if __name__=="__main__":
    from SDL import ttf
    ttf.TTF_Init()
    fontfile="/home/crispin/working/gamejam/src/pigo/MONOFONT.TTF"
    font=SDLFont(fontfile,32)
    font.RenderSet()
    print font.CalculateOptimalSize()
    image=font.Render()
    
    #image to_string
    
    
    # use PIL to save RGBA as PNG
    from PIL import Image
    from ctypes import *
    
    ctype=c_ubyte
    scount=image.w*image.h*4
    
    count=sizeof(ctype)*scount
    s=create_string_buffer(count)
    memmove(s,image._pixels,count)
    
    st=str(s.raw)
    
    #for ch in st:
        #print ord(ch),' ',
    
    newim=Image.fromstring("RGBA", (image.w,image.h), st)
    if True:
        for x in range(image.w):
            for y in range(image.h):
                #print "(%d,%d)="%(x,y),newim.getpixel((x,y))
                r,g,b,a=newim.getpixel((x,y))
                c=255 if r else 0
                newim.putpixel((x,y),(c,c,c,r))

                #newim.putpixel( (x,y), (r,g,b,255 if r else 0) )
                
                #print "(%d,%d)="%(x,y),newim.getpixel((x,y))
                
    newim.save("testfont.png")
    
    #SDL_SaveBMP(image, "testfont.bmp")
