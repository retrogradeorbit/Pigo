
from Texture import Texture
from Tex import Tex
#from weakref import *

from PIL import Image

##
## @brief stores and keeps track of on card textures
##
## stores and keeps track of on card textures. 
## TODO: resizes and caches to disk texture shrinking

HORIZONTAL=0
VERTICAL=1

import weakref

class TextureEngine:
    
    def __init__(self):
        # cache is a simple dictionary, with label as the keys and textures as the values
        self.cache={}
        
        self.textures=[]
    
    def LoadImage(self, file, framesize=None, label=None, cache=True, sequence=HORIZONTAL):
        # we call this and it loads the relevant image of disk. We can choose to cache it or not. 
        # it sets up for us a texture that is not resident, and a series of Tex's that are the frames
        # of the animation, if such a value is passed in
        print "LoadImage(",file,")"
        if cache:
            if not label:
                label=file
            if self.IsCached(label):
                return self.GetCached(label)
        
        im=Image.open(file)
        texture=Texture(im,filename=file)
        size=im.size
        if framesize==None:
            framesize=size
            
        # generate tex frames
        if sequence==HORIZONTAL:
            for outer in range(size[1]/framesize[1]):
                for inner in range(size[0]/framesize[0]):
                    #print inner,outer
                    #print ( texture, inner*framesize[0],outer*framesize[1],framesize[0],framesize[1])
                    texture.AddTexFrame(Tex( texture, inner*framesize[0],outer*framesize[1],framesize[0],framesize[1]))
                    
        elif sequence==VERTICAL:
            for outer in range(size[0]/framesize[0]):
                for inner in range(size[1]/framesize[1]):
                    texture.AddTexFrame(Tex( texture, outer*framesize[0],inner*framesize[1],framesize[0],framesize[1]))
            
        # cache it if we are asked to
        if cache:
            self.Cache(texture, label)
            
        return texture
        
    def Cache(self, texture, label):
        assert(label not in self.cache.keys())		# should not already have this label
        self.cache[label]=texture			            # TODO: should this be a weak reference instead of a hard reference?
        
    def Uncache(self, label):
        del self.cache[label]
        
    def IsCached(self,label):
        return label in self.cache.keys()
    
    def GetCached(self,label):
        return self.cache[label]
    
    def AddTexture(self,texture):
        # weakref list
        self.textures.append(weakref.ref(texture,lambda ref: self.textures.remove(ref)))
        
    def GetTextureSizes(self):
        # return a lits of texture sizes
        return [text().texturesize for text in self.textures]
     
    def GetSize(self):
        return sum(self.GetTextureSizes)
    
