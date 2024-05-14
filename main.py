import pygame
import pymunk.pygame_util
import random
import time

# Import file with the constants we need.
import constants


pymunk.pygame_util.positive_y_is_up = False


class Circle():
    radius: float = 1.0


    def __init__(self, radius):
        self.radius = radius
    
    def create_at_pos(self, space: pymunk.Space, pos: tuple, elasticity: float = 0.8, friction: float = 1.0) -> None:
        mass = 1
        moment = pymunk.moment_for_circle(mass, self.radius, outer_radius=1)
        body = pymunk.Body(mass, moment)

        # Create a box at a mouse position.
        body.position = pos
        shape = pymunk.Circle(body, self.radius)

        shape.elasticity = elasticity
        shape.friction = friction

        shape.color = [random.randrange(256) for i in range(4)] 
        space.add(body, shape)


class Square():
    timeAlive = 0.0
    isOnTheScene = False


    def __init__(self):
        self.render_time()


    def time(self):
        while self.isOnTheScene:
            timeAlive += 1
            time.sleep(1000)
   
            print(timeAlive)

        return self.timeAlive
    

    def render_time(self):
        surface.blit(font.render(str(self.time()), False, (0, 255, 0)), (100, 100))

            
    # TODO: Output square's velocity right next to it. For this I should come up with a way to calculate it using s=v0t+at^2/2.
    def create_at_pos(self, space: pymunk.Space, pos: tuple, elasticity: float = 0.8, friction: float  = 1.0) -> None:
        """
        
        Creates a square at the position specified as a pos variable, changes its color to a random one,
        and adds it to the PyMunk space.

        space - PyMunk space.
        pos - the position of a square.
        elasticity - how does a square repel any changes to its form.
        friction - how does a square does not like to move.

        """
        mass, size = 1, (60, 60)
        moment = pymunk.moment_for_box(mass, size)
        body = pymunk.Body(mass, moment)

        # Create a box at a mouse position.
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = elasticity
        shape.friction = friction

        
        square = Square()


        # Randomize the square's color.
        shape.color = [random.randrange(256) for i in range(4)]
        space.add(body, shape)


pygame.init()
pygame.font.init()

surface = pygame.display.set_mode(constants.RES)


clock = pygame.time.Clock()
font = pygame.font.SysFont("Fira Code" , 18 , bold = True)


draw_options = pymunk.pygame_util.DrawOptions(surface)


# PyMunk Settings
space = pymunk.Space()
space.gravity = 0, constants.g


# Let's add a floor to our simulation.
segment_shape = pymunk.Segment(space.static_body, (1, constants.HEIGHT), (constants.WIDTH, constants.HEIGHT), 16)
space.add(segment_shape)
segment_shape.elasticity = 0.6
segment_shape.friction = 1.0


def change_g(nv: float) -> None:
    constants.g += nv 
    space.gravity = 0, constants.g


# Drawing a game each frame
while True:
    surface.fill(pygame.Color('black'))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        # TODO: Stop game from freezing when entering commands in the console.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                pygame.event.poll()
                clock.tick(1)
                constants.is_paused = True
                print("You can enter commands here while the engine is running: ")
                
                while event.key != pygame.K_p:
                    command = str(input())
                    
                    if command == 'exit':
                        constants.is_paused = False


                
            if event.key == pygame.K_p:
                constants.is_paused = False 


        # If we press the left mouse button, then a square is spawned at this exact position.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # square = Square()
                # square.create_at_pos(space, event.pos, random.randrange(0, 1), random.randrange(0, 1))
       
                circle = Circle(radius=100.0)
                circle.create_at_pos(space, event.pos, random.randrange(0, 1), random.randrange(0,1 ))

        
        keys = pygame.key.get_pressed()        

        if keys[pygame.K_q]:
            exit()


    # PyMunk Cycle
    if constants.is_paused == False:
        space.step(1 / constants.FPS)
        space.debug_draw(draw_options)



        text = font.render(str(int(clock.get_fps())), False, (0, 255, 0))
        surface.blit(text, (0, 0))

    
        g_text = font.render("g: " + str(constants.g), False, (0, 255, 0))
        surface.blit(g_text, (50, 0))


        pygame.display.flip()
        clock.tick(constants.FPS)
    
