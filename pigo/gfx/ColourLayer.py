import pigo

#
# This layer erases everything and draws a constant colour that is set
#

class ColourLayer():
	def __init__(self, colour=(0.0,0.0,0.0)):
		self.SetColour( colour )
	
	def SetColour(self, colour=(0.0,0.0,0.0)):
		# should be RGB
		assert(len(colour)==3)
		
		# all values should be floats
		assert([type(a)==float for a in list(colour)]==[True, True, True])
		
		# all values should be between 0.0 and 1.0
		assert([a>=0.0 and a<=1.0 for a in list(colour)]==[True, True, True])
		
		self._colour=colour
		
	def GetColour(self):
		return self._colour
		
	colour = property(SetColour,GetColour)
	color = property(SetColour,GetColour)
	
	def Draw(self, gfx):
		pigo.lib.ClearWithColour(self.colour)
		