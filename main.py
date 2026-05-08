import pygame
from Pendulum import *
from PendulumRenderer import *

def main():
    pygame.init()

    screen_size = (1280, 720)

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    # Create a pendulum
    pendulum_origin = pygame.Vector2(screen_size[0]/2, 100)
    pendulum = Pendulum2D(pivot=pendulum_origin, m1=20, m2=10, l1=370, l2=200, theta1=90, theta2=180, g=0.3, damping=0.9999)
    # Create renderer
    pendulum_renderer = PendulumRenderer2D(pendulum)

    while running:

        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("white")

        # Update
        pendulum_renderer.update()

        # Render
        pendulum_renderer.render(screen)

        # Put updates on screen
        pygame.display.flip()

        delta_time = clock.tick(144) / 1000
    
    pygame.quit()


if __name__ == "__main__":
    main()