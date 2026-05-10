from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np

# TODO: Move these to new Vector file
@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0

    # Using an instance of this class by name will result in tuple (x, y)
    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, float) or isinstance(other, int):
            return Vector2(self.x + other, self.y + other)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector2(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented
        

@dataclass
class Vector3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    # Using an instance of this class by name will result in tuple (x, y)
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Vector3(self.x + other, self.y + other, self.z + other)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return NotImplemented

    def uv(self, focal_length: float, camera_distance: float = 600.0) -> Vector2:
        "Transform world space (x, y, z) to screen space (u, v)"

        depth = self.y + camera_distance

        if depth <= 0.1:
            depth = 0.1

        u = (self.x * focal_length) / depth
        v = (-self.z * focal_length) / depth
        return Vector2(u, v)

    def rotate_z(self, angle: float):
        "Yaw: Rotates the X and Y (depth) axes around the Z (up) axis"
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        new_x = self.x * cos_a - self.y * sin_a
        new_y = self.x * sin_a + self.y * cos_a
        return Vector3(new_x, new_y, self.z)

    def rotate_x(self, angle: float):
        "Pitch: Rotates the Y (depth) and Z (up) axes around the X axis"
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        new_y = self.y * cos_a - self.z * sin_a
        new_z = self.y * sin_a + self.z * cos_a
        return Vector3(self.x, new_y, new_z)

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

class Pendulum3D(Pendulum):
    def __init__(self, pivot, m1, m2, l1, l2, theta1, theta2, phi1, phi2, g=9.8, damping=0.9):
        self.pivot = Vector3(*pivot)
        self.m1 = m1
        self.m2 = m2
        self.l1 = l1
        self.l2 = l2
        self.theta1 = np.deg2rad(theta1)
        self.theta2 = np.deg2rad(theta2)
        self.phi1 = np.deg2rad(phi1)
        self.phi2 = np.deg2rad(phi2)

        self.g = g
        self.damping = damping

        self.omega_t1 = 0
        self.omega_t2 = 0
        self.omega_p1 = 0
        self.omega_p2 = 0

        self.alpha_t1 = 0
        self.alpha_t2 = 0
        self.alpha_p1 = 0
        self.alpha_p2 = 0

        # Positions of the masses (x, y, z)
        self.pos1 = Vector3()
        self.pos2 = Vector3()

    def get_M(self, q):

        theta1, phi1, theta2, phi2 = q

        mu = self.m1 + self.m2
        delta_phi = phi1 - phi2
        m2_l1_l2 = self.m2 * self.l1 * self.l2

        M = np.zeros((4, 4))

        # Diagonals
        M[0, 0] = mu * self.l1**2
        M[1, 1] = M[0, 0] * (np.sin(theta1)**2 + 1e-5)
        M[2, 2] = self.m2 * self.l2**2
        M[3, 3] = M[2, 2] * (np.sin(theta2)**2 + 1e-5)

        # Coupling
        #M[0, 1] = 0
        #M[1, 0] = 0

        M[0, 2] = m2_l1_l2 * (np.cos(theta1) * np.cos(theta2) * np.cos(delta_phi) + np.sin(theta1) * np.sin(theta2))
        M[2, 0] = M[0, 2]

        M[0, 3] = m2_l1_l2 * np.cos(theta1) * np.sin(theta2) * np.sin(delta_phi)
        M[3, 0] = M[0, 3]

        M[1, 2] = -1 * m2_l1_l2 * np.sin(theta1) * np.cos(theta2) * np.sin(delta_phi)
        M[2, 1] = M[1, 2]

        M[1, 3] = m2_l1_l2 * np.sin(theta1) * np.sin(theta2) * np.cos(delta_phi)
        M[3, 1] = M[1, 3]

        #M[2, 3] = 0
        #M[3, 2] = 0

        return M

    def get_dM_dq(self, q, epsilon=1e-5):
        dM_dq = np.zeros((4, 4, 4))

        # Current state
        q = np.array([self.theta1, self.phi1, self.theta2, self.phi2])

        for k in range(4):
            q_plus = q.copy()
            q_plus[k] += epsilon
            
            q_minus = q.copy()
            q_minus[k] -= epsilon

            M_plus = self.get_M(q_plus)
            M_minus = self.get_M(q_minus)

            dM_dq[k] = (M_plus - M_minus) / (2 * epsilon)

        return dM_dq
            

    def update(self, delta_time):
        mu = self.m1 + self.m2
        q = np.array([self.theta1, self.phi1, self.theta2, self.phi2]) # positions
        q_dot = np.array([self.omega_t1, self.omega_p1, self.omega_t2, self.omega_p2]) # velocities

        ## Mass matrix ##
        M = self.get_M(q)

        ## Gravity vector ##
        G = np.zeros(4)
        G[0] = mu * self.g * self.l1 * np.sin(self.theta1)
        #G[1] = 0
        G[2] = self.m2 * self.g * self.l2 * np.sin(self.theta2)
        #G[3] = 0

        # Coriolis vector
        dM_dq = self.get_dM_dq(q)
        C = np.zeros(4)
        for k in range(4):
            for i in range(4):
                for j in range(4):
                    tmp = dM_dq[i, k, j] - 0.5 * dM_dq[k, i, j]

                    C[k] += tmp * q_dot[i] * q_dot[j]

        # Solver for alphas
        q_dot_dot = np.linalg.solve(M, -C - G)

        self.alpha_t1, self.alpha_p1, self.alpha_t2, self.alpha_p2 = q_dot_dot

        self.omega_t1 += self.alpha_t1 * delta_time
        self.omega_p1 += self.alpha_p1 * delta_time
        self.omega_t2 += self.alpha_t2 * delta_time
        self.omega_p2 += self.alpha_p2 * delta_time

        # Apply damping
        self.omega_t1 *= self.damping
        self.omega_p1 *= self.damping
        self.omega_t2 *= self.damping
        self.omega_p2 *= self.damping

        self.theta1 += self.omega_t1 * delta_time
        self.phi1   += self.omega_p1 * delta_time
        self.theta2 += self.omega_t2 * delta_time
        self.phi2   += self.omega_p2 * delta_time
        


    def get_pos(self):
        self.pos1.x = self.pivot.x + self.l1 * np.sin(self.theta1) * np.cos(self.phi1)
        self.pos1.y = self.pivot.y + self.l1 * np.sin(self.theta1) * np.sin(self.phi1)
        self.pos1.z = self.pivot.z + -1 * self.l1 * np.cos(self.theta1)

        self.pos2.x = self.pos1.x + self.l2 * np.sin(self.theta2) * np.cos(self.phi2)
        self.pos2.y = self.pos1.y + self.l2 * np.sin(self.theta2) * np.sin(self.phi2)
        self.pos2.z = self.pos1.z + -1 * self.l2 * np.cos(self.theta2)

        return self.pos1, self.pos2