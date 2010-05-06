Proposed Features and Functionality
===================================

In this document we will layout how we propose Pigo will (should) work.

Creating an Application
-----------------------

Create an application by deriving your application class from pigo.App::
    
    from pigo import App, bootstrap
    
    class MyApp(App):
        pass
    
    bootstrap(MyApp)
    
Making an Application Run Fullscreen
------------------------------------

Setting the class variable Fullscreen to True makes the application start up in fullscreen::
    
    from pigo import App, bootstrap
    
    class MyApp(App):
        Fullscreen = True
        
    bootstrap(MyApp)
    
.. note::
    
    This does not prevent the user from *switching back* into window mode. That requires changing the default behavoir. It just makes the start up state fullscreen.
    
Setting Up Graphics Layers
--------------------------

Setting Up A ColourLayer
^^^^^^^^^^^^^^^^^^^^^^^^

A ColourLayer is just a single 2D block of colour::
    
    import pigo
    
    class MyApp(pigo.App):
        def Initialise(self):
           self.AddLayer( pigo.gfx.ColourLayer( (0.5, 0.0, 0.5) ))
           
    bootstrap(MyApp)
    
    