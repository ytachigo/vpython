from vpython import *

def func1(x, v, t): # Velocity
    return v

def func2(x, v, t): # Force function
    return -sin(x)

def lfrog(x, v, t, h): # Leap frog method
    next_x = x + func1(x,v,t) * h
    next_v = v + func2(x,v,t) * h
    return [next_x,next_v]

i = 0 # Set up initial values
h = 0.01
phi = 30
x0 = phi / 180.0 * pi
v0 = 0.0

x = func2(x0,v0,0) # Set objects
y = 0.5 - cos(x0)
ball = sphere(pos=vector(x,y,0),color=color.red, radius=0.15)
cyl = cylinder(pos=ball.pos, axis=-ball.pos,
               color=color.white, radius=0.01)

while 1: # Iteration
    rate(400)
    i += 1
    time = i * h
    next = lfrog(x0,v0,time,h)
    x0 = next[0]
    v0 = next[1]
    x = func2(x0,v0,time)
    y = 0.5 - cos(x0)
    ball.pos = vector(x,y,0)
    cyl.pos = ball.pos
    cyl.axis = -ball.pos
