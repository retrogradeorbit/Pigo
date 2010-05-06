#!/usr/bin/env python
# -*- coding: utf-8 -*-

# base imports
import os

# requires pyopengl
from OpenGL.GL import *

import pigo.lib

from TextureEngine import *

# defaults
defaultIconPath=os.path.join(os.path.dirname(__file__),"pigo.png")

class GfxEngine:
    def __init__(self):
        # is our sdl initialised?
        self._init=False
        
        self.allowedmodes=[]
        self.screenmode=0
        
        #self.textureengine=pigo.texture
        self.textureengine = None
        
        self.displaylist=None
        self._cached_quads={}
        
    def __del__(self):
        if self._init:
            self.CloseDisplay()
        
    def ListModes(self):
        """sets an internal list of SDL_Rects"""
        assert(self._init)
        
        class box(object):
            w=0
            h=0
            
            def __repr__(self):
                return "<GfxEngine::box w=%d h=%d>"%(self.w,self.h)
        
        self.allowedmodes=[]
        for rect in reversed(pigo.lib.ListModes()):
            r=box()
            r.w=rect[0]
            r.h=rect[1]
            self.allowedmodes.append(r)
            
        #self.allowedmodes=SDL_ListModes(None, SDL_FULLSCREEN|SDL_HWSURFACE)[::-1]		# [::-1] = from lowest res mode to highest res mode
        return self.allowedmodes
    
    def depGetModes(self):
        return self.allowedmodes
    
    def Initialise(self):
        """Initialise the underlying libraries."""
        if self._init:
            return
            
        pigo.lib.Initialise()
        pigo.lib.ShowCursor(False)
        self._init = True
        
    def OpenDisplay(self, title="PiGo",fullscreen=False,icon=None,mode=0):
        """Open the screen or window.
        
        title 		the Window title
        fullscreen 	if True open fullscreen, if false open window
        icon 		the Application and windows icon graphic
        mode 		the index for the ListModes() of the starting resolution. 0 is maximum resolution
        """
        self.Initialise()
        self.ListModes()
        
        pigo.lib.SetWindowTitle(title)
        
        # use the default icon if need be
        icon=defaultIconPath if icon==None else icon
        pigo.lib.SetAppIcon(icon)
        
        self.screenmode=mode
        self.screen = pigo.lib.SetVideoMode(self.allowedmodes[self.screenmode].w, self.allowedmodes[self.screenmode].h, 24, fullscreen)
        assert(self.screen != None)
        
        self.fullscreen=fullscreen
        
    def CloseDisplay(self):
        """Close the window or screen and restore the Desktop"""
        assert(self.sdlinit)
        SDL_Quit()
        self.sdlinit=False
        
        TTF_Quit()
        self.sdlttf=False
        
        
    def ToggleFullScreen(self):
        assert(self.sdlinit)
        SDL_WM_ToggleFullScreen(self.screen)
        self.fullscreen=not self.fullscreen

    def ResolutionLower(self):
        assert(self.sdlinit)
        if self.screenmode==0:
            return
        self.ChangeMode(self.screenmode-1)
        
    def ResolutionHigher(self):
        assert(self.sdlinit)
        if self.screenmode==len(self.allowedmodes)-1:
            return
        self.ChangeMode(self.screenmode+1)
        
    def ChangeMode(self,modenum):
        print "ChangeMode: modenum=",modenum,"w=",self.allowedmodes[modenum].w,"h=",self.allowedmodes[modenum].h
        self.screenmode=modenum
        self.ChangeResolution(self.allowedmodes[modenum].w, self.allowedmodes[modenum].h)
        
    def ChangeResolution(self, width, height):
        assert(self.sdlinit)
        SDL_FreeSurface(self.screen)
        if self.fullscreen:
            self.screen = SDL_SetVideoMode(width,height, 24, SDL_OPENGL|SDL_FULLSCREEN)
        else:
            self.screen = SDL_SetVideoMode(width,height, 24, SDL_OPENGL)
            
        assert(self.screen != None)
        
    def SetClosestResolution(self, width, height):
        """Set the resolution to the closest allowed matching resolution"""
        
        # calculate a match score for the widths
        scores=[abs(width-mode.w) for mode in self.allowedmodes]
        
        # get a list of the modenumbers that have the lowest match score
        lowscore=min(scores)
        modenums=[index for index in range(len(scores)) if scores[index]==lowscore]
        
        # now for each of these modenums find the height scores
        hscores=[abs(height-self.allowedmodes[mode].h) for mode in modenums]
        
        self.screenmode=modenums[hscores.index(min(hscores))]
        self.ChangeResolution(self.allowedmodes[self.screenmode].w, self.allowedmodes[self.screenmode].h)
        

    def SetupGL(self):
        """At the moment we assume the pixels are always square, which is probably not true.
        TODO: somehow use the monitors aspect ratio
        """
        print "begin frame",self.allowedmodes
        width, height = self.allowedmodes[self.screenmode].w,self.allowedmodes[self.screenmode].h
        print "S",self.screenmode,"W",width,"H",height	
        glViewport(0,0,width-1,height-1)
        glMatrixMode(GL_PROJECTION)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glDepthFunc(GL_LEQUAL)
        glLoadIdentity()
        if width==height:
            # square
            self.SetupUniformCoordinateSystem(-1.0,1.0,-1.0,1.0)
        elif width>height:
            # landscape
            self.SetupUniformCoordinateSystem(-float(width)/height,float(width)/height,-1.0,1.0)
        else:
            # portrait
            self.SetupUniformCoordinateSystem(-1.,1.,-float(height)/width,float(height)/width)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def SetupUniformCoordinateSystem(self,x1,x2,y1,y2):
        print "SetupUniform(",x1,x2,y1,y2,")"
        glOrtho( x1, x2, y2, y1, -1., 1.)

    def EndFrameGL(self):
        print "endframe"
        #glBindTexture(GL_TEXTURE_2D,1)
        #glBindTexture(GL_TEXTURE_2D,2)
        #glBindTexture(GL_TEXTURE_2D,3)
        #glBindTexture(GL_TEXTURE_2D,2)
        #glBindTexture(GL_TEXTURE_2D,1)
        #glFinish()
            
    def DrawTextureQuad(self, corners,textureid, textureextents=(0,0,1,1),tint=(1.0,1.0,1.0),alpha=1):
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glEnable(GL_BLEND)
        glEnable(GL_TEXTURE_2D)
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)               #source factor is (Rs, Bs, Gs, As) dest is (1,1,1,1)-(Rs, Bs, Gs, As)
        glPolygonMode(GL_FRONT, GL_FILL)
        self.BindTexture(textureid)
        
        glColor4fv( [tint[0],tint[1],tint[2],alpha])                            #so we modulate with white.
        
        glBegin(GL_QUADS)
        
        glNormal3d( 0.0, 0.0, 1.0)
            
        glTexCoord2d(textureextents[0],textureextents[3])
        glVertex3dv( corners[3] )
        
        glTexCoord2d(textureextents[2],textureextents[3])
        glVertex3dv( corners[2] )
        
        glTexCoord2d(textureextents[2],textureextents[1])
        glVertex3dv( corners[1] )
        
        glTexCoord2d(textureextents[0],textureextents[1])
        glVertex3dv( corners[0] )
        glEnd()
        
    def DrawTextureQuadDeprecated(self, corners,texture, textureextents=(0,0,1,1),tint=(1.0,1.0,1.0),alpha=1):
        # setup the GL
        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        #glEnable(GL_BLEND)
        
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)               #source factor is (Rs, Bs, Gs, As) dest is (1,1,1,1)-(Rs, Bs, Gs, As)
        #glPolygonMode(GL_FRONT, GL_FILL)

        texture.Bind()
        
        glColor4fv( [tint[0],tint[1],tint[2],alpha])                            #so we modulate with white.
        
        # is this corner/texture extent combo cached
        if (texture,tuple(corners),tuple(textureextents)) in self._cached_quads.keys():
            glCallList(self._cached_quads[(texture,tuple(corners),tuple(textureextents))])
            #print "DL:",self._cached_quads[(texture,tuple(corners),tuple(textureextents))]
        else:
            displaylist=glGenLists(1)
            #print "DISPLAY LIST GEN",displaylist
            glNewList(displaylist, GL_COMPILE)
            glBegin(GL_QUADS)
            
            #print "EXTENTS:",textureextents
            
            
            glNormal3d( 0.0, 0.0, 1.0)
            
            glTexCoord2d(textureextents[0],textureextents[3])
            glVertex3dv( corners[3] )
            
            glTexCoord2d(textureextents[2],textureextents[3])
            glVertex3dv( corners[2] )
            
            glTexCoord2d(textureextents[2],textureextents[1])
            glVertex3dv( corners[1] )
            
            glTexCoord2d(textureextents[0],textureextents[1])
            glVertex3dv( corners[0] )
            glEnd()
            glEndList()


            print corners,textureextents
            self._cached_quads[(texture,tuple(corners),tuple(textureextents))]=displaylist

        return self
        
        #glDisable(GL_TEXTURE_2D)
        #glEnable(GL_LIGHTING)
        # glDisable(GL_BLEND)

    def DrawTextureQuad1(self, corners,texture, textureextents=(0,0,1,1),tint=(1.0,1.0,1.0),alpha=1):
        print "GFX::DrawTextureQuad(",corners,texture, textureextents,tint,alpha,")"
        # setup the GL
        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE) #GL_MODULATE
        #glEnable(GL_TEXTURE_2D)
        
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)               #source factor is (Rs, Bs, Gs, As) dest is (1,1,1,1)-(Rs, Bs, Gs, As)
        #glPolygonMode(GL_FRONT, GL_FILL)
        
        glColor4fv( [tint[0],tint[1],tint[2],alpha])                            #so we modulate with white.

        print "texture",texture,".Bind()",texture.glid
        texture.Bind()
        
        glBegin(GL_QUADS)
        glNormal3d( 0.0, 0.0, 1.0)

        #textureextents=list(textureextents)
        #textureextents.reverse()
        #corners=list(corners)
        #corners.reverse()
            
        glTexCoord2d(textureextents[0],textureextents[3])
        glVertex3dv( corners[3] )
            
        glTexCoord2d(textureextents[2],textureextents[3])
        glVertex3dv( corners[2] )
            
        glTexCoord2d(textureextents[2],textureextents[1])
        glVertex3dv( corners[1] )
            
        glTexCoord2d(textureextents[0],textureextents[1])
        glVertex3dv( corners[0] )
        glEnd()

        glFlush()
        
        #return self
        
        #glDisable(GL_TEXTURE_2D)
        #glEnable(GL_LIGHTING)
        #glDisable(GL_BLEND)
        
    def SwapBuffers(self):
        SDL_GL_SwapBuffers()
        #SDL_Flip()
    
    @property
    def screen_width(self):
        return self.allowedmodes[self.screenmode].w
        
    @property
    def screen_height(self):
        return self.allowedmodes[self.screenmode].h
        
    def GetScreenShot(self):
        """Return an image that is a screenshot of the present opengl screen.
        returns a PIL RGB image"""
        import numpy
        
        data = self._get_opengl_surface( self.screen_width, self.screen_height )

        from PIL import Image
        
        return Image.fromstring("RGB", (self.screen_width, self.screen_height), data )
        
    def _get_opengl_surface(self,w,h):
        import OpenGL.GL
        data = OpenGL.GL.glReadPixels(0, 0, w, h,
                        OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
        if SDL_BYTEORDER == SDL_LIL_ENDIAN:
            Rmask = 0x000000ff
            Gmask = 0x0000ff00
            Bmask = 0x00ff0000
        else:
            Rmask = 0x00ff0000
            Gmask = 0x0000ff00
            Bmask = 0x000000ff
        # Flip vertically
        pitch = w * 3
        data = ''.join([data[y*pitch:y*pitch+pitch] for y in range(h - 1, -1, -1)])
        return data
        
        #newsurf = SDL_CreateRGBSurfaceFrom(data, surf.w, surf.h, 24, pitch,
                        #Rmask, Gmask, Bmask, 0)
        #return newsurf

#void GfxEngine::SwapBuffers()
#{
    #Uint32 t1,t2,t3;

    #// our entry time
    #t1=GetTicks();

    #// swap gl buffers (software linux version slow)
    #SDL_GL_SwapBuffers();
    #t2=GetTicks();

    #// signal the system for a sleep now. we eventually have to render control to the
    #// system routines so it might as well be short as possible, and straight after
    #// a frame draw
    #//SDL_Delay(0);
    #t3=GetTicks();

    ##ifdef DEBUG
    #printf("SDL_GL_SwapBuffers():%d\t\tSDL_Delay(0):%d\n",t2-t1,t3-t2);
    ##endif
#}


    def DrawGrid(self, z=0.0):
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)
        glColor4f(0.4,0,0,1.0)
        for x in [float(y)/10. for y in range(-20,20)]:
            glBegin(GL_LINES)
            glVertex3f(x, -2., z)
            glVertex3f(x, 2., z)
            glEnd()
            
        for y in [float(y)/10. for y in range(-20,20)]:
            glBegin(GL_LINES)
            glVertex3f(-2., y, z)
            glVertex3f(2., y, z)
            glEnd()
            
        glColor4f(0.8,0.8,0.8,1.0)
        for x in range(-2,2,1):
            glBegin(GL_LINES)
            glVertex3f(x, -2., z+0.01)
            glVertex3f(x, 2., z+0.01)
            glEnd()
            
        for y in range(-2,2,1):
            glBegin(GL_LINES)
            glVertex3f(-2., y, z+0.01)
            glVertex3f(2., y, z+0.01)
            glEnd()
            
    def ClearWithColour(self,colour):
        glClearColor(colour[0], colour[1], colour[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        
    def GenerateTextureId(self):
        """allocate a texture id and bind to it. Returns the id"""
        # allocate the texture
        texture=glGenTextures(1)
        
        # bind and set the texture settings
        glBindTexture(GL_TEXTURE_2D, texture)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        
        # load the image into the texture.
        #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(),image.get_height(),0,GL_RGBA,GL_UNSIGNED_BYTE,tex)
        
        # repeat the texture (maybe this should be clamp?)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        
        return texture
    
    def UploadTexture(self, glid, image):
        self.BindTexture(glid)
        string=image.tostring("raw", "RGBA", 0, 1)
        self.texturesize=len(string)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size[0], image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, string)
        
    
    def BindTexture(self, num):
        glBindTexture(GL_TEXTURE_2D, num)
    
    def DeleteTexture(self, texture ):
        glDeleteTextures(texture)
        
    def DebugInfo(self):
        return
        """ Display OpenGL driver info. """
        print "OpenGL driver info"
        print "=================="
        print "GL_VENDOR =",glGetString(GL_VENDOR)
        print "GL_RENDERER =",glGetString(GL_RENDERER)
        print "GL_VERSION =",glGetString(GL_VERSION)
        print
        print "OpenGL driver limits"
        print "===================="
        print "GL_AUX_BUFFERS =",glGetIntegerv(GL_AUX_BUFFERS)
        print "GL_MAX_LIGHTS =",glGetIntegerv(GL_MAX_LIGHTS)
        print "GL_MAX_TEXTURE_SIZE =",glGetIntegerv(GL_MAX_TEXTURE_SIZE)
        print "GL_MAX_CLIENT_ATTRIB_STACK_DEPTH = ",glGetIntegerv(GL_MAX_CLIENT_ATTRIB_STACK_DEPTH)
        print "GL_MAX_ATTRIB_STACK_DEPTH = ",glGetIntegerv(GL_MAX_ATTRIB_STACK_DEPTH)
        print "GL_MAX_CLIP_PLANES = ",glGetIntegerv(GL_MAX_CLIP_PLANES)
        print "GL_MAX_EVAL_ORDER = ",glGetIntegerv(GL_MAX_EVAL_ORDER)
        print "GL_MAX_LIST_NESTING = ",glGetIntegerv(GL_MAX_LIST_NESTING)
        print "GL_MAX_MODELVIEW_STACK_DEPTH = ",glGetIntegerv(GL_MAX_MODELVIEW_STACK_DEPTH)
        print "GL_MAX_NAME_STACK_DEPTH = ",glGetIntegerv(GL_MAX_NAME_STACK_DEPTH)
        print "GL_MAX_PIXEL_MAP_TABLE = ",glGetIntegerv(GL_MAX_PIXEL_MAP_TABLE)
        print "GL_MAX_PROJECTION_STACK_DEPTH = ",glGetIntegerv(GL_MAX_PROJECTION_STACK_DEPTH)
        print "GL_MAX_TEXTURE_STACK_DEPTH = ",glGetIntegerv(GL_MAX_TEXTURE_STACK_DEPTH)
        print "GL_MAX_VIEWPORT_DIMS = ",glGetIntegerv(GL_MAX_VIEWPORT_DIMS)
        print "GL_DEPTH_BITS = ",glGetIntegerv(GL_DEPTH_BITS)
        print
        print "OpenGL driver extensions"
        print "========================"
        print glGetString(GL_EXTENSIONS)

        print
