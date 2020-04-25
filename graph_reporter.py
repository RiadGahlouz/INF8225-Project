import copy
import warnings

import graphviz
import matplotlib.pyplot as plt
import numpy as np

from neat.reporting import BaseReporter


class GraphReporter(BaseReporter):
    def __init__(self, stats):
        self.stats = stats
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        plt.ioff()

    def post_evaluate(self, config, population, species, best_genome):
        statistics = self.stats

        plt.ion()
        generation = range(len(statistics.most_fit_genomes))
        best_fitness = [c.fitness for c in statistics.most_fit_genomes]
        avg_fitness = np.array(statistics.get_fitness_mean())
        stdev_fitness = np.array(statistics.get_fitness_stdev())

        self.ax.clear()
        
        self.ax.set_title("Population's average and best fitness")
        self.ax.set_xlabel("Generations")
        self.ax.set_ylabel("Fitness")
        self.ax.grid()

        self.ax.plot(generation, avg_fitness, 'b-', label="average")
        self.ax.plot(generation, avg_fitness - stdev_fitness, 'g-.', label="-1 sd")
        self.ax.plot(generation, avg_fitness + stdev_fitness, 'g-.', label="+1 sd")
        self.ax.plot(generation, best_fitness, 'r-', label="best")

        self.ax.legend(loc="best")

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
            
        plt.ioff()
    
    def close(self):
        plt.close()