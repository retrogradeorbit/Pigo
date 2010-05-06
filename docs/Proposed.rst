Proposed Features and Functionality
===================================

In this document we will layout how we propose bits of Pigo will (should) work.

Setting Up Graphics Layers
--------------------------

Setting Up A ColourLayer
^^^^^^^^^^^^^^^^^^^^^^^^

A ColourLayer is just a single 2D block of colour::
    
    import pigo
    
    class MyApp(pigo.App):
        def Init(self):
           self.AddLayer( pigo.gfx.ColourLayer( (0.5, 0.0, 0.5) ))
           
    MyApp.startup()

    
Setting Up An ObjectLayer
^^^^^^^^^^^^^^^^^^^^^^^^^

To put an ObjectLayer over the top that we can put sprite in::

	import pigo
	
	class MyApp(pigo.App):
		def Init(self):
			self.colour = self.AddLayer( pigo.gfx.ColourLayer( (0.5, 0.0, 0.5) ))
			self.objects = self.AddLayer( pigo.gfx.ObjectLayer() )
	
	MyApp.startup()

	
To put an object on that object layer::

	import pigo
	
	class MyApp(pigo.App):
		def Init(self):
			self.colour = self.AddLayer( pigo.gfx.ColourLayer( pigo.colours.RED ))
			self.objects = self.AddLayer( pigo.gfx.ObjectLayer() )

			self.myobj = self.objects.Add( pigo.gfx.Sprite( file="test.png", frame=(32,32) ) )
	
	MyApp.startup()

	
Moving an object in stateless way::

	import pigo
	
	class MyApp(pigo.App):
		def Init(self):
			self.colour = self.AddLayer( pigo.gfx.ColourLayer( pigo.colours.RED ))
			self.objects = self.AddLayer( pigo.gfx.ObjectLayer() )

			self.myobj = self.objects.Add( pigo.gfx.Sprite( file="test.png", frame=(32,32) ) )
	
		def Update(self):
			self.myobj.y -= 0.01		# move
			self.myobj.y = (2.0 + self.myobj.y) if self.myobj.y < -1.0 else self.myobj.y		# loop
			
	MyApp.startup()


Moving an object in a stateful way::

	import pigo
	from pigo.commands import sleep, run
	
	class MyApp(pigo.App):
		def Init(self):
			self.colour = self.AddLayer( pigo.gfx.ColourLayer( pigo.colours.RED ))
			self.objects = self.AddLayer( pigo.gfx.ObjectLayer() )

			self.myobj = self.objects.Add( pigo.gfx.Sprite( file="test.png", frame=(32,32) ) )
			
			def mover():
				while True:
					for y in pigo.math.frange(-1,1,0.01):
						self.myobj.y = y
						sleep()
			
			self.mover = run(mover)
						
	MyApp.startup()

	

