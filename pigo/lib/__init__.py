# -*- coding: utf-8 -*-
"""
This is a library that attempts to autoload and somewhat abstract away a window/platform api. Idea is to support SDL(ctypes), pygame and pyglet in beginning.

Module autodetects as much as it can as it goes along

"""

module = None

try:
    import SDL
    import SDL_ttf

    module_name = 'sdl'
    module = SDL
except ImportError, ie:
    # no sdl ctypes. Try pygame
    try:
        import pygame
        pygame.init()
        
        module_name = 'pygame'
        module = pygame
        
        import pygame.font
        pygame.font.init()
                    
    except ImportError, ie:
        # no pygame, try pyglet
        try:
            import pyglet
            
            module_name = 'pyglet'
            module = pyglet
            
        except ImportError, ie:
            raise Exception("No viable backend. Tried sdl, pygame, pyglet.")
        
if module_name == 'sdl':
    from ModuleSDL import *
            
elif module_name == 'pygame':
    from ModulePygame import *