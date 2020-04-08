import pygame
import game
import random

BLOCK_SPACING = 10
BLOCK_WIDTH = 80


def render_game_grid(window, font, grid: game.GameGrid):
    elements = grid.get_elements()

    for y, row in enumerate(elements):
        for x, col in enumerate(row):
            rect_x = x * (BLOCK_SPACING + BLOCK_WIDTH) + BLOCK_SPACING
            rect_y = y * (BLOCK_SPACING + BLOCK_WIDTH) + BLOCK_SPACING
            pygame.draw.rect(window, game.get_color_for_number(col),
                             pygame.Rect(rect_x,
                                         rect_y,
                                         BLOCK_WIDTH, BLOCK_WIDTH))
            # Don't render text for 0
            if col == 0:
                continue

            text = font.render(str(col), True, (119, 110, 101) if col <= 4 else (255, 255, 255))
            window.blit(text, (rect_x + (float(BLOCK_WIDTH) / 2) - float(text.get_width()) / 2,
                               rect_y + (float(BLOCK_WIDTH) / 2) - float(text.get_height()) / 2))


if __name__ == "__main__":
    pygame.init()
    font = pygame.font.Font("fonts/ClearSans-Bold.ttf", 32)

    window = pygame.display.set_mode(
        ((BLOCK_SPACING + BLOCK_WIDTH) * 4 + BLOCK_SPACING, (BLOCK_SPACING + BLOCK_WIDTH) * 4 + BLOCK_SPACING))
    pygame.display.set_caption("2048 NEAT Game")
    game_grid = game.GameGrid()

    running = True
    window.fill((187, 173, 160))  # TODO: Move this in the loop if we do move animations for the numbers
    while running:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False
            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_q:
                running = False
            if evt.type == pygame.KEYDOWN and (evt.key == pygame.K_a or evt.key == pygame.K_LEFT):
                game_grid.do_move(game.MoveDirection.LEFT)
            if evt.type == pygame.KEYDOWN and (evt.key == pygame.K_d or evt.key == pygame.K_RIGHT):
                game_grid.do_move(game.MoveDirection.RIGHT)
            if evt.type == pygame.KEYDOWN and (evt.key == pygame.K_w or evt.key == pygame.K_UP):
                game_grid.do_move(game.MoveDirection.UP)
            if evt.type == pygame.KEYDOWN and (evt.key == pygame.K_s or evt.key == pygame.K_DOWN):
                game_grid.do_move(game.MoveDirection.DOWN)
        render_game_grid(window, font, game_grid)
        pygame.display.flip()
