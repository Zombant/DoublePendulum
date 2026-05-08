from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np

@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0

    # Using an instance of this class by name will result in tuple (x, y)
    def __iter__(self):
        yield self.x
        yield self.y

class Pendulum(ABC):

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def get_pos(self):
        pass

class Pendulum2D(Pendulum):

    def __init__(self, pivot, m1, m2, l1, l2, theta1, theta2, g=9.8, damping=0.9):
        self.pivot = Vector2(*pivot)
        self.m1 = m1
        self.m2 = m2
        self.l1 = l1
        self.l2 = l2
        self.theta1 = np.deg2rad(theta1)
        self.theta2 = np.deg2rad(theta2)

        self.g = g
        self.damping = damping

        self.omega1 = 0
        self.omega2 = 0
        self.alpha1 = 0
        self.alpha2 = 0

        # Positions of the masses (x, y)
        self.pos1 = Vector2()
        self.pos2 = Vector2()

        

    def update(self):
        
        # Update alpha
        denominator_part = 2 * self.m1 + self.m2 - self.m2 * np.cos(2 * self.theta1 - 2 * self.theta2)
        self.alpha1 = (-1 * self.g * (2 * self.m1 + self.m2) * np.sin(self.theta1) - self.m2 * self.g * np.sin(self.theta1 - 2 * self.theta2) - 2 * np.sin(self.theta1 - self.theta2) * self.m2 * (self.omega2**2 * self.l2 + self.omega1**2 * self.l1 * np.cos(self.theta1 - self.theta2))) / (self.l1 * denominator_part)
        self.alpha2 = (2 * np.sin(self.theta1 - self.theta2) * (self.omega1**2 * self.l1 * (self.m1 + self.m2) + self.g * (self.m1 + self.m2) * np.cos(self.theta1) + self.omega2**2 * self.l2 * self.m2 * np.cos(self.theta1 - self.theta2))) / (self.l2 * denominator_part)

        # Update velocities
        self.omega1 += self.alpha1
        self.omega2 += self.alpha2

        # Apply damping
        self.omega1 *= self.damping
        self.omega2 *= self.damping

        self.theta1 += self.omega1
        self.theta2 += self.omega2

        

    def get_pos(self):
        self.pos1.x = self.pivot.x + self.l1 * np.sin(self.theta1)
        self.pos1.y = self.pivot.y + self.l1 * np.cos(self.theta1)

        self.pos2.x = self.pos1.x + self.l2 * np.sin(self.theta2)
        self.pos2.y = self.pos1.y + self.l2 * np.cos(self.theta2)

        return self.pos1, self.pos2