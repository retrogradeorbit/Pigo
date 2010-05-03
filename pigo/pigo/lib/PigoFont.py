# -*- coding: utf-8 -*-
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