#!/usr/bin/env

"""Font
==========
A Pigo font is composed of some texture storage, where all the characters of the font are stored permanently
on the graphics card RAM. These textures are RGBA and the text is usually (unless a colour font is used) white... with alpha.
In future there may be more than one texture, say in the case of a large font on a GFX card with only small texture sizes,
but at this stage its is only one texture per font.
"""
import lib
from Texture import Texture
from Tex import Tex

#import tools

import os
DEFAULT_FONT = (os.path.join(os.path.dirname(__file__),"monofont.ttf"),24)
DEFAULT_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789-=_+[]{};':\",.<>/?\|`~!@#$%^&*()"

class Font(Texture):
    def __init__(self, filename=None, fontsize=None, charset=DEFAULT_CHARSET):
        assert type(fontsize)==int
        
        if filename==None:
            filename=DEFAULT_FONT[0]
        if fontsize==None:
            fontsize=DEFAULT_FONT[1]

        # lets create the image for the texture from the font
        self._font=lib.Font(filename, fontsize)
        self._font.RenderSet(charset=charset)		# make the glyph size details for each character
        image,extents=self._font.Render()

        #image=tools.fromSDLImageToPILImage(image)
        #print "IMAGE",image
        image.save("temp.png")

        self.extents=extents

        # call constructor
        Texture.__init__(self,image=image,filename=filename)

        # create the alpha numeric tex list
        self.charset=charset
        self._metrics=self._font.metrics

        # in a font, the tex's store is a hash rather than a list (not frames)
        self.texchars=dict([ (ch,Tex(self,*extents[ch])) for ch in charset])
        self.texframes=[Tex(self,0.0,0.0,1.0,1.0)]

    def _get_metrics(self):
        """save the meta info (extents, baseline) for each character"""
        self._metrics = {}
        for char in self.charset:
            metric = self._font.GlyphMetrics(char)
            self._metrics[char] = metric
            
    def GetMetric(self, char):
        return self._metrics[char]

    def GetTex(self,key):
        return self.texchars[key]
        
