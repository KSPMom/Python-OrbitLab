import pygame
import math

# Initialize Pygame
pygame.init()
print("PROGRAM INITALIZED")
# Set up the display



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
        self.r2 = (self.pos.distance_to(other.pos) * sim.METERS_PER_PIXEL)**2
        self.theta = 180-(self.pos-other.pos).angle_to(other.pos-other.pos)
        self.f = ((sim.G * self.mass * other.mass) / self.r2)
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
        self.vel += self.acl * sim.d_T / d_T_int_step
        self.pos += self.vel / sim.METERS_PER_PIXEL * sim.d_T / d_T_int_step
        
        #print("vel:",self.vel)
        #print("pos:",self.pos)
        #print("acl:",self.acl)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.pos / sim.zoom) + sim.offset, self.radius / sim.zoom)

class Simulation:
    def __init__(self):
        # Constants
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 600, 600
        self.d_T = 10 * 86400 / 60 # timestep (delta time)
        self.d_T_int_step = 100
        self.G = 6.6743e-11
        self.EARTH_M = 5.972e+24
        self.SUN_M = 1.9891e+30
        self.MOON_M = 7.34767309e+22
        self.METERS_PER_PIXEL = 1.496e+9
        self.offset = pygame.math.Vector2(0,0)
        self.track_CoM = False
        self.track_planet = False
        self.zoom = 1

        

    def run(self):
        # Main loop
        running = True

        # things
        earth = Planet(300, 400, 29780, 0, (0,0,255), 2, self.EARTH_M)
        sun = Planet(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, 1000, 0, (255, 255, 0), 20, self.SUN_M)
        luna = Planet(300, 400 + 0.25695552898, 29780 + 1018, 0, (200,200,200), 1, self.MOON_M)
        bodies = [earth, sun, luna]

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    running = False
                
            

            screen.fill((0,0,0))
            for self.i in range(self.d_T_int_step):
                earth.update(self.d_T_int_step, bodies)
                luna.update(self.d_T_int_step, bodies)
                sun.update(self.d_T_int_step, bodies)
            
            keys = pygame.key.get_pressed()
            CoM = ((sun.pos * sun.mass + earth.pos * earth.mass + luna.pos * luna.mass) / (sun.mass + earth.mass + luna.mass)) / sim.zoom
            if keys[pygame.K_a]:
                sim.offset += (pygame.math.Vector2(10,0))
            if keys[pygame.K_d]:
                sim.offset += (pygame.math.Vector2(-10,0))
            if keys[pygame.K_w]:
                sim.offset += (pygame.math.Vector2(0,10))
            if keys[pygame.K_s]:
                sim.offset += (pygame.math.Vector2(0,-10))
            if keys[pygame.K_SPACE]:
                if self.track_CoM == False:
                    self.track_CoM = True
                else:
                    self.track_CoM = False
            if self.track_CoM == True:
                sim.offset = -(CoM - pygame.math.Vector2(300,300))
            if keys[pygame.K_z]:
                sim.zoom += 0.01
            if keys[pygame.K_x]:
                sim.zoom -= 0.01

            if keys[pygame.K_c]:
                if self.track_planet == False:
                    self.track_planet = True
                else:
                    self.track_planet = False
            
            if self.track_planet == True:
                sim.offset = -(earth.pos / sim.zoom - pygame.math.Vector2(300,300))




            print(sim.zoom)
            
            sun.draw()
            earth.draw()
            luna.draw()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

        # Quit Pygame
        pygame.quit()




sim = Simulation()
screen = pygame.display.set_mode((sim.SCREEN_WIDTH, sim.SCREEN_HEIGHT))
pygame.display.set_caption("Solar System")
sim.run()




