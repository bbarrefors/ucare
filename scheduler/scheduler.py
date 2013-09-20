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

cluster = ({'t_amb' : -8.3, 'r': 0.646, 'a1': 0.0061, 'a2': 4.5036, 'a3': 0.0928, 'a4': -0.3536, 'a5': -4.660637, 'a6': 64.8758, 'util': 4}, 
           {'t_amb' : -9.0, 'r': 0.653, 'a1': 0.0248, 'a2': 8.1349, 'a3': -0.2863, 'a4': -1.3203, 'a5': 2.6106, 'a6': 75.4638, 'util': 4}, 
           {'t_amb' : -10.0, 'r': 0.731, 'a1': -0.0040, 'a2': 5.5272, 'a3': 0.2977, 'a4': 0.0713, 'a5': -13.2765, 'a6': 56.4242, 'util': 4}, 
           {'t_amb' : -6.9, 'r': 0.615, 'a1': 0.0338, 'a2': 7.4625, 'a3': -0.4637, 'a4': -1.7374, 'a5': 10.1535, 'a6': 78.6566, 'util': 4}, 
           {'t_amb' : -8.6, 'r': 0.656, 'a1': 0.0335, 'a2': 13.8525, 'a3': -0.6544, 'a4': -1.4578, 'a5': 1.1880, 'a6': 75.7025, 'util': 4},
           {'t_amb' : -8.6, 'r': 0.659, 'a1': 0.0550, 'a2': 18.9665, 'a3': -1.4357, 'a4': -1.7860, 'a5': 15.1805, 'a6': 68.1403, 'util': 4}, 
           {'t_amb' : -6.6, 'r': 0.621, 'a1': 0.0075, 'a2': 8.9752, 'a3': 0.0611, 'a4': -0.4664, 'a5': -12.0162, 'a6': 64.0839, 'util': 4}, 
           {'t_amb' : -7.5, 'r': 0.625, 'a1': 0.0133, 'a2': 8.0939, 'a3': -0.2100, 'a4': -0.2619, 'a5': -4.4860, 'a6': 56.6180, 'util': 4},
           {'t_amb' : -4.2, 'r': 0.602, 'a1': 0.0115, 'a2': 8.4222, 'a3': -0.1817, 'a4': -0.2186, 'a5': -5.9063, 'a6': 56.8729, 'util': 4},
           {'t_amb' : -6.0, 'r': 0.630, 'a1': 0.0100, 'a2': 9.7111, 'a3': -0.2385, 'a4': 0.0409, 'a5': -9.6745, 'a6': 55.7293, 'util': 4}, 
           {'t_amb' : -8.6, 'r': 0.696, 'a1': -0.0089, 'a2': 6.9449, 'a3': 0.2484, 'a4': 0.5398, 'a5': -17.5449, 'a6': 53.9967, 'util': 4}, 
           {'t_amb' : -10.5, 'r': 0.721, 'a1': -0.1410, 'a2': -28.4890, 'a3': 4.5790, 'a4': 2.3820, 'a5': -47.7470, 'a6': 46.7540, 'util': 4}, 
           {'t_amb' : -6.6, 'r': 0.683, 'a1': 0.0121, 'a2': 9.1581, 'a3': -0.3218, 'a4': 0.0691, 'a5': -6.5838, 'a6': 52.4583, 'util': 4}, 
           {'t_amb' : -4.1, 'r': 0.620, 'a1': 0.0261, 'a2': 8.0382, 'a3': -0.4493, 'a4': -0.7162, 'a5': 2.1208, 'a6': 59.1880, 'util': 4}, 
           {'t_amb' : -9.1, 'r': 0.673, 'a1': 0.0011, 'a2': 4.7734, 'a3': 0.0952, 'a4': 0.1748, 'a5': -6.1500, 'a6': 52.0493, 'util': 4}, 
           {'t_amb' : -6.5, 'r': 0.670, 'a1': 0.0055, 'a2': 4.3663, 'a3': 0.0723, 'a4': -0.1552, 'a5': -3.9533, 'a6': 55.0371, 'util': 4}, 
           {'t_amb' : -5.5, 'r': 0.675, 'a1': -0.0314, 'a2': 1.6113, 'a3': 1.0633, 'a4': 0.8576, 'a5': -29.7808, 'a6': 56.0095, 'util': 4}, 
           {'t_amb' : -5.5, 'r': 0.644, 'a1': -0.0210, 'a2': 3.9259, 'a3': 0.4893, 'a4': 1.0868, 'a5': -18.1464, 'a6': 45.0253, 'util': 4}, 
           {'t_amb' : -6.4, 'r': 0.676, 'a1': 0.0114, 'a2': 6.3760, 'a3': -0.1265, 'a4': -0.2402, 'a5': -2.7039, 'a6': 52.7532, 'util': 4}, 
           {'t_amb' : -8.8, 'r': 0.704, 'a1': -0.0151, 'a2': 5.6876, 'a3': 0.4642, 'a4': 0.6182, 'a5': -21.2384, 'a6': 54.0389, 'util': 4})

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
    mean = float(tot_util)/float(num_tasks)
    std_dev = mean/2.75
    util = abs(numpy.random.normal(mean, std_dev, num_tasks))
    u = 0
    for i in util:
        u += i
        task_set.append(i)
    fs = open('Schedule', 'a')
    fs.write("Utilization " + str(u) + "\n")
    fs.close()
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
            gene = [task_set[j], randint(0,19)]
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
    for cpu in range(20):
        power2 = power(cpu, kFreq[9])
        e_max += power2
    return e_max
 
def eChromo(chromo):
    # Actual power consumption for task allocation. 
    # If allocation doesn't comply w temperature restrictions it gets penalised
    # PENDING : Waiting for maxTemp
    e_chromo = 0
    tot_util = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for gene_i in range(len(pop[chromo][1:])):
        gene_i += 1
        gene = pop[chromo][gene_i]
        util = gene[0]
        core = gene[1]
        tot_util[core] += util
    for cpu in range(20):
        if not (tot_util[cpu] == 0):
            j = 0
            f = 0
            while (j <= 9):
                f = kFreq[j]/kFreq[9]
                if (tot_util[cpu]/f <= 4):
                    if (kMax_temp < maxTemp(cpu, kFreq[j])):
                        j = 11
                    else:
                        break
                else:
                    j += 1
            if (j < 10):
                e_chromo += power(cpu, kFreq[j])
            else:
                e_chromo += kFreq[9]*large_integer
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
            return 1
    pop.append(chromo)
    total_cores = 0
    s = set()
    for gene_i in range(len(pop[0][1:])):
        gene_i += 1
        gene = pop[0][gene_i]
        cpu = gene[1]
        s.add(cpu)
    total_cores = len(s)
    fs = open('Schedule', 'a')
    fs.write("The number of CPU's used is " + str(total_cores) + "\n")
    fs.write("Allocation stategy\n")
    tot_util = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for gene_i in range(len(pop[0][1:])):
        gene_i += 1
        gene = pop[0][gene_i]
        cpu = gene[1]
        util = gene[0]
        tot_util[cpu] += util
    i = 1
    for cpu in tot_util:
        j = 0
        while (j <= 9):
            f = kFreq[j]/kFreq[9]
            if (cpu/f <= 4):
                break
            if j == 9:
                break
            j += 1
        fs.write("Allocate total " + str(cpu/(kFreq[j]/kFreq[9])) + " on cpu " + str(i) + " on freq " + str(kFreq[j]) + "\n")
        i += 1
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
                chromo[j] = [task_set[j], randint(0,19)]
            pop[rand] = chromo
    for chromo in range(len(pop)):
        fitness_value = fitnessValue(chromo)
        pop[chromo][0] = fitness_value
    pop = sorted(pop, key=itemgetter(0))
    total_cores = 0
    s = set()
    for gene_i in range(len(pop[0][1:])):
        gene_i += 1
        gene = pop[0][gene_i]
        cpu = gene[1]
        s.add(cpu)
    total_cores = len(s)
    fs = open('Schedule', 'a')
    fs.write("The number of CPU's used is " + str(total_cores) + "\n")
    fs.write("Allocation stategy\n")
    tot_util = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for gene_i in range(len(pop[0][1:])):
        gene_i += 1
        gene = pop[0][gene_i]
        cpu = gene[1]
        util = gene[0]
        tot_util[cpu] += util
    i = 1
    for cpu in tot_util:
        j = 0
        while (j <= 9):
            f = kFreq[j]/kFreq[9]
            if (cpu/f <= 4):
                break
            if j == 9:
                break
            j += 1
        fs.write("Allocate total " + str(cpu/(kFreq[j]/kFreq[9])) + " on cpu " + str(i) + " on freq " + str(kFreq[j]) + "\n")
        i += 1
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
    # Create a random task set
    buildTaskSet(number_tasks, tot_util)
    # Create random population for genetic alg
    buildPop(number_tasks, population_size)
    # Call algorithms
    # Run genetic w random population, print results
    genetic()
    # Run MinWF, print results
    # Feed MinWF into Genetic, print results
    if minWF() == 1:
        return 0
    hybridGAWF()
    return 1

##### This is the start of the program #####

num_tasks = [100, 150, 200, 300];
tot_util = [20, 35, 45];
pop_size = [2000, 10000];

#num_tasks = [100];
#tot_util = [30];
#pop_size = [2000];

fs = open('Schedule', 'w')
fs.write("Start scheduler\n\n")
fs.close()

for tmp_num in num_tasks:
    for tmp_util in tot_util:
        for tmp_pop in pop_size:
            fs = open('Schedule', 'a')
            fs.write("Task set: Num Tasks " + str(tmp_num) + " | Util " + str(tmp_util) + " | Pop Size " + str(tmp_pop) + "\n\n")
            fs.close()
            algorithms(tmp_num, tmp_util, tmp_pop)
