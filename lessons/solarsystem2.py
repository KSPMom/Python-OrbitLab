import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
d_T = 86400 / 60 # timestep (delta time)
d_T_inte = 1000
G = 6.6743e-11
EARTH_M = 5.972e+24
SUN_M = 1.9891e+30
METERS_PER_PIXEL = 1.496e+9

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
        self.force = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(x_pos, y_pos)
        self.vel = pygame.Vector2(x_vel, y_vel)
        self.acl = pygame.Vector2(0, 0)
        
    def update(self, d_T_inte: float):
        self.r2 = (self.pos.distance_to(sun.pos) * METERS_PER_PIXEL)**2
        self.theta = 180-(self.pos-sun.pos).angle_to(sun.pos-sun.pos)
        self.f = ((G * self.mass * sun.mass) / self.r2)
        self.force = pygame.math.Vector2.from_polar((self.f, self.theta))
        self.acl = self.force / self.mass
        self.vel += self.acl * d_T / d_T_inte
        self.pos += self.vel / METERS_PER_PIXEL * d_T / d_T_inte
        print("vel:",self.vel)
        print("pos:",self.pos)
        print("acl:",self.acl)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

# Main loop
running = True

# things
earth = Planet(300, 400, 29780, 0, (0,0,255), 2, EARTH_M)
sun = Star(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, (255, 255, 0), 5, SUN_M)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            running = False
         
    

    screen.fill((0,0,0))
    sun.update()
    for i in d_T_inte:
        earth.update(d_T_inte)

    
    earth.draw()
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
