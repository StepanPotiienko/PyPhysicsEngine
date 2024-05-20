import pygame
import pymunk.pygame_util
import random
import time

# Import file with the constants we need.
import constants


pymunk.pygame_util.positive_y_is_up = False


class Object:
    object_type: str = 'circle'
    mass: float = 1.0

    def __init__(self, mass: float, object_type: str):
        self.mass = mass
        self.object_type = object_type


    # TODO: Implement a system where user can choose which object to place.
    def create_at_pos(self, space: pymunk.Space, pos: tuple, elasticity: float = 0.8, friction: float = 1.0) -> None:
        if self.object_type is not 'triangle':

            body = pymunk.Body(self.mass, 1)

            body.position = pos
        
            if self.object_type == 'circle':
                shape = pymunk.Circle(body, 100 * constants.scalar_size)

            elif self.object_type == 'box':
                shape = pymunk.Poly.create_box(body, (100 * constants.scalar_size, 100 * constants.scalar_size))
        
            shape.color = [random.randrange(256) for i in range(4)]
            space.add(body, shape)
       
        else:
            points = (0,0), (50,0), (25,50)
            moment = pymunk.moment_for_poly(self.mass, points)

            triangle_body = pymunk.Body(self.mass, moment)
            triangle_body.position = pos

            shape = pymunk.Poly(triangle_body, points)
            
            shape.color = [random.randrange(256) for i in range(4)]
            space.add(triangle_body, shape)
            

class UI:
    pass


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

   
body_id = 1   
# Drawing a game each frame
while True:
    surface.fill(pygame.Color('black'))
   
    game_gui = UI()

    
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

            if event.key == pygame.K_c:
                body_id += 1

                if body_id > len(constants.bodies_index):
                    body_id = 1

            if event.key == pygame.K_v:
                constants.scalar_size += 1

                if constants.scalar_size > 3:
                    constants.scalar_size = 1

        """
        
        To implement choosing between different bodies I can use dictionaries.
        For example, when I press 'C' key, the switch goes from 0 to 1, and 
        '1' is the key in dictionary for 'cube' body.

            
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                obj = Object(mass=15, object_type=constants.bodies_index[body_id])
                obj.create_at_pos(space, event.pos, 0.8, 0.5)

        
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
    
