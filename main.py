import pygame
import game
import random
import time
import neat
import os
import math
import visualize
from graph_reporter import GraphReporter

BLOCK_SPACING = 10
BLOCK_WIDTH = 80
SETTINGS = {}
SETTINGS['WINDOW_WIDTH'] = (BLOCK_SPACING + BLOCK_WIDTH) * 4 + BLOCK_SPACING + 500
SETTINGS['WINDOW_HEIGTH'] = (BLOCK_SPACING + BLOCK_WIDTH) * 4 + BLOCK_SPACING
SETTINGS['GENERATIONS'] = 100
SETTINGS['DEFAULT_STEP_DELAY'] = 1

COLORS = {}
COLORS["GREY"] = (77, 77, 77)

def get_config_file_path():
    return os.path.join(os.path.dirname(__file__), 'neat-config')

def load_config():
    return neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                       neat.DefaultSpeciesSet, neat.DefaultStagnation,
                       get_config_file_path())

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game_grid = game.GameGrid()
        invalid_moves_in_a_row = 0
        while not game_grid.is_game_over() and invalid_moves_in_a_row < 10:
            inputs = []
            for row in game_grid.get_elements():
                for val in row:
                    inputs.append(val)
            move_one_hot = net.activate(inputs)
            move = game.MoveDirection(move_one_hot.index(min(move_one_hot)))
            valid_move = game_grid.do_move(move)

            # TODO Make legit fitness
            if valid_move:
                genome.fitness = game_grid.get_total_score() # 1.0
                invalid_moves_in_a_row = 0
            else:
                invalid_moves_in_a_row += 1

    
        
def run():
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(load_config())

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    graph_reporter = GraphReporter(stats)
    p.add_reporter(graph_reporter)

    # Run for 300 generations.
    winner = p.run(eval_genomes, SETTINGS['GENERATIONS'])
    graph_reporter.close()

    print('\nBest genome:\n{!s}'.format(winner))
    render_game_with_NN(winner)
    
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

def render_game_with_NN(nn_param ):
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.Font("fonts/ClearSans-Bold.ttf", 32)
    step_delay = SETTINGS['DEFAULT_STEP_DELAY']



    def update_fps():
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text


    window = pygame.display.set_mode((SETTINGS['WINDOW_WIDTH'], SETTINGS['WINDOW_HEIGTH']))
    pygame.display.set_caption("2048 NEAT Game")
    game_grid = game.GameGrid()

    running = True
    nn = neat.nn.FeedForwardNetwork.create(nn_param, load_config())
    invalid_moves_in_a_row = 0
    while not game_grid.is_game_over() and invalid_moves_in_a_row < 10:
        inputs = []
        for row in game_grid.get_elements():
            for val in row:
                inputs.append(val)
        move_one_hot = nn.activate(inputs)
        move = game.MoveDirection(move_one_hot.index(min(move_one_hot)))
        valid_move = game_grid.do_move(move)
        invalid_moves_in_a_row += 0 if valid_move else 1

        render_game_grid(window, font, game_grid, 
            {"nb_invalid_move": invalid_moves_in_a_row,
             "step_delay": step_delay})
        window.blit(update_fps(), (10, 0))
        clock.tick(60)
        pygame.display.flip()
        if game_grid.is_game_over()  and invalid_moves_in_a_row < 10:
            raise SystemExit(0)

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                raise SystemExit(0)
            elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
                step_delay -= 0.2 if step_delay - 0.2 > 0 else 0
        time.sleep(step_delay)
        



def render_game_grid(window, font, grid: game.GameGrid, data: {}):
    window.fill((187, 173, 160))  # TODO: Move this in the loop if we do move animations for the numbers
    elements = grid.get_elements()

    window.blit(pygame.font.SysFont("arial", 32).render("Generation size: " + str(SETTINGS['GENERATIONS']), 1, COLORS["GREY"]), ( 375, 8))
    window.blit(pygame.font.SysFont("arial", 32).render("Score: " + str(grid.get_highscore()), 1, COLORS["GREY"]), ( 375, 40))
    window.blit(pygame.font.SysFont("arial", 32).render("Nb invalid move: " + str(data['nb_invalid_move']), 1, COLORS["GREY"]), ( 375, 72))
    window.blit(pygame.font.SysFont("arial", 32).render("Step delay: " + str(float("{:.2f}".format(data['step_delay']))), 1, COLORS["GREY"]), ( 375, 104))

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
    run()

if __name__ == "__main_":
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.Font("fonts/ClearSans-Bold.ttf", 32)


    def update_fps():
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text


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
        window.blit(update_fps(), (10, 0))
        clock.tick(60)
        pygame.display.flip()
        if game_grid.is_game_over():
            time.sleep(5)
            raise SystemExit(0)
        # pygame.display.update()
