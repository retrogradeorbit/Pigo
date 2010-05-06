from unittest import TestCase, main
import Font
import sys

from OpenGL.GL import *
import PIL
import lib

class FontTest(lib.TestCase,TestCase):
	def testMonoFont(self):
		fnt = Font.Font( filename="test_monofont.ttf", fontsize=32 )
		
		self.assert_( fnt.filename )
		
		for glyph in Font.DEFAULT_CHARSET:
			metric = fnt.GetMetric(glyph)
			# make sure each glyphs metrics are correct
			self.assert_(list(metric) == list(fnt._font.GlyphMetrics(glyph)))
			
		#get the fixed dvance this onofont is using
		fixed_width = metric.advance
		
		# make sure entire font is fixed width
		for glyph in Font.DEFAULT_CHARSET:
			self.assert_(fnt.GetMetric(glyph).advance == fixed_width)
	
	def testProportionalFont(self):
		fnt = Font.Font( filename="test_propfont.ttf", fontsize=32 )
		self.assert_(fnt.filename)
        
       
        
if __name__ == '__main__':
    main()
