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

cluster = ({'r': 0.3685, 'a1': 0.0061, 'a2': 4.5036, 'a3': 0.0928, 'a4': -0.3536, 'a5': -4.660637, 'a6': 64.8758, 'util': 4}, {'r': 0.3685, 'a1': 0.0248, 'a2': 8.1349, 'a3': -0.2863, 'a4': -1.3203, 'a5': 2.6106, 'a6': 75.4638, 'util': 4}, {'r': 0.3685, 'a1': -0.0040, 'a2': 5.5272, 'a3': 0.2977, 'a4': 0.0713, 'a5': -13.2765, 'a6': 56.4242, 'util': 4}, {'r': 0.3685, 'a1': 0.0338, 'a2': 7.4625, 'a3': -0.4637, 'a4': -1.7374, 'a5': 10.1535, 'a6': 78.6566, 'util': 4}, {'r': 0.3685, 'a1': 0.0335, 'a2': 13.8525, 'a3': -0.6544, 'a4': -1.4578, 'a5': 1.1880, 'a6': 75.7025, 'util': 4}, {'r': 0.3685, 'a1': 0.0069, 'a2': 7.3865, 'a3': 0.0405, 'a4': -0.4351, 'a5': -6.9793, 'a6': 61.1205, 'util': 4}, {'r': 0.3685, 'a1': 0.0069, 'a2': 7.3865, 'a3': 0.0405, 'a4': -0.4351, 'a5': -6.9793, 'a6': 61.1205, 'util': 4}, {'r': 0.3685, 'a1': 0.0069, 'a2': 7.3865, 'a3': 0.0405, 'a4': -0.4351, 'a5': -6.9793, 'a6': 61.1205, 'util': 4})

kFreq = (1.97000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000)

task_set = []
pop = []
kHyper_period = 1000
kTot_util = 0
kMax_gen = 10
kMax_converge = 10
kT_amb = 26
kMax_temp = 60
large_integer = 1000

def buildTaskSet(num_tasks, tot_util):
    # Generate a random task set based on the tot util and num tasks
    # task_set is a lost of floats where each float is the utilization for a task
    # [ task_util, task_util, ... ]
    # CHECKED : WORKS
    print "Building task set"
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
    print "Building population"
    global pop
    pop = []
    for i in range(pop_size):
        chromo = [0]
        for j in range(num_tasks):
            chromo.append([task_set[j], randint(0,7), 0])
        pop.append(chromo)
    return 1

def maxTemp(core, freq):
    # Based on cpu properties and frequency, return the maximum possible temperature for core
    # TODO : Half accurate but need to get correct constants for cluster
    f = freq
    a1 = cluster[core]['a1']
    a2 = cluster[core]['a2']
    a3 = cluster[core]['a3']
    a4 = cluster[core]['a4']
    a5 = cluster[core]['a5']
    a6 = cluster[core]['a6']
    r = cluster[core]['r']
    A = a1*r
    B = a3*r*f + a4*r - 1
    C = a2*r*math.pow(f,2) + a5*f*r + a6*r + kT_amb
    max_temp = -B/(2*A) - math.sqrt(math.pow(B,2) - 4*A*C)/(2*A)
    return max_temp

def power(core, freq):
    # Based on cpu properties and a frequency, return the power consumption at maximum temperature
    # TODO : Fairly accurate but not correct values for cluster constants most likely
    # PENDING : Waiting for maxTemp function to work
    f = freq
    a1 = cluster[core]['a1']
    a2 = cluster[core]['a2']
    a3 = cluster[core]['a3']
    a4 = cluster[core]['a4']
    a5 = cluster[core]['a5']
    a6 = cluster[core]['a6']
    r = cluster[core]['r']
    t = maxTemp(core, freq)
    power1 = a1*math.pow(t,2) + a2*math.pow(f,2) + a3*f*t + a4*t + a5*f + a6
    return power1

def eMax(chromo):
    # power consumption added up assuming all cpu's ran on highest frequency
    # PENDING : Waiting for maxTemp and power formula to work
    e_max = 0
    for gene in pop[chromo][1:]:
        power2 = power(gene[1], kFreq[9])
        e_max += power2
    return e_max
 
def eChromo(chromo):
    # Actual power consumption for task allocation. 
    # If allocation doesn't comply w temperature restrictions it gets penalised
    # PENDING : Waiting for maxTemp and power forumala to work
    global pop
    e_chromo = 0
    for gene_i in range(len(pop[chromo][1:])):
        gene_i += 1
        gene = pop[chromo][gene_i]
        util = gene[0]
        core = gene[1]
        j = 0
        f = 0
        while (j <= 9):
            f = kFreq[j]/kFreq[9]
            if (f >= util):
                if (kMax_temp >= maxTemp(core, f)):
                    pop[chromo][gene_i][2] = f
                    j = 11
                else:
                    j = 10
            else:
                j += 1
        if (j == 10):
            pop[chromo][gene_i][2] = f
            e_chromo += f*large_integer
        else:
            e_chromo += power(core, f)
    return e_chromo

def fitnessValue(chromo):
    # e_max - e_chromo, the higher value the better
    # PENDING : Waiting for maxTemp and power formula to work
    e_max = eMax(chromo)
    e_chromo = eChromo(chromo)
    fitness_value = e_max - e_chromo
    return fitness_value

def minWF():
    # Select the core with least available util left that can satisfy the conditions
    # to schedule tasks on.
    # Create one chromosome based on that scheduling philosophy
    print "MinWF algorithm"
    global pop
    pop = []
    chromo = [0]
    util = []
    i = 0
    for cpu in cluster:
        heapq.heappush(util, (cpu['util'], i))
        i += 1
    for task_util in task_set:
        while util:
            cpu = heapq.heappop(util)
            cpu_num = cpu[1]
            j = 0
            f = 0
            while (j <= 9):
                f = kFreq[j]/kFreq[9]
                if (f >= task_util and f <= cpu[0]):
                    if (kMax_temp >= maxTemp(cpu_num, f)):
                        chromo.append((task_util, cpu_num, f))
                        j = 11
                    else:
                        j = 10
                else:
                    j += 1
            if (j == 11):
                cpu = (cpu[0]-task_util, cpu[1])
                heapq.heappush(util, cpu)
                break
        if not util:
            print "failed"
            return 1
    pop.append(chromo)
    total_energy = eChromo(0)
    max_energy = eMax(0)
    print "Max energy " + str(max_energy)
    print "Total energy " + str(total_energy)
    print pop[0]
    return 0

def genetic():
    # TODO : Sort population based on fitness value
    # PENDING : Waiting for maxTemp and power formulas to work
    print "Genetic algorithm"
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
    total_energy = eChromo(0)
    max_energy = eMax(0)
    print "Max energy " + str(max_energy)
    print "Total energy " + str(total_energy)
    print pop[0]
    return 1

def hybridGAWF(num_tasks, tot_util):
    print "HybridGAWF algorithm"
    global pop
    wf_chromo = pop[0]
    buildPop(num_tasks, tot_util)
    pop[0] = wf_chromo
    genetic()
    total_energy = eChromo(0)
    max_energy = eMax(0)
    print "Max energy " + str(max_energy)
    print "Total energy " + str(total_energy)
    print pop[0]
    return 1

def algorithms(num_tasks, tot_util, pop_size):
    # PENDING : Waiting for genetic algorithm
    # PENDIng : Waiting for Worst Fit algorithm
    # Create a random task set
    buildTaskSet(num_tasks, tot_util)
    # Create random population for genetic alg
    buildPop(num_tasks, pop_size)
    # Call algorithms
    # Run genetic w random population, print results
    genetic()
    #minWF()
    #hybridGAWF(num_tasks, tot_util)
    # Run MinWF, print results
    #if minWF() == 0:
    #    return 0
    # Feed MinWF into Genetic, print results
    return 1

##### This is the start of the program #####

#num_tasks = [100, 150, 200, 300];
#tot_util = [20, 35, 45];
#pop_size = [2000, 10000];

num_tasks = [100];
tot_util = [20];
pop_size = [20];

for tmp_num in num_tasks:
    print "Next task set"
    for tmp_util in tot_util:
        print "Next total utilization"
        for tmp_pop in pop_size:
            print "Next population size"
            print "Task set: Num Tasks ", tmp_num, " | Util ", tmp_util, " | Pop Size ", tmp_pop
            algorithms(tmp_num, tmp_util, tmp_pop)
print "Done"
