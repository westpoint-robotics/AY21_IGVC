import math

def triangulate(pxl=100, pyl=100, pxr=150, pyr=150):
    image_width = 1920
    #fov is in degrees
    camera_fov = 120
    fov = math.radians(camera_fov)

    #Delta x and y
    dpx = pxr - pxl
    dpy = pyr - pyl

    #Center of stopsign
    centerx = dpx/2
    centery = dpy/2

    #ppr
    ppr = image_width/fov

    #radian conversions
    rad_x = centerx/ppr
    rad_y = centery/ppr
    drad_x = dpx/ppr
    drad_y = dpy/ppr

    #Distance to stop sign
    r = 0.75/drad_x

    #delta x and delta y the 
    delta_x = r*math.cos(rad_x)
    delta_y = r*math.sin(rad_x)
    return (delta_x,delta_y)

def test():
    delta_x,delta_y = triangulate()
    print("Here is the distance of the stop sign from the car.")
    print(delta_x)
    print(delta_y)