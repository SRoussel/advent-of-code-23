"""Advent of code day 24 (part 2)."""

import numpy

COORD_MIN = 200000000000000

class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.vz = velocity[2]
        self.m = float(velocity[1]) / float(velocity[0])

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'
    
    def in_past(self, position):
        return self.time_from_position(position) < 0

    def time_from_position(self, position):
        return (position[0] - self.x) / self.vx

    def z_at_time(self, time):
        return self.z + (time * self.vz)

    def z_from_x_y(self, x, y):
        time = self.time_from_position((x,y))
        return self.z + (time * self.vz)

def find_intersection(particle_a, particle_b):
    if (particle_a.m == particle_b.m):
        return None

    x = (((-1 * particle_b.m) * particle_b.x) + particle_b.y + (particle_a.m * particle_a.x) - particle_a.y) / (particle_a.m - particle_b.m)
    y = particle_a.m * (x - particle_a.x) + particle_a.y
    z = particle_a.z_from_x_y(x,y)
    return (x, y, z)

def system(a, b, c):
    vel_y = ((c.y * c.vx * a.y) - (c.y * c.vx * b.y) + (c.x * c.vy * a.y) - (c.x * c.vy * b.y) + (a.y * a.y * a.vx)\
        -  (a.y * a.vx * b.y) - (a.x * a.y * a.vy) + (a.x * a.vy * b.y) - (b.y * b.vx * a.y) + (b.y * b.vx * c.y)\
        - (b.x * b.vy * a.y) + (b.x * b.vy * c.y) - (a.y * a.y * a.vx) + (a.y * a.vx * c.y) + (a.x * a.vy * a.y)\
        - (a.x * a.vy * c.y)) / ((a.x * a.y) - (a.x * c.y) - (b.x * a.y) + (b.x * c.y) - (a.x * a.y) + (a.x * b.y) - (c.x * a.y) + (c.x * b.y))

    return vel_y

def beta_create_equation(a, b):
    return (a.vx - b.vx, a.y - b.y, -a.vy + b.vy, -a.x + b.x, ((a.y * a.vx) - (a.x * a.y) - (b.y * b.vx) + (b.x * b.y)))

def create_equation(a, b):
    return (a.vy - b.vy, b.vx - a.vx, -a.y + b.y, a.x - b.x, (a.x * a.vy) - (a.y * a.vx) - (b.x * b.vy) + (b.y * b.vx))

def velocity_adjust():
    return (3, -1, -2)

def run(filename):
    """Return."""
    with open(filename) as file:
        lines = file.readlines()
    
    particles = []
    for line in lines:
        line = line.strip('\n')
        pos, vel = line.split(' @ ')
        x, y, z = pos.split(', ')
        vx, vy, vz = vel.split(', ')
        particles.append(Particle((float(x) - COORD_MIN, float(y) - COORD_MIN, float(z) - COORD_MIN), (float(vx), float(vy), float(vz))))
    
    intersections = 0

    equation_a = create_equation(particles[0], particles[1])
    equation_b = create_equation(particles[0], particles[2])
    equation_c = create_equation(particles[0], particles[3])
    equation_d = create_equation(particles[0], particles[4])

    system = numpy.array([[*equation_a[:-1]], [*equation_b[:-1]], [*equation_c[:-1]], [*equation_d[:-1]]])
    rhs = numpy.array([equation_a[4], equation_b[4], equation_c[4], equation_d[4]])

    sol_x, sol_y, sol_vx, sol_vy = numpy.linalg.solve(system, rhs)
    time_a = (sol_x - particles[0].x) / (particles[0].vx - sol_vx)
    time_b = (sol_x - particles[1].x) / (particles[1].vx - sol_vx)

    z_time_a = particles[0].z_at_time(time_a)
    z_time_b = particles[1].z_at_time(time_b)

    sol_vz = (z_time_b - z_time_a) / (time_b - time_a)
    sol_z = z_time_a - (time_a * sol_vz)
 
    sol_particle = Particle((sol_x, sol_y, 0), (sol_vx, sol_vy, 0))

    for particle in particles:
        intersection = find_intersection(particle, sol_particle)
        if intersection != None:
            x, y, z = intersection
            if not particle.in_past(intersection) and not sol_particle.in_past(intersection):
                intersections += 1

    return round(sol_x + COORD_MIN) + round(sol_y + COORD_MIN) + round(sol_z + COORD_MIN)