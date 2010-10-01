Creating an Application
-----------------------

Create an application by deriving your application class from pigo.App::
    
	from pigo import App

	class MyApp(App):
		pass

	MyApp.start()
	
Pressing the 'q' key or 'escape' will quit the programme. The plus and minus keys increase and decrease the window size
or screen resolution. The 'f' key or 'f11' toggles between fullscreen and windowed mode.
    
Making an Application Run Fullscreen
------------------------------------

Setting the class variable Fullscreen to True makes the application start up in fullscreen::
    
    from pigo import App
    
    class MyApp(App):
        fullscreen = True
        
    MyApp.start()
    
.. note::
    
    This does not prevent the user from *switching back* into window mode. That requires changing the default behavoir.
    It just makes the start up state fullscreen.
    
Loading a Basic Layer
---------------------

The graphics engine inside pigo has a layering subsytem. To display something on screen we create one of those layers.
We add this layer to the layer system ``pigo.gfx.layers``::

	import pigo

	class MyApp(pigo.App):
		fullscreen = False
		# keys_fullscreen = ( pigo.key.f, pigo.key.F12 )
	    # keys_exit = ( pigo.key.ESC, )

		def init(self):
			pigo.App.Init(self)
			self.background = self.AddLayer( pigo.gfx.ColourLayer(colour=(0.0,1.0,1.0)) )
		
	MyApp.start()

This gives you a blight blue screen. The screen persists going through resolutions and switching fullscreen and back.

.. warning:: Note that the method to override is init(), NOT __init__(). We don't want to execute this code on the
	construction of the object, we want to execute this code when the application is initialising itself on the host OS.

Adding an Object Layer
----------------------

On top of the colour layer we want to add a 2D object layer. To this we can add sprites and other objects for the game.
Let's begin by making a snowfall scene. We add snowflakes in the Initialisation::

	from pigo import App, gfx
	import random
	
	NUM_FLAKES = 30
	
	class MyApp(App):
	
		def init(self):
			self.background = gfx.layers.Add( pigo.gfx.ColourLayer( colour=(0.0,1.0,1.0) ) )
			self.objects = gfx.layers.Add( pigo.gfx.ObjectLayer() )
			
			self.snowflakes = [ self.objects.Add( 
							gfx.Sprite( file="snowflake.png", x=random.rand()*2.0-1.0, y=random.rand()*2.0-1.0  )
												)  for num in range(NUM_FLAKES) ]
			
			
	MyApp.start()

Making Things Move
------------------

A lot of people are familiar with updating all the objects in a scene in a game loop or a step function that gets called
each game tick. Lets try that method here::

    from pigo import App, gfx
    import random

	NUM_FLAKES = 30

	class MyApp(App):

		def init(self):
			self.background = gfx.layers.Add( pigo.gfx.ColourLayer( colour=(0.0,1.0,1.0) ) )
			self.objects = gfx.layers.Add( pigo.gfx.ObjectLayer() )

			# tuples of the objects and their velocities
			self.snowflakes = [ ( self.objects.Add(
							gfx.Sprite( file="snowflake.png", x=random.rand()*2.0-1.0, y=random.rand()*2.0-1.0  )
												), random.rand()*5.0 )  for num in range(NUM_FLAKES) ]


	    def step(self):
	        for obj, speed in self.snowflakes:                          # loop over objects
	            obj.y += speed                                          # update each object
	            while obj.y > 1.2:                                      # if it's off the bottom of the screen
	                obj.y -= 2.5                                        # move it up so its hidden off hte top

	MyApp.start()

Doing Things the Pigo Way
-------------------------

Pigo runs on stackless and can use tasklets to control in game behavior. This doesn't offer a lot in very simple cases
but in the more complex instances it dramatically reduces the complexity and therefor bugs of complex bahvoir code. Lets
redo our snowflake application using tasklets.

    from pigo import App, gfx, schedule
    import random

	NUM_FLAKES = 30

	class Snowflake(gfx.Sprite):
	    def run(self, speed=1.0):
	        while True:
	            self.y += speed
	            while self.y > 1.2:
	                self.y -= 2.5
	            schedule()

	class MyApp(App):

		def init(self):
			self.background = gfx.layers.Add( pigo.gfx.ColourLayer( colour=(0.0,1.0,1.0) ) )
			self.objects = gfx.layers.Add( pigo.gfx.ObjectLayer() )

			self.snowflakes = [ self.objects.Add(
							gfx.Sprite( file="snowflake.png", x=random.rand()*2.0-1.0, y=random.rand()*2.0-1.0  )
												) for num in range(NUM_FLAKES) ]
		    for flake in self.snowflakes():
		        pigo.run(flake.run)( random.rand()*5.0 )

	MyApp.start()

	
.. warning::
	Unimplemented.
	
	