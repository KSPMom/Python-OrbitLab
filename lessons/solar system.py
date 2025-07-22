import pygame
import math

# Initialize Pygame
pygame.init()
print("PROGRAM INITALIZED")

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
d_T = 10 * 86400 / 60 # timestep (delta time)
d_T_int_step = 1000
G = 6.6743e-11
EARTH_M = 5.972e+24
SUN_M = 1.9891e+30
MOON_M = 7.34767309e+22
METERS_PER_PIXEL = 1.496e+9
frames = 0

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Solar System")

class Star:
    def __init__(self, x_pos: float, y_pos: float, color: tuple, radius: int, mass: int):
        self.color = color
        self.radius = radius
        self.mass = mass
        self.pos = pygame.Vector2(x_pos, y_pos)
        


    def update(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

class Planet:
    def __init__(self, x_pos: float, y_pos: float, x_vel: float, y_vel: float, color: tuple, radius: int, mass: int):
        self.color = color
        self.radius = radius
        self.mass = mass
        self.force_i = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(x_pos, y_pos)
        self.vel = pygame.Vector2(x_vel, y_vel)
        self.acl = pygame.Vector2(0, 0)
        
    def calc_force(self, other: "Planet"):
        self.r2 = (self.pos.distance_to(other.pos) * METERS_PER_PIXEL)**2
        self.theta = 180-(self.pos-other.pos).angle_to(other.pos-other.pos)
        self.f = ((G * self.mass * other.mass) / self.r2)
        self.force_i = pygame.math.Vector2.from_polar((self.f, self.theta))
        return self.force_i
    
    def update(self, d_T_int_step, others: list["Planet"]):

        self.force = None
        for other in others:
            try:
                self.force_i = self.calc_force(other)
                if self.force is None:
                    self.force = self.force_i
                else:
                    self.force += self.force_i
            except ZeroDivisionError:
                continue

        self.acl = self.force / self.mass
        self.vel += self.acl * d_T / d_T_int_step
        self.pos += self.vel / METERS_PER_PIXEL * d_T / d_T_int_step
        
        #print("vel:",self.vel)
        #print("pos:",self.pos)
        #print("acl:",self.acl)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

# Main loop
running = True

# things
earth = Planet(300, 400, 29780, 0, (0,0,255), 2, EARTH_M)
earth2 = Planet(300, 404, 29780, 0, (0,0,255), 2, SUN_M)
sun = Planet(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, 0, (255, 255, 0), 20, SUN_M)
luna = Planet(300, 400 + 0.25695552898, 29780 + 1018, 0, (200,200,200), 1, MOON_M)
bodies = [earth, earth2, sun, luna]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            running = False
         
    

    screen.fill((0,0,0))
    for i in range(d_T_int_step):
        earth.update(d_T_int_step, bodies)
        earth2.update(d_T_int_step, bodies)
        luna.update(d_T_int_step, bodies)
        sun.update(d_T_int_step, bodies)

    
    earth.draw()
    earth2.draw()
    luna.draw()
    sun.draw()
    frames += 1
    print("frames elapsed:",frames)


    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
