

##
## Function to SDL rendered text into alpha 32 bit RGBA text
##
## The problem:
## When SDL renders a font into an RGBA surface, the alpha blending is blended opaquely.
## The r,g,b value is antialiased, but the alpha is not. The alpha is "applied" in 24 bit land
## and rendered at full opacity in 32 bit land.
##
## The solution:
## This cython function takes a rendered font image of the incorrect format and 
## recalculates a new image with only two colour values (255,255,255) and (0,0,0)
## but with varying levels of alpha, corresponding with the antialiasing for that font
## at that bit point. This is done in cython to achieve some speed.
##

import numpy as npcimport numpy as np

def create_font_image_alpha( np.ndarray[np.uint8_t,ndim=3] buff, np.ndarray[np.uint8_t,ndim=1] colour ):
    cdef:
        Py_ssize_t x,y
    
    assert buff.shape[2] == 4
    
    for y in range(buff.shape[1]):
        for x in range(buff.shape[0]):
            if buff[x,y,0] > 0:
                buff[x,y,3] = buff[x,y,0]
                buff[x,y,0] = colour[0]  
                buff[x,y,1] = colour[1]
                buff[x,y,2] = colour[2]
            else:
                buff[x,y,0] = 0
                buff[x,y,1] = 0
                buff[x,y,2] = 0
                buff[x,y,3] = 0
        

    
