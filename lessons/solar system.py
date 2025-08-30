import pygame
import math
import pygame.freetype

# Initialize Pygame
pygame.init()
print("PROGRAM INITALIZED")

# basically a function to create a celestial object
class Planet:
    def __init__(self, x_pos: float, y_pos: float, x_vel: float, y_vel: float, color: tuple, radius: int, mass: int):
        # Variables
        self.color = color
        self.radius = radius
        self.mass = mass
        self.force_i = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(x_pos, y_pos)
        self.vel = pygame.Vector2(x_vel, y_vel)
        self.acl = pygame.Vector2(0, 0)
        
    # function to calculate the force between this object and another object
    def calc_force(self, other: "Planet"):
        self.r2 = (self.pos.distance_to(other.pos) * sim.METERS_PER_PIXEL)**2
        self.theta = 180-(self.pos-other.pos).angle_to(other.pos-other.pos)
        self.f = ((sim.G * self.mass * other.mass) / self.r2)
        self.force_i = pygame.math.Vector2.from_polar((self.f, self.theta))
        return self.force_i
    
    # function to make physics happen
    def update(self, d_T_int_step, others: list["Planet"]):

        self.force = None
        # calculates the force between all other objects on a certain one and adds it up to get a total force vector
        for other in others:
            try:
                self.force_i = self.calc_force(other)
                if self.force is None:
                    self.force = self.force_i
                else:
                    self.force += self.force_i
            except ZeroDivisionError:
                continue

        # make stuff move with newton's laws
        self.acl = self.force / self.mass
        self.vel += self.acl * sim.d_T / d_T_int_step
        self.pos += self.vel / sim.METERS_PER_PIXEL * sim.d_T / d_T_int_step
        
        
    def draw(self):
        # makes a circle to represent the object and a marker that is not affected by zoom
        pygame.draw.circle(screen, self.color, (self.pos * sim.zoom) + sim.offset, self.radius * sim.zoom)
        pygame.draw.circle(screen, (255, 255, 255), (self.pos * sim.zoom) + sim.offset, 1)

# a function to run the simulation and loop because i was forced to make this
class Simulation:
    def __init__(self):
        # Constants/Variables
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 600, 600
        self.d_T = 10 * 86400 / 60 # timestep (delta time)
        self.d_T_int_step = 100 # how much do you account for inaccuracies caused by the sim moving too fast (how many subframes calced in a frame?)
        self.G = 6.6743e-11 # universal gravitational constant
        self.EARTH_M = 5.972e+24
        self.SUN_M = 1.9891e+30
        self.MOON_M = 7.34767309e+22
        self.METERS_PER_PIXEL = 1.496e+9
        self.offset = pygame.math.Vector2(0,0) # camera offset for panning around (visual, does affect physics)
        self.zoom = 1 # zoom multplier
        self.GAME_FONT = pygame.freetype.Font(None, 24)
        self.time_elapsed = 0
        self.track_CoM = True
        self.tracked_planet = "None"

        

    def run(self):
        # Main loop
        running = True

        # Objects
        earth = Planet(300, 400, 29780, 0, (0,0,255), 0.004, self.EARTH_M)
        sun = Planet(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, 0, 0, (255, 255, 0), 0.4, self.SUN_M)
        luna = Planet(300, 400 + 0.25695552898, 29780 + 1018, 0, (200,200,200), 0.001, self.MOON_M)
        jupiter = Planet(300, 820, 13070, 0, (255, 165, 0), 0.045, 1.898e+27)
        mars = Planet(300, 150, -24077, 0, (255, 0, 0), 0.002, 6.4171e+23)
        # LIST ALL BODIES FOR GRAVITY CALCULATION OR IT WON'T WORK
        bodies = [earth, sun, luna, jupiter, mars]

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    running = False
                
            
            """
            to account for errors (integration, euler method)

            calculate subframe [d_T_int_step] times:
                objects.update(d_T_int_step of a total frame)
            """
            for self.i in range(self.d_T_int_step):
                earth.update(self.d_T_int_step, bodies)
                luna.update(self.d_T_int_step, bodies)
                sun.update(self.d_T_int_step, bodies)
                jupiter.update(self.d_T_int_step, bodies)
                mars.update(self.d_T_int_step, bodies)
                
            
            

            # calculate center of mass
            CoM = ((sun.pos * sun.mass + earth.pos * earth.mass + luna.pos * luna.mass) / (sun.mass + earth.mass + luna.mass)) * sim.zoom

            # manage camera tools
            keys = pygame.key.get_pressed()
            # panning
            if keys[pygame.K_a]:
                sim.offset += (pygame.math.Vector2(10,0))
            if keys[pygame.K_d]:
                sim.offset += (pygame.math.Vector2(-10,0))
            if keys[pygame.K_w]:
                sim.offset += (pygame.math.Vector2(0,10))
            if keys[pygame.K_s]:
                sim.offset += (pygame.math.Vector2(0,-10))

            # CoM tracking
            if keys[pygame.K_SPACE]:
                if self.track_CoM == False:
                    self.track_CoM = True
                else:
                    self.track_CoM = False

            if self.track_CoM == True:
                sim.offset = -(CoM - pygame.math.Vector2(300,300))

            # zooming
            if keys[pygame.K_z]:
                sim.zoom *= 1.1
            if keys[pygame.K_x]:
                sim.zoom *= 0.9
            
            # tracking objects
            self.track_planet = True
            if keys[pygame.K_0]:
                self.tracked_planet = "None"

            if keys[pygame.K_1]:
                self.tracked_planet = "Earth"
            if keys[pygame.K_3]:
                self.tracked_planet = "Jupiter"
            if keys[pygame.K_2]:
                self.tracked_planet = "Mars"
            
            if self.tracked_planet == "Jupiter":
                sim.offset = -(jupiter.pos * sim.zoom - pygame.math.Vector2(300,300))
            if self.tracked_planet == "Earth":
                sim.offset = -(earth.pos * sim.zoom - pygame.math.Vector2(300,300))
            if self.tracked_planet == "Mars":
                sim.offset = -(mars.pos * sim.zoom - pygame.math.Vector2(300,300))



            # put stuff on screen so you know what's happening
            sim.zoomstr = "Zoom factor: " + str(sim.zoom)
            sim.track_CoMstr = "Tracking CoM: " + str(sim.track_CoM)
            sim.tracked_planetstr = "Tracked Planet: " + str(self.tracked_planet)
            sim.time_elapsedstr = "Days Elapsed: " + str(self.time_elapsed)


            screen.fill((0,0,0)) # rest screen for next frame to be drawn

            self.GAME_FONT.render_to(screen, (5, 5), sim.zoomstr, (255, 255, 255))
            self.GAME_FONT.render_to(screen, (5, 30), sim.track_CoMstr, (255, 255, 255))
            self.GAME_FONT.render_to(screen, (5, 55), sim.tracked_planetstr, (255, 255, 255))
            self.GAME_FONT.render_to(screen, (5, 80), sim.time_elapsedstr, (255, 255, 255))

            # actually make the planets appear
            sun.draw()
            earth.draw()
            luna.draw()
            jupiter.draw()
            mars.draw()
            self.time_elapsed += self.d_T / 86400

            # manage frame stuff
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        # Quit Pygame
        pygame.quit()



# Make and run sim and screen
sim = Simulation()
screen = pygame.display.set_mode((sim.SCREEN_WIDTH, sim.SCREEN_HEIGHT)) 
pygame.display.set_caption("Solar System")
sim.run()