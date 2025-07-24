import pygame
import math

# Initialize Pygame
pygame.init()
print("PROGRAM INITALIZED")

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
d_T = 100 * 86400 / 60 # timestep (delta time)
d_T_int_step = 1000
G = 6.6743e-11
EARTH_M = 5.972e+24
SUN_M = 1.9891e+30
MOON_M = 7.34767309e+22
METERS_PER_PIXEL = 1.496e+9
frames = 0
offset = pygame.math.Vector2(0,0)
track_CoM = False

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Solar System")

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
        pygame.draw.circle(screen, self.color, self.pos + offset, self.radius)


# Main loop
running = True

# things
earth = Planet(300, 400, 29780, 0, (0,0,255), 2, EARTH_M)
sun = Planet(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 1000, 0, (255, 255, 0), 20, SUN_M)
luna = Planet(300, 400 + 0.25695552898, 29780 + 1018, 0, (200,200,200), 1, MOON_M)
bodies = [earth, sun, luna]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            running = False
         
    

    screen.fill((0,0,0))
    for i in range(d_T_int_step):
        earth.update(d_T_int_step, bodies)
        luna.update(d_T_int_step, bodies)
        sun.update(d_T_int_step, bodies)
    
    keys = pygame.key.get_pressed()
    CoM = ((sun.pos * sun.mass + earth.pos * earth.mass + luna.pos * luna.mass) / (sun.mass + earth.mass + luna.mass))
    if keys[pygame.K_a]:
        offset += pygame.math.Vector2(10,0)
    if keys[pygame.K_d]:
        offset += pygame.math.Vector2(-10,0)
    if keys[pygame.K_w]:
        offset += pygame.math.Vector2(0,10)
    if keys[pygame.K_s]:
        offset += pygame.math.Vector2(0,-10)
    if keys[pygame.K_SPACE]:
        if track_CoM == False:
            track_CoM = True
        else:
            track_CoM = False
    if track_CoM == True:
        offset = -(CoM - pygame.math.Vector2(300,300))
    
    
    earth.draw()
    luna.draw()
    sun.draw()
    frames += 1
    #print("frames elapsed:",frames)


    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
