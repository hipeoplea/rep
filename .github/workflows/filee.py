import pygame


class Tables:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.table = [[0] * w for _ in range(h)]

        self.left = 3
        self.right = 3
        self.top = 3
        self.cell_size = 6

    def set_view(self, left, right, top, cell_size):
        self.left = left
        self.top = top
        self.right = right
        self.cell_size = cell_size

    def render(self, screen):
        colors = [pygame.Color('black'), pygame.Color('red'), pygame.Color('blue')]
        for i in range(self.h):
            for j in range(self.w):
                pygame.draw.rect(screen, colors[self.table[j][i]], (
                    self.left + i * self.cell_size, self.top + j * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color('white'), (
                    self.left + i * self.cell_size, self.top + j * self.cell_size, self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_position):
        cell_x = (mouse_position[0] - self.left) // self.cell_size
        cell_y = (mouse_position[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.w or cell_y < 0 or cell_y >= self.h:
            return None
        return cell_x, cell_y

    def on_click(self, cell_coordinate):
        self.table[cell_coordinate[1]][cell_coordinate[0]] = \
            (self.table[cell_coordinate[1]][cell_coordinate[0]] + 1) % 2
        # for i in range(self.w):
        #     self.table[cell_coordinate[1]][i] = (self.table[cell_coordinate[1]][i] + 1) % 2
        # for i in range(self.h):
        #     if i == cell_coordinate[1]:
        #         continue
        #     self.table[i][cell_coordinate[0]] = (self.table[i][cell_coordinate[0]] + 1) % 2

    def get_click(self, mouse_position):
        cell = self.get_cell(mouse_position)
        if cell:
            self.on_click(cell)


if __name__ == '__main__':
    table = Tables(30, 30)
    pygame.init()

    size = w, h = (670, 650)
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                table.get_click(event.pos)

        table.set_view(40, 40, 20, 20)
        table.render(screen)
        pygame.display.flip()
    pygame.quit()