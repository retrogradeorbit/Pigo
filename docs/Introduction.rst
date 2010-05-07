Creating an Application
-----------------------

Create an application by deriving your application class from pigo.App::
    
	from pigo import App

	class MyApp(App):
		pass

	MyApp.startup()
	
Pressing the 'q' key or 'escape' will quit the programme. The plus and minus keys increase and decrease the window size or screen
resolution. The 'f' key or 'f11' toggles between fullscreen and windowed mode.
    
Making an Application Run Fullscreen
------------------------------------

Setting the class variable Fullscreen to True makes the application start up in fullscreen::
    
    from pigo import App
    
    class MyApp(App):
        fullscreen = True
        
    MyApp.startup()
    
.. note::
    
    This does not prevent the user from *switching back* into window mode. That requires changing the default behavoir. It just makes the start up state fullscreen.
    
Loading a Basic Layer
---------------------

The graphics engine inside pigo has a layering subsytem. To display something on screen we create one of those layers. We add
this layer to the layer system ``pigo.gfx.layers``::

	import pigo

	class MyApp(pigo.App):
		fullscreen = False
	
		def Init(self):
			pigo.App.Init(self)
			self.background = self.AddLayer( pigo.gfx.ColourLayer(colour=(0.0,1.0,1.0)) )
		
	MyApp.startup()

This gives you a blight blue screen. The screen persists going through resolutions and switching fullscreen and back.
	
Adding an Object Layer
----------------------

On top of the colour layer we want to add a 2D object layer. To this we can add sprites and other objects for the game. Let's
begin by making a snowfall scene. We add snowflakes in the Initialisation::

	import pigo
	
	NUM_FLAKES = 30
	
	class MyApp(pigo.App):
	
		def Init(self):
			self.background = pigo.gfx.layers.Add( pigo.gfx.ColourLayer( colour=(0.0,1.0,1.0) ) )
			self.objects = pigo.gfx.layers.Add( pigo.gfx.ObjectLayer() )
			
			self.snowflakes = [ self.objects.Add( 
							pigo.gfx.Sprite( file="snowflake.png", x=random.rand()*2.0-1.0, y=random.rand()*2.0-1.0  )
												)  for num in range(NUM_FLAKES) ]
			
			
	MyApp.startup()
	
.. warning::
	Unimplemented.
	
	