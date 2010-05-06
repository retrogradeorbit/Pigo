from math import ceil, log
from PIL import Image
import numpy

# requires pyopengl
from OpenGL.GL import *

from ctypes import c_ubyte, POINTER

DEBUG = False

class Texture(object):
    """an OpenGL texture loaded on the card. An image off of disk. A drawn image. A captured image."""
    
    def __init__(self, image=None, filename=None):
        self.filename=filename
        self.glid=None
        self.width=0
        self.height=0
        
        # how many bytes we take up on the gfx card
        self.texturesize=0
        
        # for handling of resident textures, this is our opengl priority.
        # between zero and one. 1 is highst piority. Most likely to stay resident
        self.SetPriority(1.0)
        
        # our Tex frames if we have any
        self.texframes=[]
        
        # set the image	
        self.SetImage(image)
        
        #if image:
        #    self.GenerateID()
        #    self.MakeResident()

            #pigo.AddTexture(self)
        
    def __del__(self):
        self.DelID()
            
    def DelID(self):
        if self.glid!=None:
            if DEBUG:
                print "glDelTexture"
            glDeleteTextures(self.glid)
            self.glid=None
        
    def SetTexFrames(self, frames=[]):
        self.texframes=frames

    def AddTexFrame(self, frame):
        # TODO: assertions
        self.texframes.append(frame)
        
    def GetTexFrame(self, index):
        return self.texframes[index]
        
    def GetNumTexFrames(self):
        """return the number of texframes stored here"""
        return len(self.texframes)

    def GenerateID(self):
        id=glGenTextures(1)
        if DEBUG:
            print self,"GenerateID()=",id
        self.SetID(id)
        
    def GetID(self):
        """the GL id number.
        \returns The id number of the texture"""
        return self.glid
    
    def SetID(self, i):
        """Set the objects id number to that specified
        \param i The new ID number"""
        self.glid=i
        
    def SetPriority(self, prio=1.0):
        """Sets the priority of a texture between 0 and 1. O hardly resident. 1 as much as possible resident"""
        self.priority=prio

    def GetPriority(self):
        return self.priority

    def Bind(self):
        assert(self.glid != None)		# has to of already been assigned
        #print "Bind()",self,"glid=",self.glid
        glBindTexture(GL_TEXTURE_2D, self.glid)
        #gfx.BindTexture(self.glid)
        
    def Upload(self):
        """DEPRECATED"""
        print "WARNING: Texture::Upload() is deprecated. Use Texure::MakeResident() instead"
        return self.MakeResident()
        
    def MakeResident(self):
        if DEBUG:
            print "MakeResident()",self,"GLIDstore=",self.glid
        self.Bind()
        #glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        # copy the texture into the current texture ID
        string=self.image.tostring("raw", "RGBA", 0, 1)
        self.texturesize=len(string)
        
        if DEBUG:
            print "glTextImage2D"
            print "glTexImage2D()=",len(string)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, string)
        
    def EnsureResident(self):
        if not self.IsResident():
            if self.glid==None:
                self.GenerateID()
            self.MakeResident()
        
    def MakeNonResident(self):
        """If the texture is resident make it non resident"""
        assert(self.texturesize)
        assert(self.glid)
        assert(self.IsResident())
        
        # unload the texture from the gfx card
        glDeleteTextures([self.glid])
        self.glid=None
        
    def IsResident(self):
        """Warning: texture may not be resident until it is drawn with, even if it is generated"""
        if self.glid==None:
            return False
        return True
        return glAreTexturesResident( [self.glid] )[0]
        
    def GetWidth(self):
        return self.width
    
    def GetHeight(self):
        return self.height
    
    def SetWidth(self, width):
        self.width=width
        
    def SetHeight(self, height):
        self.height=height
            
    def GetImage(self):
        return self.image
            
    def SetImage(self, im=None):
        """Set the image for this texture to the one specified.
        \param image The PIL image object."""
        if im==None:
            self.image=None
            self.SetWidth(0)
            self.SetHeight(0)
            return

        assert hasattr(im,'size'), "Not an image"
    
        #we have to upscale width and height to a power of 2 for texture mapping
        iwidth,iheight=im.size
        texwidth=int(pow(2,ceil(log(iwidth,2))))
        texheight=int(pow(2,ceil(log(iheight,2))))
    
        #blit into the top left
        im2=Image.new("RGBA",(texwidth,texheight))
        im2.paste(im,(0,0))

        #imsum=0
        #for y in xrange(im2.size[1]):
        #    for x in xrange(im2.size[0]):
        #        pix=im2.getpixel((x,y))
        #        imsum+=(pix[0]+pix[1]+pix[2])

        #if self.glid!=None:
            #agi.renderer.ReloadTextureImage(self.glid,im2,texwidth,texheight)
    
        self.image=im2
        self.width=texwidth
        self.height=texheight
        self.originalwidth=iwidth
        self.originalheight=iheight
        self.originalimage=im
        

