import pygame
import pymunk.pygame_util
import random


# Import file with the constants we need.
import constants


pymunk.pygame_util.positive_y_is_up = False


def create_square_at_pos(space: pymunk.Space, pos: tuple, elasticity: float = 0.8, friction: float  = 1.0) -> None:
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

    # Randomize the square's color.
    shape.color = [random.randrange(256) for i in range(4)]
    space.add(body, shape)


pygame.init()
pygame.font.init()


surface = pygame.display.set_mode(constants.RES)


clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial" , 18 , bold = True)


draw_options = pymunk.pygame_util.DrawOptions(surface)


# PyMunk Settings
space = pymunk.Space()
space.gravity = 0, constants.g


# Let's add a floor to our simulation.
segment_shape = pymunk.Segment(space.static_body, (1, constants.HEIGHT), (constants.WIDTH, constants.HEIGHT), 16)
space.add(segment_shape)
segment_shape.elasticity = 0.6
segment_shape.friction = 1.0


# Drawing a game each frame
while True:
    surface.fill(pygame.Color('black'))


    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()


        # If we press the left mouse button, then a square is spawned at this exact position.
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                create_square_at_pos(space, i.pos, random.randrange(0, 1), random.randrange(0, 1))
                


    # PyMunk Cycle
    space.step(1 / constants.FPS)
    space.debug_draw(draw_options)


    text = font.render(str(int(clock.get_fps())), False, (0, 255, 0))
    surface.blit(text, (0, 0))


    pygame.display.flip()
    clock.tick(constants.FPS)
    
