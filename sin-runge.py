from vpython import *

def func1(x, v, t): # Velocity
    return v

def func2(x, v, t): # Force function
    return -sin(x)

def runge4(x, v, t, h): # 4th Order Runge–Kutta method
    k1 = h * func1(x,v,t)
    m1 = h * func2(x,v,t)
    k2 = h * func1(x + k1 / 2,v + m1 / 2,t + h / 2)
    m2 = h * func2(x + k1 / 2,v + m1 / 2,t + h / 2)
    k3 = h * func1(x + k2 / 2,v + m2 / 2,t + h / 2)
    m3 = h * func2(x + k2 / 2,v + m2 / 2,t + h / 2)
    k4 = h * func1(x + k3,v + m3,t + h)
    m4 = h * func2(x + k3,v + m3,t + h)
    delta_x = (k1 + k4 + 2 * (k2 + k3)) / 6.0
    delta_v = (m1 + m4 + 2 * (m2 + m3)) / 6.0
    return [delta_x,delta_v]

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
    delta = runge4(x0,v0,time,h)
    x0 += delta[0]
    v0 += delta[1]
    x = func2(x0,v0,time)
    y = 0.5 - cos(x0)
    ball.pos = vector(x,y,0)
    cyl.pos = ball.pos
    cyl.axis = -ball.pos
