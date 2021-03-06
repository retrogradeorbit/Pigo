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

Pigo is designed for rapid prototyping and gamejam situations and intended to be a solid platform for building 
apon that over time. Writing games with pigo involves overriding the methods of pigo objects and triggering
and managing the execution of tasklets. Tasklets can drive the entire game forward in a very graceful and implicitly
stateful way.

Pigo is the game framework I would have loved to have had as a kid. I remember BASIC's on various 8-bit platforms and owned Blitz Basic
and AMOS for the Amiga. What I want Pigo to be is the ultimate version of that for home game development. A modern interpretation.
Fully utilising the hardware, but in an oldschool way. Use a modern language like stackless python to bring tools like closures, coroutines
and microthreads.

Contents:

.. toctree::
   :maxdepth: 2

	Proposed

Installation
============

Install from source.

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
            

However, unlike before we don't really want a single tasklet controlling this object's movement. If you look at the original Space Invaders
you will notice only one alien moves at any one time. Each game step the microprocessor only had the power to update a single ship at a time.
It would loop over the ships, on consequtive steps, moving from the top left alien to the bottom right alien in horizontal stripes.
This algorithm naturally gives us the classic Space Invaders speed up as the alien horde gets smaller. And each time the entire wave is
updated (be it one or fifty ships) we emit a alien advance noise, creating the Space Invaders soundscape. We implement this by having a
class that controls the alien horde that has a stackless tasklet that processes the space invaders like the old microprocessor would have done.

    class AlienController():
        def __init__(self, aliens=[]):
            self.aliens = aliens[:]             # this is all the aliens. We set entries to None when they are destroyed

        def run(self):
            # a generator to return ships forever. When this stops returning ships, the player destroyed them all
            def generate():
                while False in [X is None for X in self.aliens]:            # while some are still alive
                    for alien in self.aliens:
                        if alien is not None:
                            yield alien
                    self.sfx.play()

            for alien in generate():
                alien.move()
                stackless.schedule()

            # TODO: aliens are dead, lets advance levels


    
                

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


