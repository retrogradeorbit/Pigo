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
		
		def Init(self):
			self.background = pigo.gfx.layers.Add( pigo.gfx.ColourLayer( colour=(1.0,1.0,1.0) ) )
			
	MyApp.startup()
	
.. warning::

	Unimplemented.
	
Adding an Object Layer
----------------------

On top of the colour layer we want to add a 2D object layer. To this we can add sprites and other objects for the game::

	import pigo
	
	class MyApp(pigo.App):
	
		def Init(self):
			self.background = pigo.gfx.layers.Add( pigo.gfx.ColourLayer( colour=(1.0,1.0,1.0) ) )
			self.objects = pigo.gfx.layers.Add( pigo.gfx.ObjectLayer() )
			
	MyApp.startup()
	
.. warning::
	Unimplemented.
	
	