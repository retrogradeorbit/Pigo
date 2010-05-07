import pigo

class ColourApp(pigo.App):
	fullscreen = False
		
	def __init__(self):
		pigo.App.__init__(self,title="Colour Window App")
		
	def Init(self):
		pigo.App.Init(self)
		pigo.gfx.engine.SetClosestResolution(640,480)
		self.background = self.AddLayer( pigo.gfx.ColourLayer(colour=(0.0,1.0,1.0)) )

ColourApp.startup()
