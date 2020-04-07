import pygame
import game
import random

BLOCK_SPACING = 10
BLOCK_WIDTH = 80


def render_game_grid(window, font, grid: game.GameGrid):
    elements = grid.get_elements()

    for y, row in enumerate(elements):
        print(row)
        for x, col in enumerate(row):
            rect_x = x * (BLOCK_SPACING + BLOCK_WIDTH) + BLOCK_SPACING
            rect_y = y * (BLOCK_SPACING + BLOCK_WIDTH) + BLOCK_SPACING
            pygame.draw.rect(window, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                             pygame.Rect(rect_x,
                                         rect_y,
                                         BLOCK_WIDTH, BLOCK_WIDTH))
            text = font.render(str(col), True, (255, 255, 255))
            window.blit(text, (rect_x + (float(BLOCK_WIDTH) / 2) - float(text.get_width()) / 2,
                        rect_y + (float(BLOCK_WIDTH) / 2) - float(text.get_height()) / 2))


if __name__ == "__main__":
    pygame.init()
    font = pygame.font.Font(None, 24)

    window = pygame.display.set_mode(
        ((BLOCK_SPACING + BLOCK_WIDTH) * 4 + BLOCK_SPACING , (BLOCK_SPACING + BLOCK_WIDTH) * 4 + BLOCK_SPACING))
    pygame.display.set_caption("2048 NEAT Game")
    game_grid = game.GameGrid()

    render_game_grid(window, font, game_grid)
    running = True
    while running:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False
            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_q:
                running = False

        pygame.display.flip()
