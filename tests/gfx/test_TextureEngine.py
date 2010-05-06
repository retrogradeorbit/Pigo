from unittest import TestCase, main

from OpenGL.GL import *
from SDL import *
from SDL.ttf import TTF_Init
import PIL

import os
from PIL import Image
from random import randint

from TextureEngine import TextureEngine, HORIZONTAL, VERTICAL

class TextureEngineTest(TestCase):
    def setUp(self):
        self.texeng = TextureEngine()
        
    def tearDown(self):
        self.texeng = None
        
    def testInstantiation(self):
        self.assert_(self.texeng)
        
    def testLoadRGBAImageHorizontal(self):
        for w,h in [ (512,512), (256,1024), (1024,512) ]:
            for xs,ys in [ (24,32), (48,12), (8,128), (50,50) ]:
                # make an image file
                pic = Image.new( "RGBA", (w, h) )
                for x in range(w):
                    for y in range(h):
                        pic.putpixel( (x,y), (randint(0,255), randint(0,255), randint(0,255), randint(0,255)) )
                name = ".test.load.rgba.%d.%d.%d.%d.png"%(w,h,xs,ys)
                pic.save(name)
                
                texture = self.texeng.LoadImage(name,(xs,ys),label="testlabel",cache=False,sequence=HORIZONTAL)
                
                #self.assert_( self.texeng.IsCached("testlabel") )
                
                self.assert_(texture.GetNumTexFrames())
                print w,h,xs,ys,w/xs,h/ys
                for i in range(texture.GetNumTexFrames()):
                    print texture.GetTexFrame(i)
                self.assert_(texture.GetNumTexFrames() == (w/xs)*(h/ys) )
                
                # assert we are actually laid our horizontally
                self.assert_( False not in [ texture.GetTexFrame(i).x < texture.GetTexFrame(i+1).x for i in range( w/xs - 1 ) ] )
                for xoffset in range( w/xs -1 ):
                    self.assert_( False not in [ texture.GetTexFrame(i*w/xs).y < texture.GetTexFrame(i*w/xs + w/xs).y for i in range( h/ys - 1 ) ] )
        
    def testLoadRGBAImageVertical(self):
        w,h = 512,512
        xs,ys = 64,64
        
        # make an image file
        pic = Image.new( "RGBA", (w, h) )
        for x in range(w):
            for y in range(h):
                pic.putpixel( (x,y), (randint(0,255), randint(0,255), randint(0,255), randint(0,255)) )
        pic.save(".test.load.rgba.png")
        
        texture = self.texeng.LoadImage(".test.load.rgba.png",(xs,ys),label="testlabel",cache=True,sequence=VERTICAL)
        
        self.assert_( self.texeng.IsCached("testlabel") )
        
        self.assert_(texture.GetNumTexFrames())
        self.assert_(texture.GetNumTexFrames() == (w/xs)*(h/ys) )
        
        # assert we are actually laid our horizontally
        self.assert_( False not in [ texture.GetTexFrame(i).y < texture.GetTexFrame(i+1).y for i in range( h/ys - 1 ) ] )
        for xoffset in range( h/ys -1 ):
            self.assert_( False not in [ texture.GetTexFrame(i*h/ys).x < texture.GetTexFrame(i*h/ys + h/ys).x for i in range( w/xs - 1 ) ] )
        

    
if __name__ == '__main__':
    main()
