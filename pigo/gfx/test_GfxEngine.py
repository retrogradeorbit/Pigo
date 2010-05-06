from unittest import TestCase, main
import Font
import sys
import time

from OpenGL.GL import *
from SDL import *
from SDL.ttf import TTF_Init
import PIL

import os
from PIL import Image
        

from GfxEngine import GfxEngine

class GfxEngineTest(TestCase):
    def setUp(self):
        self.gfx = GfxEngine()
        
    def tearDown(self):
        self.gfx = None
        
    def ntestInstantiation(self):
        self.assert_(self.gfx)
       
    def ntestListModes(self):
        self.gfx.InitVideo()
        modes = self.gfx.ListModes()
        self.assert_(len(modes))            # make sure we get some modes
        
        # make sure mode is unique list
        already=[]
        for mode in modes:
            self.assert_( (mode.w,mode.h) not in already )
            already.append( (mode.w, mode.h) )
            
    def ntestOpenCloseDisplay(self):
        self.gfx.InitVideo()
        self.gfx.OpenDisplay()
        time.sleep(1)
        self.gfx.CloseDisplay()
        time.sleep(1)
        
    def ntestZZHalfOpenDisplay(self):
        self.gfx.OpenDisplay()
        time.sleep(1)
        
    def compare(self, image, filename, threshold=0):
        fname = ".%s.png"%filename
        
        if os.path.exists(fname):
            # file exists, lets compare
            saved = Image.open(fname)
            
            if saved.size != image.size:
                return False, "Screen does not match size of stored image %s"%fname
            
            s = 0
            for x in range(saved.size[0]):
                for y in range(saved.size[1]):
                    s+=sum(abs(A-B) for (A,B) in zip( saved.getpixel((x,y)),image.getpixel((x,y)) ))
                    
            return s<=threshold, "Screen does not match stored image %s to threshold value %d"%(fname,threshold)
            
        else:
            # assume this is the correct image and save it
            print "Saving image %s"%fname
            image.save(fname)
            
            return False, "Please look at image %s and verify this is how this code should render"%fname
        
    def ntestGetOpenGLBuffer(self):
        self.gfx.OpenDisplay()
        image = self.gfx.GetScreenShot()
        self.assert_(*self.compare(image,"blank_screen", threshold=0) )
        self.gfx.CloseDisplay()
        
    def ntestDrawGrid(self):
        self.gfx.OpenDisplay()
        self.gfx.DrawGrid()
        self.assert_(*self.compare(self.gfx.GetScreenShot(),"grid",0))
        self.gfx.CloseDisplay()
        
    def ntestClearWithColour(self):
        self.gfx.OpenDisplay()
        self.gfx.ClearWithColour( (0,0,0) )
        self.assert_(*self.compare(self.gfx.GetScreenShot(), "black_clear", 0))
        self.gfx.ClearWithColour( (1.0,1.0,1.0) )
        self.assert_(*self.compare(self.gfx.GetScreenShot(), "white_clear", 0))
        self.gfx.ClearWithColour( (0.30,.15,0.5) )
        self.assert_(*self.compare(self.gfx.GetScreenShot(), "purple_clear", 0))
        self.gfx.ClearWithColour( (1.0,0.0,0.0) )
        self.assert_(*self.compare(self.gfx.GetScreenShot(), "red_clear", 0))
        self.gfx.ClearWithColour( (0.0,0.0,1.0) )
        self.assert_(*self.compare(self.gfx.GetScreenShot(), "blue_clear" ,0))
        self.gfx.CloseDisplay()
        
    def ntestTextureUpload(self):
        self.gfx.OpenDisplay()
        self.gfx.SetupGL()
        self.gfx.ClearWithColour( (0,0,0) )
        self.gfx.DrawGrid()
        
        # make a texture
        teximage = Image.new("RGBA",(32,32))
        for y in range(32):
            for x in range(32):
                if (x+y)%2==0:
                    teximage.putpixel((x,y),(255,255,0,128))
                else:
                    teximage.putpixel((x,y),(0,0,0,0))
                    
        for x in range(8,32-8):
            for y in range(8,32-8):
                teximage.putpixel( (x,y) , (0,0,0,0) )
        
        # upload texture
        id = self.gfx.GenerateTextureId()
        self.gfx.UploadTexture(id,teximage)
        
        # next texture should be a new id
        self.assert_(self.gfx.GenerateTextureId() != id)
                    
        corners = [
            ( -0.5, 0.5, 0 ),
            ( 0.5, 0.5, 0 ),
            ( 0.5, -0.5, 0 ),
            ( -0.5, -0.5, 0 )
                    ]
                    
        self.gfx.DrawTextureQuad(corners, id, textureextents=(0,0,1,1), tint=(1.0,1.0,1.0), alpha=1.0)
        
        self.assert_(*self.compare(self.gfx.GetScreenShot(), "texture" ,0))
        
    def testDrawTextureQuad(self):
        self.gfx.OpenDisplay()
        self.gfx.SetupGL()
        self.gfx.ClearWithColour( (0,0,0) )
        self.gfx.DrawGrid()
        
        # make a texture
        teximage = Image.new("RGBA",(32,32))
        for y in range(32):
            for x in range(32):
                if (x+y)%2==0:
                    teximage.putpixel((x,y),(255,255,0,128))
                else:
                    teximage.putpixel((x,y),(0,0,0,255))
                    
        for x in range(8,32-8):
            for y in range(8,32-8):
                teximage.putpixel( (x,y) , (0,0,0,0) )
        
        # upload texture
        id = self.gfx.GenerateTextureId()
        self.gfx.UploadTexture(id,teximage)
        
        # next texture should be a new id
        self.assert_(self.gfx.GenerateTextureId() != id)
                    
        corners = [
            ( -0.5, 0.5, 0 ),
            ( 0.5, 0.5, 0 ),
            ( 0.5, -0.5, 0 ),
            ( -0.5, -0.5, 0 )
                    ]
                    
        self.gfx.DrawTextureQuad(corners, id, textureextents=(0,0,1,1), tint=(1.0,1.0,1.0), alpha=1.0)
        self.assert_(*self.compare(self.gfx.GetScreenShot(), "texture_quad" ,0))
        
        #self.gfx.CloseDisplay()
        #self.gfx.OpenDisplay()
        #self.gfx.SetupGL()
        
        self.gfx.ClearWithColour( (0,0,0) )
        self.gfx.DrawGrid()
        self.gfx.DrawTextureQuad(corners, id, textureextents=(0,0,1,1), tint=(1.0,1.0,1.0), alpha=0.5)
        self.assert_(*self.compare(self.gfx.GetScreenShot(), "texture_quad_alpha_0.5" ,0))
        
        self.gfx.ClearWithColour( (0,0,0) )
        self.gfx.DrawGrid()
        self.gfx.DrawTextureQuad(corners, id, textureextents=(0,0,1,1), tint=(0,1.0,0), alpha=1.0)
        self.assert_(*self.compare(self.gfx.GetScreenShot(), "texture_quad_tint_green" ,0))
        
        
        
        
        
      
if __name__ == '__main__':
    main()
