import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
d_T = 1 # timestep (delta time)
G = .005

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
        
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.vel += pygame.math.Vector2(0.1,0)
        
        if keys[pygame.K_a]:
            self.vel += pygame.math.Vector2(-0.1,0)
        
        if keys[pygame.K_w]:
            self.vel += pygame.math.Vector2(0,-0.1)
        
        if keys[pygame.K_s]:
            self.vel += pygame.math.Vector2(0,0.1)

        if keys[pygame.K_SPACE]:
            self.vel = pygame.math.Vector2(0,0)
        

        r2 = self.pos.distance_squared_to(sun.pos)

        f_g = ((G * self.mass * sun.mass) / r2)

        theta = 180-(self.pos-sun.pos).angle_to(sun.pos-sun.pos)

        f = pygame.math.Vector2.from_polar( (f_g , theta))

        a = f / self.mass
       
        self.vel += a * d_T
        self.pos += self.vel * d_T



        print(self.pos, sun.pos, f)

        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        pygame.draw.line(screen, (255, 0, 0), self.pos, self.pos + f * 5000, 2)  






# Main loop
running = True

# things
earth = Planet(300, 100, 0, 0, (0,0,255), 10, 100)
sun = Star(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, (255, 255, 0), 50, 1000)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            running = False
         
    

    screen.fill((0,0,0))
    sun.update()
    earth.update()
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
