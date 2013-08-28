#!/usr/bin/env python

###############################################################################
#                                                                             #
#                             S C H E D U L E R                               #
#                                                                             #
###############################################################################

__author__ =  'Bjorn Barrefors'

import numpy
import math
import heapq
from random import randint
from operator import itemgetter

cluster = ({'t_amb' : -8.3, 'r': 0.6458, 'a1': 0.0061, 'a2': 4.5036, 'a3': 0.0928, 'a4': -0.3536, 'a5': -4.660637, 'a6': 64.8758, 'util': 4}, 
           {'t_amb' : -9.0, 'r': 0.6532, 'a1': 0.0248, 'a2': 8.1349, 'a3': -0.2863, 'a4': -1.3203, 'a5': 2.6106, 'a6': 75.4638, 'util': 4}, 
           {'t_amb' : -10.0, 'r': 0.7321, 'a1': -0.0040, 'a2': 5.5272, 'a3': 0.2977, 'a4': 0.0713, 'a5': -13.2765, 'a6': 56.4242, 'util': 4}, 
           {'t_amb' : -6.9, 'r': 0.6154, 'a1': 0.0338, 'a2': 7.4625, 'a3': -0.4637, 'a4': -1.7374, 'a5': 10.1535, 'a6': 78.6566, 'util': 4}, 
           {'t_amb' : -8.6, 'r': 0.6562, 'a1': 0.0335, 'a2': 13.8525, 'a3': -0.6544, 'a4': -1.4578, 'a5': 1.1880, 'a6': 75.7025, 'util': 4},
           {'t_amb' : -8.6, 'r': 0.6591, 'a1': 0.0550, 'a2': 18.9665, 'a3': -1.4357, 'a4': -1.7860, 'a5': 15.1805, 'a6': 68.1403, 'util': 4}, 
           {'t_amb' : -6.6, 'r': 0.6210, 'a1': 0.0075, 'a2': 8.9752, 'a3': 0.0611, 'a4': -0.4664, 'a5': -12.0162, 'a6': 64.0839, 'util': 4}, 
           {'t_amb' : -7.5, 'r': 0.6250, 'a1': 0.0133, 'a2': 8.0939, 'a3': -0.2100, 'a4': -0.2619, 'a5': -4.4860, 'a6': 56.6180, 'util': 4})

kFreq = (1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000)

task_set = []
pop = []
kHyper_period = 1000
kTot_util = 0
kMax_gen = 1000
kMax_converge = 10
kMax_temp = 45
large_integer = 1000
population_size = 0
max_elite = 0
crossover_size = 0
mutation_size = 0
number_tasks = 0

def buildTaskSet(num_tasks, tot_util):
    # Generate a random task set based on the tot util and num tasks
    # task_set is a list of floats where each float is the utilization for a task
    # [ task_util, task_util, ... ]
    # CHECKED : WORKS
    global task_set
    global kTot_util
    kTot_util = tot_util
    task_set = []
    mean = float(kTot_util)/float(num_tasks)
    std_dev = mean/2.75
    util = abs(numpy.random.normal(mean, std_dev, num_tasks))
    for i in util:
        task_set.append(i)
    return 1

def buildPop(num_tasks, pop_size):
    # Randomly generate a population/allocation strategy
    # pop is a list of chromosomes which is turn is a list of genes, 
    # though first value in each chromosome is a float representing the fitness value of the chromosome,
    # each gene represents the allocation of a task and contains task utilization, cpu number, and frequency of cpu.
    # [ [ fitness_value, [ task_util, cpu_num, freq ], [ task_util, cpu_num, freq ], ... ], ...]
    # CHECKED : WORKS
    global pop
    pop = []
    for i in range(pop_size):
        chromo = [0]
        for j in range(num_tasks):
            gene = [task_set[j], randint(0,7)]
            chromo.append(gene)
        pop.append(chromo)
    return 1

def maxTemp(core, freq):
    # Based on cpu properties and frequency, return the maximum possible temperature for core
    f = freq
    a1 = cluster[core]['a1']
    a2 = cluster[core]['a2']
    a3 = cluster[core]['a3']
    a4 = cluster[core]['a4']
    a5 = cluster[core]['a5']
    a6 = cluster[core]['a6']
    r = cluster[core]['r']
    t_amb = cluster[core]['t_amb']
    A = a1*r
    B = a3*r*f + a4*r - 1
    C = a2*r*math.pow(f,2) + a5*f*r + a6*r + t_amb
    max_temp = -B/(2*A) - math.sqrt(math.pow(B,2) - 4*A*C)/(2*A)
    return max_temp

def power(core, freq):
    # Based on cpu properties and a frequency, return the power consumption at maximum temperature
    # PENDING : Waiting for maxTemp function to work
    f = freq
    a1 = cluster[core]['a1']
    a2 = cluster[core]['a2']
    a3 = cluster[core]['a3']
    a4 = cluster[core]['a4']
    a5 = cluster[core]['a5']
    a6 = cluster[core]['a6']
    r = cluster[core]['r']
    t_amb = cluster[core]['t_amb']
    t = maxTemp(core, freq)
    power1 = a1*math.pow(t,2) + a2*math.pow(f,2) + a3*f*t + a4*t + a5*f + a6
    return power1

def eMax(chromo):
    # power consumption added up assuming all cpu's ran on highest frequency
    # PENDING : Waiting for maxTemp
    e_max = 0
    for cpu in range(8):
        power2 = power(cpu, kFreq[9])
        e_max += power2
    return e_max
 
def eChromo(chromo):
    # Actual power consumption for task allocation. 
    # If allocation doesn't comply w temperature restrictions it gets penalised
    # PENDING : Waiting for maxTemp
    global pop
    e_chromo = 0
    tot_util = [0, 0, 0, 0, 0, 0, 0, 0]
    for gene_i in range(len(pop[chromo][1:])):
        gene_i += 1
        gene = pop[chromo][gene_i]
        util = gene[0]
        core = gene[1]
        tot_util[core] += util
    j = 0
    f = 0
    for cpu in range(8):
        while (j <= 9):
            f = kFreq[j]/kFreq[9]
            if (tot_util[cpu]/f <= 4):
                if (tot_util[cpu] == 0):
                    j = 12
                elif (kMax_temp >= maxTemp(cpu, f*kFreq[9])):
                    j = 11
                else:
                    j = 10
            else:
                j += 1
        if (j == 10):
            e_chromo += kFreq[9]*large_integer
        elif (j == 11):
            e_chromo += power(core, f*kFreq[9])
        else:
            e_chromo += 0
    return e_chromo

def fitnessValue(chromo):
    # e_max - e_chromo, the higher value the better
    # PENDING : Waiting for maxTemp and power formula to work
    e_max = eMax(chromo)
    e_chromo = eChromo(chromo)
    fitness_value = e_max - e_chromo
    return (-fitness_value)

def minWF():
    # Select the core with least available util left that can satisfy the conditions
    # to schedule tasks on.
    # Create one chromosome based on that scheduling philosophy
    fs = open('Schedule', 'a')
    fs.write("MW Algorithm\n")
    fs.close()
    global pop
    pop = []
    chromo = [0]
    util = []
    i = 0
    for cpu in cluster:
        heapq.heappush(util, (0, i))
        i += 1
    for task_util in task_set:
        while util:
            cpu = heapq.heappop(util)
            cpu_num = cpu[1]
            j = 0
            f = 0
            while (j <= 9):
                f = kFreq[j]/kFreq[9]
                if (cpu[0]/f <= 4):
                    if (kMax_temp >= maxTemp(cpu_num, f*kFreq[9])):
                        chromo.append([task_util, cpu_num])
                        j = 11
                    else:
                        j = 10
                else:
                    j += 1
            if (j == 11):
                cpu = (cpu[0]+task_util, cpu[1])
                heapq.heappush(util, cpu)
                break
        if not util:
            print "failed"
            return 1
    pop.append(chromo)
    total_energy = eChromo(0)
    total_cores = 0
    s = set()
    for gene_i in range(len(pop[0][1:])):
        gene_i += 1
        gene = pop[0][gene_i]
        cpu = gene[1]
        s.add(cpu)
    total_cores = len(s)
    fs = open('Schedule', 'a')
    fs.write("The total energy consumption for this schedule is " + str(total_energy) + "\n")
    fs.write("the number of CPU's used is " + str(total_cores) + "\n")
    fs.write("Allocation stategy\n")
    for gene_i in range(len(pop[0][1:])):
        gene_i += 1
        gene = pop[0][gene_i]
        cpu = gene[1]
        util = gene[0]
        fs.write("Allocate " + str(util) + " on cpu " + str(cpu) + "\n")
    fs.write("\n")
    fs.close()
    return 0

def genetic():
    fs = open('Schedule', 'a')
    fs.write("Genetic Algorithm\n")
    fs.close()
    global pop
    generation = 1
    converge = 1
    best_fit = 0
    while ((generation < kMax_gen) and (converge < kMax_converge)):
        print "Generation " + str(generation)
        for chromo in range(len(pop)):
            fitness_value = fitnessValue(chromo)
            pop[chromo][0] = fitness_value
        pop = sorted(pop, key=itemgetter(0))
        generation += 1
        if (pop[0][0] == best_fit):
            converge += 1
        else:
            besf_fit = pop[0][0]
            converge = 1
            
        # Crossover
        for i in range(max_elite, max_elite + crossover_size):
            rand = randint(0,population_size-1)
            chromo_1 = pop[i]
            chromo_2 = pop[rand]
            point_1 = randint(0, number_tasks-1)
            point_2 = randint(0, number_tasks-1)
            if (point_1 > point_2):
                tmp = point_1
                point_1 = point_2
                point_2 = tmp
            for j in range(point_1, point_2):
                tmp = chromo_1[j]
                chromo_1[j] = chromo_2[j]
                chromo_2[j] = tmp
            pop[i] = chromo_1
            pop[rand] = chromo_2

        # Mutate
        for i in range(mutation_size):
            rand = randint(max_elite, population_size-1)
            chromo = pop[rand]
            point_1 = randint(0, number_tasks-1)
            point_2 = randint(0, number_tasks-1)
            if (point_1 > point_2):
                tmp = point_1
                point_1 = point_2
                point_2 = tmp
            for j in range(point_1, point_2):
                chromo[j] = [task_set[j], randint(0,7)]
            pop[rand] = chromo
    for chromo in range(len(pop)):
        fitness_value = fitnessValue(chromo)
        pop[chromo][0] = fitness_value
    pop = sorted(pop, key=itemgetter(0))
    total_energy = eChromo(0)
    total_cores = 0
    s = set()
    for gene_i in range(len(pop[0][1:])):
        gene_i += 1
        gene = pop[0][gene_i]
        cpu = gene[1]
        s.add(cpu)
    total_cores = len(s)
    fs = open('Schedule', 'a')
    fs.write("The total energy consumption for this schedule is " + str(total_energy) + "\n")
    fs.write("the number of CPU's used is " + str(total_cores) + "\n")
    fs.write("Allocation stategy\n")
    for gene_i in range(len(pop[0][1:])):
        gene_i += 1
        gene = pop[0][gene_i]
        cpu = gene[1]
        util = gene[0]
        fs.write("Allocate " + str(util) + " on cpu " + str(cpu) +"\n")
    fs.write("\n")
    fs.close()
    return 1

def hybridGAWF():
    fs = open('Schedule', 'a')
    fs.write("HybridWGA algorithm\n")
    fs.close()
    global pop
    wf_chromo = pop[0]
    buildPop(number_tasks, population_size)
    pop[0] = wf_chromo
    genetic()
    return 1

def algorithms(num_tasks, tot_util, pop_size):
    global population_size
    global max_elite
    global number_tasks
    global crossover_size
    global mutation_size
    population_size = pop_size
    number_tasks = num_tasks
    max_elite = int(population_size*0.01)
    crossover_size = int(population_size*0.85)
    mutation_size = int(population_size*0.005)
    # PENDING : Waiting for genetic algorithm
    # PENDIng : Waiting for Worst Fit algorithm
    # Create a random task set
    buildTaskSet(number_tasks, tot_util)
    # Create random population for genetic alg
    buildPop(number_tasks, population_size)
    # Call algorithms
    # Run genetic w random population, print results
    genetic()
    if minWF() == 1:
        return 0
    hybridGAWF()
    # Run MinWF, print results
    # Feed MinWF into Genetic, print results
    return 1

##### This is the start of the program #####

#num_tasks = [100, 150, 200, 300];
#tot_util = [20, 35, 45];
#pop_size = [2000, 10000];

num_tasks = [100];
tot_util = [20];
pop_size = [2000];

for tmp_num in num_tasks:
    print "Next task set"
    for tmp_util in tot_util:
        print "Next total utilization"
        for tmp_pop in pop_size:
            print "Next population size"
            fs = open('Schedule', 'a')
            fs.write("Task set: Num Tasks " + str(tmp_num) + " | Util " + str(tmp_util) + " | Pop Size " + str(tmp_pop) + "\n\n")
            fs.close()
            algorithms(tmp_num, tmp_util, tmp_pop)
print "Done"
