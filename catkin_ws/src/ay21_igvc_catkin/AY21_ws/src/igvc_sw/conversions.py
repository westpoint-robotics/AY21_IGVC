import math

image_width = 1920
#fov is in degrees
camera_fov = 120
fov = math.radians(camera_fov)

#Left-side location
pxl = 100
pyl = 100

#right-side location
pxr = 800
pyr = 800

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

#delta x and delta y
delta_x = r*math.cos(rad_x)
delta_y = r*math.sin(rad_x)

print("Here is the distance of the stop sign from the car.")
print(delta_x)
print(delta_y)