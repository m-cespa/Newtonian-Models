# SolarSystemTurtle.py

import turtle
import numpy as np

G = 1

class SolarSystemBody(turtle.Turtle):
    """Defines any body within the solar system"""
# define limits of body size
    min_display_size = 20

    def __init__(self, name, solar_system, mass, position = (0,0), velocity = (0,0)):
# super enables inheritance of all attributes of parent turtle class 
        super().__init__()
        self.name = name
        self.mass = mass
        self.setposition(position)
        self.velocity = velocity
# size of bodies scales with mass but ensuring all bodies visible
        self.display_size = max(self.mass / 200, self.min_display_size)
        self.shape("circle")

# ensures body does not trace a line under self.setposition to reach initial position
        self.pu()
        self.hideturtle()
 
 # super() used later to ensure all subclasses of SolarSystemBody are added to solar_system
        solar_system.add_body(self)

    def draw(self):
# clears the body before drawing new instance of body
        self.clear()
        self.dot(self.display_size)

# move function using turtle method
    def move(self):
# set will place body at coordinate based on current (cor) coordinate
        self.setx(self.xcor() + self.velocity[0])
        self.sety(self.ycor() + self.velocity[1])


class Planet(SolarSystemBody):
    """A type of solar system body"""
    def __init__(self, name, solar_system, color, mass, position = (0,0), velocity = (0,0)):
        super().__init__(name, solar_system, mass, position, velocity)
        self.c = color
        self.color(self.c)
        

class Sun(SolarSystemBody):
    """A type of solar system body"""
    def __init__(self, name, solar_system, mass, position = (0,0), velocity = (0,0)):
        super().__init__(name, solar_system, mass, position, velocity)
        self.color("yellow")


class SolarSystem(turtle.Turtle):
    """Visual representation of the solar system"""

# defining parameters for window to display system on
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.solar_system = turtle.Screen()
        self.solar_system.title("Planetary Orbit Simulation")
        self.solar_system.setup(width, height)
        self.solar_system.tracer(0)
        self.solar_system.bgcolor("black")

# stores all bodies associated with the solar system
        self.bodies = []
    
    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        body.clear()
        self.bodies.remove(body)

# updates position of all bodies
    def update_bodies(self):
        for body in self.bodies:
            body.move()
            body.draw()
        self.solar_system.update()
        
# defining position determining function
    @staticmethod
    def gravity(self: SolarSystemBody, other: SolarSystemBody):
        direction = np.subtract(other.pos(), self.pos())
        distance = np.linalg.norm(direction)
        unit_direc = direction / distance
        force_mag = G*self.mass*other.mass / (distance**2)
        force = force_mag * unit_direc

# reverse set to 1: direction defined from "self" to "other" (eg: from sun to earth)
# for "self", direction +ve, needs to be -ve for "other"
        reverse = 1
        for body in self, other:
            accel = force / body.mass
            body.velocity += reverse*accel
            reverse = -1
            
    def collision(self, first: SolarSystemBody, second: SolarSystemBody):
        distance = np.linalg.norm(np.subtract(second.pos(), first.pos()))
        if distance < 0.5 * (first.display_size + second.display_size):
            for body in first, second:
                if isinstance(body, Planet):
                    self.remove_body(body)
                    
    def all_bodies_gravity(self):
        for i, first in enumerate(self.bodies):
            for second in self.bodies[i+1:]:
                self.gravity(first, second)
                self.collision(first, second)

solar_system = SolarSystem(1400, 900)

sun = Sun("Sun", solar_system, mass = 20000)
Planets = (
    Planet("Mercury", solar_system, "white", mass = 50,
           position = (150, 0), velocity = (0, 12)),
    Planet("Venus", solar_system, "orange", mass = 100, 
           position = (-250, 0), velocity = (0, -9)),
    Planet("Earth", solar_system, "green", mass = 100,
           position = (400, 0), velocity = (0, 7)),
    Planet("Mars", solar_system, "red", mass = 80,
           position = (-600, 0), velocity = (0, -5)),
    Planet("Comet", solar_system, "blue", mass = 10,
           position = (-900, 0), velocity = (0, 2))
)

while True:
    solar_system.update_bodies()
    solar_system.all_bodies_gravity()
        
