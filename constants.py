import scipy


"""

Here we have all the constant values our program need to operate properly.
g -> small g used, for example, in gravitational force law: F=mg.
G -> big g, which is present in the Newton's Gravitational Law.

RES -> the resolution of the window.
FPS -> how many times per second the window changes its properties.

"""

is_paused = False


g = scipy.constants.g
G = scipy.constants.G


RES = WIDTH, HEIGHT = 900, 720
FPS = 60


bodies_index = {1: 'box', 2: 'circle', 3: 'triangle'}


scalar_size: float = 1.0


