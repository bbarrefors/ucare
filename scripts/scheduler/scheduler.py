#!/usr/bin/env python

###############################################################################
#                                                                             #
#                             S C H E D U L E R                               #
#                                                                             #
###############################################################################

__author__ =  'Bjorn Barrefors'

import sys
import numpy
import math
import heapq
import copy
import timeit
from random import randint
from operator import itemgetter
from itertools import combinations

cluster = ({'t_amb' : -8.3, 'r': 0.646, 'a1': 0.0061, 'a2': 4.5036, 'a3': 0.0928, 'a4': -0.3536, 'a5': -4.660637, 'a6': 64.8758, 'util': 4, 'u1' : 247.01, 'u2' : 75.46, 'u0' : 429.51},
           {'t_amb' : -9.0, 'r': 0.653, 'a1': 0.0248, 'a2': 8.1349, 'a3': -0.2863, 'a4': -1.3203, 'a5': 2.6106, 'a6': 75.4638, 'util': 4, 'u1' : 304.91, 'u2' : 123.8, 'u0' : 422.0},
           {'t_amb' : -10.0, 'r': 0.731, 'a1': -0.0040, 'a2': 5.5272, 'a3': 0.2977, 'a4': 0.0713, 'a5': -13.2765, 'a6': 56.4242, 'util': 4, 'u1' : 276.60, 'u2' : 114.0, 'u0' : 402.9},
           {'t_amb' : -6.9, 'r': 0.615, 'a1': 0.0338, 'a2': 7.4625, 'a3': -0.4637, 'a4': -1.7374, 'a5': 10.1535, 'a6': 78.6566, 'util': 4, 'u1' : 247.06, 'u2' : 81.28, 'u0' : 431.55},
           {'t_amb' : -8.6, 'r': 0.656, 'a1': 0.0335, 'a2': 13.8525, 'a3': -0.6544, 'a4': -1.4578, 'a5': 1.1880, 'a6': 75.7025, 'util': 4, 'u1' : 202.57, 'u2' : 66.14, 'u0' : 432.98},
           {'t_amb' : -8.6, 'r': 0.659, 'a1': 0.0550, 'a2': 18.9665, 'a3': -1.4357, 'a4': -1.7860, 'a5': 15.1805, 'a6': 68.1403, 'util': 4, 'u1' : 256.70, 'u2' : 106.2, 'u0' : 414.40},
           {'t_amb' : -6.6, 'r': 0.621, 'a1': 0.0075, 'a2': 8.9752, 'a3': 0.0611, 'a4': -0.4664, 'a5': -12.0162, 'a6': 64.0839, 'util': 4, 'u1' : 301.30, 'u2' : 138.0, 'u0' : 403.70},
           {'t_amb' : -7.5, 'r': 0.625, 'a1': 0.0133, 'a2': 8.0939, 'a3': -0.2100, 'a4': -0.2619, 'a5': -4.4860, 'a6': 56.6180, 'util': 4, 'u1' : 228.53, 'u2' : 78.39, 'u0' : 429.78},
           {'t_amb' : -4.2, 'r': 0.602, 'a1': 0.0115, 'a2': 8.4222, 'a3': -0.1817, 'a4': -0.2186, 'a5': -5.9063, 'a6': 56.8729, 'util': 4, 'u1' : 268.20, 'u2' : 114.8, 'u0' : 423.9},
           {'t_amb' : -6.0, 'r': 0.630, 'a1': 0.0100, 'a2': 9.7111, 'a3': -0.2385, 'a4': 0.0409, 'a5': -9.6745, 'a6': 55.7293, 'util': 4, 'u1' : 218.06, 'u2' : 71.53, 'u0' : 431.00},
           {'t_amb' : -8.6, 'r': 0.696, 'a1': -0.0089, 'a2': 6.9449, 'a3': 0.2484, 'a4': 0.5398, 'a5': -17.5449, 'a6': 53.9967, 'util': 4, 'u1' : 297.50, 'u2' : 129.6, 'u0' : 417.6},
           {'t_amb' : -10.5, 'r': 0.721, 'a1': -0.1410, 'a2': -28.4890, 'a3': 4.5790, 'a4': 2.3820, 'a5': -47.7470, 'a6': 46.7540, 'util': 4, 'u1' : 261.03, 'u2' : 96.15, 'u0' : 411.75},
           {'t_amb' : -6.6, 'r': 0.683, 'a1': 0.0121, 'a2': 9.1581, 'a3': -0.3218, 'a4': 0.0691, 'a5': -6.5838, 'a6': 52.4583, 'util': 4, 'u1' : 238.30, 'u2' : 85.90, 'u0' : 424.2},
           {'t_amb' : -4.1, 'r': 0.620, 'a1': 0.0261, 'a2': 8.0382, 'a3': -0.4493, 'a4': -0.7162, 'a5': 2.1208, 'a6': 59.1880, 'util': 4, 'u1' : 330.90, 'u2' : 152.6, 'u0' : 396.1},
           {'t_amb' : -9.1, 'r': 0.673, 'a1': 0.0011, 'a2': 4.7734, 'a3': 0.0952, 'a4': 0.1748, 'a5': -6.1500, 'a6': 52.0493, 'util': 4, 'u1' : 229.23, 'u2' : 56.24, 'u0' : 433.38},
           {'t_amb' : -6.5, 'r': 0.670, 'a1': 0.0055, 'a2': 4.3663, 'a3': 0.0723, 'a4': -0.1552, 'a5': -3.9533, 'a6': 55.0371, 'util': 4, 'u1' : 260.11, 'u2' : 83.78, 'u0' : 419.28},
           {'t_amb' : -5.5, 'r': 0.675, 'a1': -0.0314, 'a2': 1.6113, 'a3': 1.0633, 'a4': 0.8576, 'a5': -29.7808, 'a6': 56.0095, 'util': 4, 'u1' : 405.20, 'u2' : 108.7, 'u0' : 405.2},
           {'t_amb' : -5.5, 'r': 0.644, 'a1': -0.0210, 'a2': 3.9259, 'a3': 0.4893, 'a4': 1.0868, 'a5': -18.1464, 'a6': 45.0253, 'util': 4, 'u1' : 291.90, 'u2' : 125.1, 'u0' : 411.4},
           {'t_amb' : -6.4, 'r': 0.676, 'a1': 0.0114, 'a2': 6.3760, 'a3': -0.1265, 'a4': -0.2402, 'a5': -2.7039, 'a6': 52.7532, 'util': 4, 'u1' : 200.27, 'u2' : 58.36, 'u0' : 418.78},
           {'t_amb' : -8.8, 'r': 0.704, 'a1': -0.0151, 'a2': 5.6876, 'a3': 0.4642, 'a4': 0.6182, 'a5': -21.2384, 'a6': 54.0389, 'util': 4, 'u1' : 238.74, 'u2' : 87.32, 'u0' : 414.86})

kFreq = (1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000)

task_set = []
pop = []
kHyper_period = 1000
kTot_util = 0
kMax_gen = 10000
kMax_converge = 20
kMax_temp = 45
large_integer = 10000
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
            gene = randint(0,19)
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

def power(core, freq, util):
    # Based on cpu properties and a frequency, return the power consumption at maximum temperature
    f = freq
    if f == 1.197000:
        u1 = cluster[core]['u1']
        u2 = cluster[core]['u2']
        u0 = cluster[core]['u0']
        power1 = 0.1*(u1*util - u2*math.pow(util,2) + u0)
        return power1
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

def eMax():
    # power consumption added up assuming all cpu's ran on highest frequency
    e_max = 0
    for cpu in range(20):
        power2 = power(cpu, kFreq[9], 0)
        e_max += power2
    return e_max

def eChromo(chromo):
    # Actual power consumption for task allocation.
    # If allocation doesn't comply w temperature restrictions it gets penalized
    global pop
    e_chromo = 0
    tot_util = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for gene in range(number_tasks):
        cpu = pop[chromo][gene+1]
        tot_util[cpu] += task_set[gene]
    cpu = 0
    for util in tot_util:
        if not (util == 0):
            j = 0
            f = 0
            while (j <= 9):
                f = kFreq[j]/kFreq[9]
                if (util/f <= 4):
                    if (kMax_temp < maxTemp(cpu, kFreq[j])):
                        j = 11
                    else:
                        break
                else:
                    j += 1
            if (j < 10):
                e_chromo += power(cpu, kFreq[j], util)
            else:
                e_chromo += kFreq[9]*large_integer
        cpu += 1
    return e_chromo

def fitnessValue(chromo):
    # e_max - e_chromo, the higher value the better
    e_max = eMax()
    e_chromo = eChromo(chromo)
    #print e_max
    #print e_chromo
    fitness_value = e_max - e_chromo
    return (-fitness_value)

def findMin():
    # Here we will find the theoretical minimum number of cores
    # needed to schedule all tasks
    totUtil = kTotUtil
    global cluster
    cores = 0
    for machine in cluster:
        cores += 1
        totUtil -= machine['util']
        if totUtil <= 0:
            break
    else:
        # Not enough cores to schedule all tasks
        return 0
    return cores

def minWFPrime(numCores):
     global pop
     chromo = [0]
     util = []
     for i in range(numCores):
         heapq.heappush(util, (0, i))
     for task_util in task_set:
         while util:
             cpu = heapq.heappop(util)
             cpu_num = cpu[1]
             cpu_util = cpu[0] + task_util
             j = 0
             f = 0
             while (j <= 9):
                 f = kFreq[j]/kFreq[9]
                 if (cpu_util/f <= 4):
                     if (kMax_temp >= maxTemp(cpu_num, f*kFreq[9])):
                         chromo.append(cpu_num)
                         heapq.heappush(util,(cpu_util, cpu_num))
                         j = 11
                     else:
                         j = 10
                 else:
                     j += 1
             if j == 11:
                 break
         if not util:
             return False
     pop = []
     pop.append(chromo)
     pop[0][0] =  fitnessValue(0)
     return True

def minWF():
     # Select the core with least available util left that can satisfy the conditions
     # to schedule tasks on.
     # Create one chromosome based on that scheduling philosophy
     fs = open('Schedule', 'a')
     fs.write("MW Algorithm\n")
     fs.close()
     i = 20
     while i > 0:
         if not (minWFPrime(i)):
             break
         i -= 1
     total_cores = 0
     s = set()
     for gene_i in range(len(pop[0][1:])):
         cpu = pop[0][gene_i+1]
         s.add(cpu)
     total_cores = len(s)

     fs = open('Schedule', 'a')
     fs.write("The number of CPU's used is " + str(total_cores) + "\n")
     fs.write("Allocation stategy\n")
     tot_util = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     for gene in range(number_tasks):
         util = task_set[gene]
         cpu = pop[0][gene+1]
         tot_util[cpu] += util
     i = 1
     for util in tot_util:
         fs.write("%s\t%s\n" % (str(i), str(util)))
         i += 1
     fs.write("\n")
     fs.close()
     return 0

def genetic():
    fs = open('Schedule', 'a')
    fs.write("Genetic Algorithm\n")
    fs.close()
    global pop
    generation = 0
    converge = 0
    best_fit = 0
    elite_pop = []
    for chromo in range(len(pop)):
        fitness_value = fitnessValue(chromo)
        pop[chromo][0] = fitness_value
    pop = sorted(pop, key=itemgetter(0))
    while ((generation < kMax_gen) and (converge < kMax_converge)):
        generation += 1
        if (int(pop[0][0]) == best_fit):
            converge += 1
        else:
            besf_fit = pop[0][0]
            converge = 1
        elite_pop = copy.deepcopy(pop[:max_elite])
        # Crossover
        for i in range(crossover_size):
            rand = randint(0,population_size-1)
            chromo_1 = pop[i]
            chromo_2 = pop[rand]
            point_1 = randint(1, number_tasks-1)
            point_2 = randint(1, number_tasks-1)
            if (point_1 > point_2):
                tmp = point_1
                point_1 = point_2
                point_2 = tmp
            for j in range(point_1, point_2):
                tmp = chromo_1[j]
                chromo_1[j] = chromo_2[j]
                chromo_2[j] = tmp
            pop[i] = copy.deepcopy(chromo_1)
            pop[rand] = copy.deepcopy(chromo_2)

        # Mutate
        for i in range(mutation_size):
            rand = randint(0, population_size-1)
            chromo = pop[rand]
            point_1 = randint(1, number_tasks-1)
            point_2 = randint(1, number_tasks-1)
            if (point_1 > point_2):
                tmp = point_1
                point_1 = point_2
                point_2 = tmp
            for j in range(point_1, point_2):
                chromo[j] = randint(0,19)

        # Copy back elite population
        for chromo in range(len(pop)):
            pop[chromo][0] = -fitnessValue(chromo)
        pop = sorted(pop, key=itemgetter(0))

        for chromo in range(len(pop)):
            pop[chromo][0] = -pop[chromo][0]
        i = 0
        pop[:max_elite] = elite_pop[:]
        pop = sorted(pop, key=itemgetter(0))
    total_cores = 0
    s = set()
    for gene_i in range(len(pop[0][1:])):
        cpu = pop[0][gene_i+1]
        s.add(cpu)
    total_cores = len(s)
    fs = open('Schedule', 'a')
    fs.write("The number of CPU's used is " + str(total_cores) + "\n")
    fs.write("Allocation stategy\n")
    tot_util = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for gene in range(number_tasks):
        util = task_set[gene]
        cpu = pop[0][gene+1]
        tot_util[cpu] += util
    i = 1
    for util in tot_util:
        fs.write("%s\t%s\n" % (str(i), str(util)))
        i += 1
    fs.write("\n")
    fs.close()
    return 1

def buildChromo(cores):
    # @TODO : Build an evenly distributed chromosome on cores in cores
    # Use max-core worst fit
    chromo = [0]
    util = []
    for i in cores:
        heapq.heappush(util, (0, i))
    for task_util in task_set:
        while util:
            cpu = heapq.heappop(util)
            cpu_num = cpu[1]
            cpu_util = cpu[0] + task_util
            j = 0
            f = 0
            while (j <= 9):
                f = kFreq[j]/kFreq[9]
                if (cpu_util/f <= 4):
                    if (kMax_temp >= maxTemp(cpu_num, f*kFreq[9])):
                        chromo.append(cpu_num)
                        heapq.heappush(util,(cpu_util, cpu_num))
                        j = 11
                    else:
                        j = 10
                else:
                    j += 1
            if j == 11:
                break
        if not util:
            return False
    chromo[0] = fitnessValue(0)
    return chromo

def hybridGAWF():
    fs = open('Schedule', 'a')
    fs.write("HybridWGA algorithm\n")
    fs.close()
    global pop
    global population_size
    buildPop(number_tasks, population_size)
    cores = int(math.ceil(float(kTot_util) / 4))
    comb_set = range(20)
    chromosomes = combinations(comb_set, cores)
    wf = []
    for i in chromosomes:
        chromo = buildChromo(i)
        if chromo:
            wf.append(chromo)
    chromosomes = combinations(comb_set, cores+1)
    for i in chromosomes:
        chromo = buildChromo(i)
        if chromo:
            wf.append(chromo)
    buildPop(number_tasks, population_size)
    if len(pop) >= len(wf):
        for i in range(len(wf)):
            pop[i] = copy.deepcopy(wf[i])
    else:
        pop = copy.deepcopy(wf)
        global max_elite
        global crossover_size
        global mutation_size
        population_size = len(pop)
        max_elite = int(population_size*0.01)
        crossover_size = int(population_size*0.85)
        mutation_size = int(population_size*0.005)
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
    minWF()
    hybridGAWF()
    return 0

##### This is the start of the program #####
def main():
    #num_tasks = [100, 150, 200, 300]
    #tot_util = [20, 35, 45]
    num_tasks = 100
    tot_util = 20
    pop_size = 2000

    #num_tasks = int(sys.argv[1])
    #tot_util = int(sys.argv[2])
    #pop_size = int(sys.argv[3])

    fs = open('Schedule', 'w')
    fs.write("Start scheduler\n\n")
    fs.close()

    tmp_num = num_tasks
    tmp_util = tot_util
    tmp_pop = pop_size

    fs = open('Schedule', 'a')
    fs.write("Task set: Num Tasks " + str(tmp_num) + " | Util " + str(tmp_util) + " | Pop Size " + str(tmp_pop) + "\n\n")
    fs.close()
    algorithms(tmp_num, tmp_util, tmp_pop)

if __name__ == '__main__':
    #if not len(sys.argv) == 4:
    #    sys.exit(1)
    #t = timeit.Timer("main()", setup="from __main__ import main")
    #fs1 = open('Timer', 'w')
    #fs1.write(str(t.timeit(number=1)) + "\n")
    #fs1.close()
    #print "Done"
    main()
    sys.exit(0)
