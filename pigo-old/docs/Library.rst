Abstraction Library
===================

Pigo contains an inbuilt lower level library to abstract away the functionality necessary to run on different platforms. This is for functionality like opening a window, 
opening a full screen instance or accessing the audio, mouse and joystick facilities of the underlying operating system. The library autodetects the best backend to use
and automatically uses that. To find out which backend your system uses, just import the lib module and haver a look like this::
    
    >>> from pigo import lib
    >>> lib.module_name
    'pygame'

So here we can see the pygame backend will be used for operating system functionality.

Inside the lib namespace you will find some general abstraction of underlying operating system functionality.

.. note::
    This library is intended mostly for internal use inside Pigo. You will not usually need to call this directly if you programme your game using the higher level pigo functionality. It is included here for completeness, and just in case
    for some reason you do need to gain access to some of the operating systems underlying functionality.

Font
----

This is a generalised abstraction of TrueType® font technology.

TestCase
--------

This is a TestCase to derive from to test functionality requiring the OS system services. During setup it initialises a window context and necessary subsystems.






