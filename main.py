import pygame
from Pendulum import *



def main():
    pygame.init()

    screen_size = (1280, 720)

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    running = True

    delta_time = 0

    pendulum_origin = pygame.Vector2(screen_size[0]/2, 100)
    pendulum = Pendulum(pivot_x=pendulum_origin.x, pivot_y = pendulum_origin.y, m1=40, m2=20, l1=350, l2=200, theta1=90, theta2=-90, g=1, damping=0.999)
    pendulum_pos_1 = pygame.Vector2()
    pendulum_pos_2 = pygame.Vector2()

    while running:

        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("white")

        # Update
        pendulum.update()
        mass_position1, mass_position2 = pendulum.get_pos()
        pendulum_pos_1.update(mass_position1)
        pendulum_pos_2.update(mass_position2)

        # Render
        pygame.draw.circle(screen, "green", pendulum_pos_1, pendulum.m1)
        pygame.draw.circle(screen, "red", pendulum_pos_2, pendulum.m2)
        pygame.draw.line(screen, "black", pendulum_origin, pendulum_pos_1, width=5)
        pygame.draw.line(screen, "black", pendulum_pos_1, pendulum_pos_2, width=5)

        # Put updates on screen
        pygame.display.flip()

        delta_time = clock.tick(60) / 1000
    
    pygame.quit()


if __name__ == "__main__":
    main()