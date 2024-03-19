# PlanetaryMotion.py
#
# A script to simulate planetary motion - generalised

import numpy as np
import matplotlib.pyplot as plt

G = 6.6743e-11
M = 100000000000
m = 200000000
A = -G*M*m
pos_0 = np.array([0.0, -2000.0])
vel_0 = np.array([0.05, 0.0])

# defining vector force
def Force(pos):
    f = (A/(np.linalg.norm(pos))**3)*pos
    return f

pos_track = []
time_track = []
pos = pos_0
vel = vel_0
T = 0
N = 100000

# Euler iterative method
for i in range(N):
    pos_track.append(pos)
    time_track.append(T)
    dt = 10
    f = Force(pos)
    # print(vel,dt*vel,f,dt/m*f)
    pos = pos + dt*vel
    vel += (dt/m)*f
    T += dt

x, y = zip(*pos_track)
fig = plt.figure()
# print(x,y)
plt.scatter(x, y, s=0.1)
plt.grid()
plt.show()



    


