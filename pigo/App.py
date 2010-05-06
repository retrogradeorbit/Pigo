# -*- coding: utf-8 -*-
import os,time

# requires pyopengl
from OpenGL.GL import *

import pigo.lib
import pigo.gfx

# shortcut to the engine
gfx = pigo.gfx.engine

#import GfxEngine
#import LayerEngine
#import TextureEngine
import stackless

import time, sys

#
# constants
#
FULLSCREEN = 1
WINDOWED = 2

class App:
	fullscreen = False                      # by default app opens windowed

	@classmethod
	def startup(cls):
		print "pigo startup..."
		instance = cls()
		instance.Start()
	
	def __init__(self, title="Pigo Application", options=None):
		self.title=title
		#self.options=options
		
		# setup our layer engine
		#self.layerengine=pigo.SetLayerEngine(LayerEngine.LayerEngine())
		#self.textureengine=pigo.SetTextureEngine(TextureEngine.TextureEngine())

		self.lastframetime=0.001
		
	def Start(self):
		"""run the app loop until exit"""
		self.Init()
		self.Setup()
		
		self.running=True
		self.MainLoop()
		
	def Init(self):
		"""Initialise the application"""
		#gfx=pigo.SetGfxEngine(GfxEngine.GfxEngine())
		
		gfx.OpenDisplay(self.title,self.fullscreen)
		
		modes=gfx.ListModes()
		assert(len(modes))
		gfx.ChangeMode(len(modes)-1)
		gfx.SetupGL()
		glClear(GL_DEPTH_BUFFER_BIT|GL_COLOR_BUFFER_BIT)
		glLoadIdentity()
		
	def Cleanup(self):
		gfx.CloseDisplay()
		
	def MainLoop(self):
		t=time.time()
		while self.running:
			self.Tick()
			self.DrawFrame()
			T=t
			self.lastframetime=time.time()-t
			t=time.time()
			
			#FIXED FRAME RATE
			#block until the difference is made up
			#while time.time()-t < (1.0/30)-self.lastframetime-(10.0/6000):
			#   pass
			
			#import agl
			#vsync=1
			#swap = c_long(int(vsync))
			#_agl_context=agl.aglGetCurrentContext()
			#agl.aglSetInteger(_agl_context, agl.AGL_SWAP_INTERVAL, byref(swap))
						
			self.lastframetime=time.time()-T
			t=time.time()
			
			gfx.SwapBuffers()
			self.ProcessEvents()
			#print "mainloop schedule"
			stackless.schedule()
			
	def Setup(self):
		"""Overide this to setup the system. This is called after display and audio is initialised"""
		pass
	
	def Tick(self):
		"""Override this to perform frame by frame stateless updates"""
		pass
	
	def DrawFrame(self):
		"""Draw the present frame"""

		#print "DrawFrame"
		
		# get the graphics engine to draw the frame
		#pigo.layer.Draw(pigo.gfx)

		#print "Drawn"
	
	def ProcessEvents(self):
		"""Perform default event processing for escape key and resolution keys"""
		while self.HandleEvent(pigo.lib.Poll()):
			pass
			
	
	def Close(self):
		"""Override with stuff to do on window close"""
		pass
	
	def HandleEvent(self, event):
		#print event
		if not event:
			return event
		
		if event.type == pigo.lib.KEYTYPE:
			if pigo.lib.iskey(event, pigo.lib.KEY_q) or pigo.lib.iskey(event, pigo.lib.KEY_ESCAPE):
				gfx.CloseDisplay()
				self.Close()
				sys.exit(0)
				
			elif pigo.lib.iskey(event,pigo. lib.KEY_KP_MINUS) or pigo.lib.iskey(event,pigo. lib.KEY_MINUS):
				gfx.ResolutionLower()
				
			elif pigo.lib.iskey(event,pigo. lib.KEY_KP_PLUS) or pigo.lib.iskey(event,pigo. lib.KEY_EQUALS):
				gfx.ResolutionHigher()
				
			elif pigo.lib.iskey(event,pigo. lib.KEY_f):
				gfx.ToggleFullScreen()
				
				
		elif pigo.lib.isquit(event):
			gfx.CloseDisplay()
			sys.exit(0)
		else:
			#pigo.log.Log("%s\n"%str(event))
			pass

	
	
	
