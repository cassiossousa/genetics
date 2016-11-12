import numpy.random as random
import fitness
import copy
from utils import *
from individuals import new_individual
from individuals import Individual

class GeneFlow:
    def __init__(self, ind_type, gene_type, ffit=None, pc=0.9, pm=0.01, mu=100, ngen=200, print_stats=True):
        self.fitness = ffit
        self.population = [new_individual(ind_type, gene_type) for x in range(mu)]
        self.pm = pm
        self.pc = pc
        self.mu = mu
        self.ngen = ngen
        self.print_stats = print_stats

    def calculate_fitness(self):
        for individual in self.population:
            individual.fitness = self.fitness(individual)

    def min_fitness(self):
        return min([x.fitness for x in self.population])

    def max_fitness(self):
        return max([x.fitness for x in self.population])

    def avg_fitness(self):
        return mean([x.fitness for x in self.population])

    def std_fitness(self):
        return std([x.fitness for x in self.population])

    def stats(self):
        if self.print_stats is False:
            return

        print('Min    : %.6f' % self.min_fitness())
        print('Max    : %.6f' % self.max_fitness())
        print('Average: %.6f' % self.avg_fitness())
        print('Std    : %.6f' % self.std_fitness())
        print('Best individual is: ' + str(self.population[0]))

    def generate(self):
        if self.print_stats:
            print('Generation 0:')

        self.stats()

        for i in range(self.ngen):
            if self.print_stats:
                print('\nGeneration %s:' % (i+1))
            self.update()
            self.stats()

    def update(self):
        self.select()
        self.crossover()
        self.mutate()
        self.survive()
        pass

    # The offspring is selected based on the best fitness values - each parent selected generates one child
    def select(self):
        self.population.sort(key=lambda ind:ind.fitness, reverse=True)
        self.elite = copy.deepcopy(self.population[0])
        self.offspring = []

    # Offspring is paired and crossed over with probability pc
    def crossover(self):
        for parent1, parent2 in zip(self.population[::2], self.population[1::2]):
            if random.random() < self.pc:
                child1, child2 = self.cross(parent1, parent2)
                self.offspring.append(child1)
                self.offspring.append(child2)

    # Two-point crossover - two children mix their genes, which are separated in two different points
    def cross(self, ind1, ind2):
        length = len(ind1)
        gene_type = ind1.gene_type

        genes1 = copy.deepcopy(ind1.genes)
        genes2 = copy.deepcopy(ind2.genes)

        # Two distinct points are chosen
        rand1 = random.randint(length + 1)
        rand2 = random.randint(length + 1)

        while (rand1 == rand2) or (rand1 == 0 and rand2 == length) or (rand2 == 0 and rand1 == length):
            rand2 = random.randint(length + 1)

        rand1, rand2 = (rand1, rand2) if rand1 < rand2 else (rand2, rand1)
        genes1[rand1:rand2], genes2[rand1:rand2] = genes2[rand1:rand2], genes1[rand1:rand2]

        return Individual.from_genes(gene_type, genes1), Individual.from_genes(gene_type, genes2)

    # Mutation acts over all genes, with probability pm
    def mutate(self):
        self.population = self.population[1:] + self.offspring
        for ind in self.population:
            for gene in ind.genes:
                if random.random() < self.pm:
                    gene.mutate()

    # Only the best mu individuals survive
    def survive(self):
        self.population.append(self.elite)
        self.calculate_fitness()
        self.population.sort(key=lambda ind:ind.fitness, reverse=True)
        self.population = self.population[:self.mu]


#GeneFlow('OneMaxIndividual', 'BooleanGene', fitness.onemax).generate()
GeneFlow('OneMaxIndividual', 'RealGene', fitness.onemax).generate()
