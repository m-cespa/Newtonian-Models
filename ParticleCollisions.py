# ParticleCollisions.py

import turtle
import numpy as np

class Particle(turtle.Turtle):
    """Defines any bouncing ball on the game board"""
    def __init__(self, board, colour, mass, position = (0,0), velocity = (0,0)):
        super().__init__()

# colour of ball can be chosen
        self.color(colour)
        self.mass = mass
        self.setposition(position)
        self.velocity = np.array(velocity)
        self.particle_size = 3*self.mass
        self.shape("circle")
        self.collision_count = 0
# ball does not draw itself when setting itself in position
        self.pu()
        self.hideturtle()
        self.board = board
# ball is added to the board on which it moves
        board.add_particle(self)

# collision count label
        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.pu()
        # self.update_collision_label()
    
    def draw(self):
        self.clear()
        self.dot(self.particle_size)
        
    def move(self):
        self.setx(self.xcor() + self.velocity[0])
        self.sety(self.ycor() + self.velocity[1])
        
    #     for particle in self.board.particles:
    #         if particle != self and self.detect_collision(particle):
    #             self.collision_count += 1
    #             self.update_collision_label()
        
    #     self.label.clear()
    #     new_label_x = self.xcor() + 20
    #     new_label_y = self.ycor() + 20
    #     self.label.goto(new_label_x, new_label_y)
        
    # def detect_collision(self, other):
    #     radius1 = 0.5 * self.particle_size
    #     radius2 = 0.5 * other.particle_size
    #     distance = np.linalg.norm(self.pos() - other.pos())
    #     if distance <= radius1 + radius2:
    #         return True
            
#     def update_collision_label(self):
# # setting label position
#         self.label.goto(self.xcor() + 20, self.ycor() + 20)
# # update label display
#         self.label.write(self.collision_count, align="left", font=("Arial", 15, "normal")) 
#         self.board.board.update()  
    
class Game_Board(turtle.Turtle):
    """Defines the game board on which the bouncing balls collide"""
    def __init__(self, width, height):
        super().__init__()
        
        self.pu()
        self.hideturtle()
        self.width = width
        self.height = height
        self.board = turtle.Screen()
        self.board.title("Bouncing Ball Simulation")
        self.board.setup(width, height)
        self.board.tracer(0)
        self.board.bgcolor("white")
        self.board.onkey(self.change_board, "space")
        self.board.listen()
        
# list of particles
        self.particles = []
    
    def add_particle(self, particle):
        self.particles.append(particle)
            
# updates position of all particles
    def update_particles(self):
        for particle in self.particles:
            particle.move()
            particle.draw()
            # particle.update_collision_label()
        self.board.update()
    
    def change_board(self):
        v_x = -10
        v_y = -5
        self.width += v_x
        self.height += v_y
        self.board.setup(self.width, self.height)

    def wall_bounce(self, particle: Particle):  
        radius = 0.5 * particle.particle_size           
        if particle.velocity[0] < 0:
            if particle.xcor() - radius <= -self.width/2:
                particle.velocity[0] *=- 1
        else:
            if particle.xcor() + radius >= self.width/2:
                particle.velocity[0] *=- 1
        if particle.velocity[1] < 0:
            if particle.ycor() - radius <= -self.width/2:
                particle.velocity[1] *=- 1
        else:
            if particle.ycor() + radius >= self.width/2:
                particle.velocity[1] *= -1

    def is_collision(self, first: Particle, second: Particle):
        distance = np.linalg.norm(first.pos() - second.pos())
        if distance <= 0.5*(first.particle_size + second.particle_size):
            return True

    def resolve_collision(self, first: Particle, second: Particle):
# from conservation of momentum and kinetic energy
        total_mass = first.mass + second.mass
# create copy of initial velocities at point of collision
        u1 = first.velocity
        u2 = second.velocity
# calculate new velocities after collision
        v1 = ((first.mass-second.mass)/total_mass)*u1 \
            + (2*second.mass/total_mass)*u2
        v2 = ((second.mass-first.mass)/total_mass)*u2 \
            + (2*second.mass/total_mass)*u1
# replace particle velocity with new velocity
        first.velocity = v1
        second.velocity = v2
        
    def check_collisions(self):
# loop through each (i) particle and check whether is_collision is satsified with every other particle (j)
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                particle1 = self.particles[i]
                particle2 = self.particles[j]
# call resolve_collision if condition met
                if self.is_collision(particle1, particle2):
                    self.resolve_collision(particle1, particle2)
# loop through all particles in list and call wall_bounce
        for _ in self.particles:
            self.wall_bounce(_)
       
board1 = Game_Board(700, 700)

# balls on which position data is taken
ball1 = Particle(board1, "red", 10, position = (200,0), velocity = (3,6))
ball2 = Particle(board1, "green", 10, position = (0,-200), velocity = (-3,9))

balls = (
    Particle(board1, "black", 10, position = (50,0), velocity = (3,6)),
    Particle(board1, "black", 10, position = (100,0), velocity = (-3,9)),
    Particle(board1, "black", 10, position = (0,50), velocity = (-4,-6)),
    Particle(board1, "black", 10, position = (0, 100), velocity = (5,6))
    )

while True:
    board1.update_particles()
    board1.check_collisions()
                        
                
                
            
            
            
        
        
        