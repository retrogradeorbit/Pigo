.. Pigo documentation master file, created by
   sphinx-quickstart on Mon May  3 16:56:09 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================
Python Interactive Game Objects
================================

Pigo is a high level game creation framework written in stackless python tailored for 2D game creation. 
It is not a low level library like pygame or pyglet, although those types of operation can be done with pigo.
Instead think of it as a high level object oriented description where you say what you want, not how to do it.

Contents:

.. toctree::
   :maxdepth: 2


Installation
============

Install from source.

Introduction
============

There are many game development frameworks, and many just for Python, and in the opinion of this author, they *all* stink. They are all going about it wrong.
Why after all these years, all this modernisation of code design are we still building complex state machines by hand and calling update() on every object for
every frame. Why after all these years is making a simple clone of pacman or space invaders so ridiculously complex?

Pigo is a high level framework that attempts to fix this horrid state of affairs. The approach is that you subclass built in modules and override certain methods to get where you want to go.
Nothing is stopping you going low level, but the aim is to code your game at a more commanding level, and leave all the micro management and game algorithms to
library.

Examples
========

Space Invaders
--------------

First, lets define a Player object::

    class Player(Sprite):
    
        speed = 0.01
    
        def __init__(self):
            Sprite.__init__(self, file="player.png", frame=(16,16), pos=(0.0, 0.9) )    # middle bottom of the screen
            self.alive = True
            
        def run_control(self):
            while self.alive:
                if pigo.keypress('z'):
                    self.x = self.x - self.speed
                elif pigo.keypress('x'):
                    self.x = self.x + self.speed
                self.x = max(-0.9, min(0.9, self.x) )    # limit where we can move
                
                if pigo.keypress(' '):
                    self.Fire()
                
                pigo.schedule()
        
            # we must be dead now
            self.LoadAnim( pigo.gfx.anim( "explosion.png", (16,16) ) )
            pigo.wait_for_animation()
            
            
The speed class variable is an amount we add or subtract from the players xposition at each game tick. The initialiser calls the
parent initialiser and sets its position on the screen. An internal variable 'alive' will be used to tell if the player is still alive.
The initial graphics for the players ship is loaded.

The run_control function specifies a stackless tasklet that will be run to handle the processing of the players keyboard input and
move the ship. While the player is still alive, it moves the player, constrains their position, and then schedules for the frame update.

When this alive loop exits, the player must be dead. So we load the explosion animation, and play that. During this phase we dont check
keypresses or move the player.

Next, we define an alien::

    class Alien(Sprite):
    
        def __init__(self,row,column):
            Sprite.__init__(self)
            
            self.LoadAnim( "alien-%s.png"%(row), (32,32) )
            self.SetFrame(0)
            
        def walk(self):
            pass
    
                

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


