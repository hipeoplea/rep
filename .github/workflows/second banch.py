import filee
import pygame
from copy import deepcopy


class Life(filee.Tables):



if __name__ == '__main__':
    table = Life(30, 30)
    pygame.init()

    size = w, h = (670, 650)
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.:
                table.get_click(event.pos)

        table.set_view(40, 40, 20, 20)
        table.render(screen)
        pygame.display.flip()
    pygame.quit()