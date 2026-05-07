import numpy as np

class Pendulum:

    # TODO: 3D (or even more? :O)
    # TODO: More bobs
    def __init__(self, pivot_x, pivot_y, m1, m2, l1, l2, theta1, theta2, g=9.8, damping=0.9):
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
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

        self.x1 = 0
        self.y1 = 0
        self.y2 = 0
        self.x2 = 0

        

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
        self.x1 = self.pivot_x + self.l1 * np.sin(self.theta1)
        self.y1 = self.pivot_y + self.l1 * np.cos(self.theta1)

        self.x2 = self.x1 + self.l2 * np.sin(self.theta2)
        self.y2 = self.y1 + self.l2 * np.cos(self.theta2)

        return (self.x1, self.y1), (self.x2, self.y2)