
from Texture import Texture
import weakref

class Tex:
    """A Tex is a window into a small part of a Texture. Successive Tex's can spell out an animation for a sprite to follow. Or a tex could have its offsets moved slowly over time to create special scaling and scrolling effects.
    """
    
    def __init__(self, texture, x=0, y=0, width=None, height=None):
        #this is a weak ref so when our parent texture dies, we signal it here by setting to None
        #in this way each Tex is tied to a texture. Different textures shareing the same Tex behavoir?
        #make them different Tex()s
        self.texture=weakref.ref(texture, lambda x: self.ClearTexture())
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        if width==None:
            self.width=self.texture().originalwidth
        if height==None:
            self.height=self.texture().originalheight

    def __str__(self):
        return "%s, %s, %s, %s, %s"%(str(self.texture()),str(self.x),str(self.y),str(self.width),str(self.height))
        
    def ClearTexture(self):
        self.texture=None
        
    # texture co-ordinates
    def GetU0(self):
        return float(self.x) / self.texture().width
    
    def GetU1(self):
        return float(self.x + self.width) / self.texture().width
    
    def GetV0(self):
        return float(self.y) / self.texture().height
    
    def GetV1(self):
        return float(self.y + self.height) / self.texture().height
    
    def GetExtents(self):
        return ( self.GetU0(), self.GetV0(), self.GetU1(), self.GetV1() )
    
