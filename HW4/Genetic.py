# Artificial Intelligence
# Genetic Algorithms Assignment
# The Knapsack Problem
# Yuchen Yang and Isabella Forman
# November 22, 2019

from random import random
from random import randint
from copy import deepcopy

# Use mutation to generate a new population.
def mutation(chro):
    chro = deepcopy(chro)
    i = randint(0, len(chro)-1)
    chro[i] = 1 - chro[i]
    return chro

# Use crossover to generate a new population.
def crossover(chroA, chroB):
    i = randint(0, len(chroA))
    chro = chroA[0][:i] + chroB[0][i:]
    return chro

# Main Solution of Genetic Algorithm.
class Genetic:

    # Weight is the weight of every box.
    # Value is the value of every box.
    # Limit is the maximum weight that the bag can carry.
    # Population list contains the possible solution (chromosome) for every generation.
    # Possibility_list contains the possibility of every chromosome being chosen to go through crossover.
    # Genlimit is the number of generation.
    # Size is the number of population.
    # Mutation is the possibility of one chromosome go through mutation.
    # Best holds the best case for every generation.
    # Bestvalue holds the highest value for the best possible solution.
    Weight = [20, 30, 60, 90, 50, 70, 30]
    Value = [6, 5, 8, 7, 6, 9, 4]
    Limit = 120
    Population = []
    possibility_list = []
    Genlimit = None
    Size = None
    Mutation = None
    Best = None
    Bestvalue = None

    def __init__(self, Genlimit, Size, Mutation):
        self.Genlimit = Genlimit
        self.Size = Size
        self.Mutation = Mutation
    
    # When we start, we need to generate a group of possible solution (chromosome).
    def random_start(self):
        for i in range(self.Size):
            init = []
            for j in range(7):
                r = random()
                init.append(round(r))
            self.Population.append([init, self.calculate_fitness(init)])
        return True
    
    # We apply a fitness function to calculate the finess value for evey individuals.
    # The fitness function is the total value of boxes contained in the bag, it will be 0 if exceed maximum weight.
    def calculate_fitness(self, chro):
        weight_sum = 0
        value_sum = 0
        for i in range(len(chro)):
            if chro[i] == 1:
                weight_sum += self.Weight[i]
                value_sum += self.Value[i]
        if weight_sum > self.Limit:
            return 0
        else:
            return value_sum
    
    # We recognize the fittest individuals and cull half of the chromosomes that does not have a high fitness value.
    def find_n_fittest(self):
        for i in range(len(self.Population)):
            for j in range(i, len(self.Population)):
                if self.Population[i][1] < self.Population[j][1]:
                    temp = self.Population[i]
                    self.Population[i] = self.Population[j]
                    self.Population[j] = temp
        self.Population = self.Population[:round(self.Size / 2)]

    # We calculate the possibility of every individuals being chosed based on their fitness value.
    def generate_possiblity_list(self):
        self.possibility_list = []
        fsum = 0

        for i in self.Population:
            fsum += i[1]

        afsum = 0
        for i in self.Population:
            if fsum == 0:
                afsum = 0
            else:
                afsum += float(i[1] / fsum)

            self.possibility_list.append(afsum)
    
    # We use both crossover and mutation to generate a new generation.
    def generate_next_generation(self):

        crossover_result = []

        for i in range(self.Size-1):
            r = random()
            for p in range(len(self.possibility_list)):
                if r < self.possibility_list[p]:
                    p1 = p
                    break

            r = random()
            for p in range(len(self.possibility_list)):
                if r < self.possibility_list[p]:
                    p2 = p
                    break

            crossover_result.append(crossover(self.Population[p1], self.Population[p2]))

        self.Population = []
        for i in crossover_result:
            r = random()
            if r < self.Mutation:
                newchro=mutation(i)
                self.Population.append([newchro, self.calculate_fitness(newchro)])
        self.Population.append(self.Best)
        return True
    
    # We pick the best individuals in the population and record the chromosome and its fitness value.
    def choose_best_individual(self):
        maxi = []
        maxvalue = 0
        for i in self.Population:
            if maxvalue < i[1]:
                maxvalue = i[1]
                maxi = i

        self.Best = maxi
        self.Bestvalue = maxvalue
        return True

    # Print the solution.
    def print_solution(self):
        string1="We are choosing"
        string2="The weight is "
        string3="The value is "
        weight=0
        for i in range(7):
            if self.Best[0][i] == 1:
                string1 += " Box" + str(i+1)
                string2 += str(self.Weight[i]) + "+"
                string3 += str(self.Value[i]) + "+"
                weight+=self.Weight[i]
                
        string2 = string2[:-1]
        string3 = string3[:-1]

        string1 += " for this problem."

        string2 += "=" + str(weight)
        string3 += "=" + str(self.Bestvalue)
        
        print(string1)
        print(string2)
        print(string3)

    # Go through the genetic algorithm.
    def run(self):
        self.random_start()
        self.choose_best_individual()
        for i in range(self.Genlimit):
            self.find_n_fittest()
            self.generate_possiblity_list()
            self.generate_next_generation()
            self.choose_best_individual()
            #print(self.Best)
        
        self.find_n_fittest()
        #print(self.Best)

        self.print_solution()


if __name__ == "__main__":
    g = Genetic(200, 100, 0.5)
    g.run()