import pygame
from Pendulum import *

class PendulumRenderer2D:
    def __init__(self, pendulum: Pendulum):
        self.pendulum = pendulum
        self.pendulum_pos_1 = pygame.Vector2()
        self.pendulum_pos_2 = pygame.Vector2()

    def update(self):
        self.pendulum.update()
        mass_position1, mass_position2 = self.pendulum.get_pos()
        self.pendulum_pos_1.update(*mass_position1)
        self.pendulum_pos_2.update(*mass_position2)

    def render(self, screen: pygame.Surface):
        pygame.draw.circle(screen, "green", self.pendulum_pos_1, self.pendulum.m1)
        pygame.draw.circle(screen, "red", self.pendulum_pos_2, self.pendulum.m2)
        pygame.draw.line(screen, "black", pygame.Vector2(*self.pendulum.pivot), self.pendulum_pos_1, width=5)
        pygame.draw.line(screen, "black", self.pendulum_pos_1, self.pendulum_pos_2, width=5)