import pygame
from Pendulum import *

class PendulumRenderer(ABC):

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass

class PendulumRenderer2D(PendulumRenderer):
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

class PendulumRenderer3D(PendulumRenderer):
    def __init__(self, pendulum: Pendulum, screen_center: Vector2, d: float):
        self.pendulum = pendulum
        self.screen_center = screen_center

        self.pendulum_pivot = pygame.Vector2()
        self.pendulum_pos_1 = pygame.Vector2()
        self.pendulum_pos_2 = pygame.Vector2()
        self.bob_depth1 = d
        self.bob_depth2 = d

        self.screen_d = d

        self.camera_pos = Vector3(0, 0, 0)
        self.camera_yaw = 0.0
        self.camera_pitch = 0.0

    def update(self, delta_time):
        self.pendulum.update(delta_time)
        mass_position1, mass_position2 = self.pendulum.get_pos()

        points = [self.pendulum.pivot, mass_position1, mass_position2]
        processed_points = []

        for point in points:
            # Transform
            p_view = point - self.camera_pos

            # Rotate
            p_rot = p_view.rotate_z(self.camera_yaw)
            p_rot = p_rot.rotate_x(self.camera_pitch)
            processed_points.append(p_rot)

        self.pivot_depth =max(processed_points[0].y + self.screen_d, 0.1)
        self.bob_depth1 = max(processed_points[1].y + self.screen_d, 0.1)
        self.bob_depth2 = max(processed_points[2].y + self.screen_d, 0.1)

        # Project to 2D
        proj_pivot = processed_points[0].uv(self.screen_d, camera_distance=600)
        proj1 = processed_points[1].uv(self.screen_d, camera_distance=600)
        proj2 = processed_points[2].uv(self.screen_d, camera_distance=600)

        self.pendulum_pivot.update(*(proj_pivot + self.screen_center))
        self.pendulum_pos_1.update(*(proj1 + self.screen_center))
        self.pendulum_pos_2.update(*(proj2 + self.screen_center))

    def render(self, screen: pygame.Surface):
        r1 = max(1, int(self.pendulum.m1 * (self.screen_d / self.bob_depth1)))
        r2 = max(1, int(self.pendulum.m2 * (self.screen_d / self.bob_depth2)))

        rod1_depth = (self.pivot_depth + self.bob_depth1) / 2.0
        rod2_depth = (self.bob_depth1 + self.bob_depth2) / 2.0

        render_queue = [
            {
                "type": "line", 
                "depth": rod1_depth, 
                "start": self.pendulum_pivot, 
                "end": self.pendulum_pos_1
            },
            {
                "type": "line", 
                "depth": rod2_depth, 
                "start": self.pendulum_pos_1, 
                "end": self.pendulum_pos_2
            },
            {
                "type": "circle", 
                "depth": self.bob_depth1, 
                "color": "green", 
                "pos": self.pendulum_pos_1, 
                "radius": r1
            },
            {
                "type": "circle", 
                "depth": self.bob_depth2, 
                "color": "red", 
                "pos": self.pendulum_pos_2, 
                "radius": r2
            }
        ]

        render_queue.sort(key=lambda item: item["depth"], reverse=True)

        for item in render_queue:
            if item["type"] == "line":
                pygame.draw.line(screen, "black", item["start"], item["end"], width=5)
            elif item["type"] == "circle":
                pygame.draw.circle(screen, item["color"], item["pos"], item["radius"])
        