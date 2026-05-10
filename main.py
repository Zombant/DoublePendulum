import pygame
from Pendulum import *
from PendulumRenderer import *

def main():
    pygame.init()

    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    screen_size = (1280, 720)

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    # Create a 2D pendulum
    # pendulum_pivot = pygame.Vector2(screen_size[0]/2, 100)
    # pendulum = Pendulum2D(pivot=pendulum_pivot, m1=40, m2=10, l1=370, l2=200, theta1=90, theta2=180, g=0.3, damping=0.9999)
    # # Create renderer
    # pendulum_renderer = PendulumRenderer2D(pendulum)

    # Create a 3D pendulum
    pendulum_pivot = pygame.Vector3(0, 0, 0)
    pendulum = Pendulum3D(pivot=pendulum_pivot, m1=40, m2=10, l1=100, l2=100, theta1=90, theta2=80, phi1=100, phi2=0, g=100, damping=0.999)
    # # Create renderer
    pendulum_renderer = PendulumRenderer3D(pendulum, Vector2(1280/2, 720/2), d=600)

    move_speed = 100
    rotate_speed = 1

    while running:

        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_rel()
        if keys[pygame.K_w]:
            pendulum_renderer.camera_pos += Vector3(0, -1, 0) * move_speed * delta_time
        if keys[pygame.K_s]:
            pendulum_renderer.camera_pos += Vector3(0, 1, 0) * move_speed * delta_time
        if keys[pygame.K_a]:
            pendulum_renderer.camera_pos += Vector3(1, 0, 0) * move_speed * delta_time
        if keys[pygame.K_d]:
            pendulum_renderer.camera_pos += Vector3(-1, 0, 0) * move_speed * delta_time
        if keys[pygame.K_SPACE]:
            pendulum_renderer.camera_pos += Vector3(0, 0, -1) * move_speed * delta_time
        if keys[pygame.K_LCTRL]:
            pendulum_renderer.camera_pos += Vector3(0, 0, 1) * move_speed * delta_time
        
        pendulum_renderer.camera_yaw += -1 * rotate_speed * delta_time * mouse[0]
        pendulum_renderer.camera_pitch += 1 * rotate_speed * delta_time * mouse[1]
        
        
        screen.fill("white")

        # Update
        pendulum_renderer.update(delta_time)

        # Render
        pendulum_renderer.render(screen)

        # Put updates on screen
        pygame.display.flip()

        delta_time = clock.tick(60) / 1000
    
    pygame.quit()


if __name__ == "__main__":
    main()