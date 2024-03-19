import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

G = 6.67e-11

dt = 10000

class Planet():
    """A type of solar system body"""
    def __init__(self, solar_system, colour, mass, position=(0, 0, 0), velocity=(0, 0, 0)):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.solar_system = solar_system
        self.c = colour
        self.solar_system.add_body(self)
        self.display_size = 10

    def draw(self):
        """Plotting & colouring method"""
        self.solar_system.ax.scatter(*self.position, marker="o", s=self.display_size, c=self.c)

    def move(self):
        """Position updating method"""
        self.position += dt * self.velocity

    def gravity(self, other):
        direction = other.position - self.position
        distance = np.linalg.norm(direction)
        unit_direc = direction / distance
        force_mag = G * self.mass * other.mass / (distance ** 2)
        force = force_mag * unit_direc

        accel_self = force / self.mass
        accel_other = -force / other.mass

        self.velocity += dt * accel_self
        other.velocity += dt * accel_other


class Sun(Planet):
    """A type of solar system body"""
    def __init__(self, solar_system, colour, mass, position=(0, 0, 0), velocity=(0, 0, 0)):
        super().__init__(solar_system, colour, mass, position, velocity)


class SolarSystem():
    """Visual representation of the solar system"""

    def __init__(self):
        self.bodies = []
        self.size = 1e12
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def fix_axes(self):
        """Axes are fixed irrespective of iteration"""
        self.ax.set_xlim(-self.size, self.size)
        self.ax.set_ylim(-self.size, self.size)
        self.ax.set_zlim(-self.size, self.size)

    def add_body(self, body):
        self.bodies.append(body)

    def update_bodies(self):
        self.ax.clear()
        for body in self.bodies:
            body.move()
            body.draw()

    def gravity_bodies(self):
        """This method calculates gravity interaction for every planet"""
        for i, first in enumerate(self.bodies):
            for second in self.bodies[i + 1:]:
                first.gravity(second)

solar_system = SolarSystem()

sun = Sun(solar_system, "yellow", mass=2e30)
earth = Planet(solar_system, "green", mass=6e24,
               position=(-1.5e11, 0, 0), velocity=(0, 29000, 0))

def animate(i):
    print("The frame is:", i)
    solar_system.gravity_bodies()
    solar_system.update_bodies()
    solar_system.fix_axes()

anim = animation.FuncAnimation(solar_system.fig, animate, frames=100, interval=100)

writervideo = animation.FFMpegWriter(fps=60)

anim.save("planets_animation.mp4", writer=writervideo, dpi=200)

# turn on interactive mode to view iterations as script runs
plt.ion()
plt.show()
