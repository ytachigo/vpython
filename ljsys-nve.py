from vpython import *
import numpy as np
import copy as cp
import os

def lj_force(r_list): # Function for LJ potential
    lj_force = 0
    for i in range(0, na - 1):
        lj_force += epsilon * (2 * ((sigma / r_list[i]) ** 13) -
        ((sigma / r_list[i]) ** 7)) / sigma
    return lj_force

def lfrog(x, y, z, vx, vy, vz, h): # Leap frog method
    coll = False
    r_list = []

    for i in range(0, na):
        dx = np.abs(x - x0_list[i])
        dy = np.abs(y - y0_list[i])
        dz = np.abs(z - z0_list[i])

        if dx > (blength / 2):
            dx = dx - blength
        if dy > (blength / 2):
            dy = dy - blength
        if dz > (blength / 2):
            dz = dz - blength

        r = np.sqrt(dx * dx + dy * dy + dz * dz)
        if r != 0:
            if r < sigma * 0.9: coll = False
            r_list.append(r)

    if coll == True: # In the case of collision
        next_x = x - vx * h
        next_y = y - vy * h
        next_z = z - vz * h
        next_vx = -vx
        next_vy = -vy
        next_vz = -vz
    else:
        next_x = x + vx * h
        next_y = y + vy * h
        next_z = z + vz * h
        next_vx = vx + lj_force(r_list) * h / m
        next_vy = vy + lj_force(r_list) * h / m
        next_vz = vz + lj_force(r_list) * h / m
    return [next_x,next_y,next_z], [next_vx,next_vy,next_vz]

i = 0 # Set up initial values
h = 0.5
m = 1
na = 1000
sigma = 1
epsilon = 1
blength = 20
x0_list = []
y0_list = []
z0_list = []
vx0_list = []
vy0_list = []
vz0_list = []
ljsp_list = []

for i in range(0, na): # Generate initial positions and velocities
    x0_list.append(blength * random() - blength / 2)
    y0_list.append(blength * random() - blength / 2)
    z0_list.append(blength * random() - blength / 2)
    vx0_list.append(random() - 0.5)
    vy0_list.append(random() - 0.5)
    vz0_list.append(random() - 0.5)

for i in range(0, na): # Set objects
    ljsp = sphere(pos=vector(x0_list[i],y0_list[i],z0_list[i]),
                  color=color.green,
                  radius=sigma * 0.9 / 2)
    ljsp_list.append(ljsp)

box0 = box(pos=vector(0,-blength / 2,0),
           axis=vector(blength,0,0),
           size=vector(blength,0.2,blength))
box1 = box(pos=vector(0,blength / 2,0),
           axis=vector(blength,0,0),
           size=vector(blength,0.2,blength))
box2 = box(pos=vector(-blength / 2,0,0),
           axis=vector(0,blength,0),
           size=vector(blength,0.2,blength))
box3 = box(pos=vector(blength / 2,0,0),
           axis=vector(0,blength,0),
           size=vector(blength,0.2,blength))
box4 = box(pos=vector(0,0,-blength / 2),
           axis=vector(0,blength,0),
           size=vector(blength,blength,0.2))

while 1: # Iteration
    rate(1000)
    i += 1
    time = i * h
    x0_copy = cp.copy(x0_list)
    y0_copy = cp.copy(y0_list)
    z0_copy = cp.copy(z0_list)
    vx0_copy = cp.copy(vx0_list)
    vy0_copy = cp.copy(vy0_list)
    vz0_copy = cp.copy(vz0_list)

    for i in range(0, na):
        next_p, next_v = lfrog(x0_copy[i],y0_copy[i],z0_copy[i],
                               vx0_copy[i],vy0_copy[i],vz0_copy[i],h)
        x0_list[i] = next_p[0]
        y0_list[i] = next_p[1]
        z0_list[i] = next_p[2]
        vx0_list[i] = next_v[0]
        vy0_list[i] = next_v[1]
        vz0_list[i] = next_v[2]
        x = x0_list[i]
        y = y0_list[i]
        z = z0_list[i]

        if (blength / 2) < x: # Periodic boundary condition
            x = x - blength
        if -(blength / 2) > x:
            x = x + blength
        if (blength / 2) < y:
            y = y - blength
        if -(blength / 2) > y:
            y = y + blength
        if (blength / 2) < z:
            z = z - blength
        if -(blength / 2) > z:
            z = z + blength

        ljsp_list[i].pos = vector(x,y,z)
