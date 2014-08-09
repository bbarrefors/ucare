#!/usr/local/bin/python
#---------------------------------------------------------------------------------------------------
# Hybrid Min-Core Worst-Fit Genetic Algorithm
#
# Make assumption that total utilization of cluster is sufficient to schedule all tasks
#---------------------------------------------------------------------------------------------------
import math, random, copy
from operator import itemgetter
from random import randint

cluster = []
freqs = []
maxTemps = []
taskSet = []

#===================================================================================================
#  H E L P E R S
#===================================================================================================
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
	tAmb = cluster[core]['t_amb']
	A = a1*r
	B = a3*r*f + a4*r - 1
	C = a2*r*math.pow(f,2) + a5*f*r + a6*r + tAmb
	maxTemp = -B/(2*A) - math.sqrt(math.pow(B,2) - 4*A*C)/(2*A)
	return maxTemp

def getMaxFreq(core):
	j = len(freqs[core]) - 1
	while(maxTemp(core, freqs[core][j]) > maxTemps[core]):
		j -= 1
	maxFreq = freqs[core][j]
	return maxFreq

def maxUtil(core, freq):
	maxUtil = 4*(freq/freqs[core][len(freqs[core])-1])
	return maxUtil

def generatePopulation(cores, popSize):
	pop = []
	for i in range(popSize):
		chromo = [0]
		for task in taskSet:
			c = random.choice(cores)
			chromo.append(c)
		pop.append(chromo)
	return 0, pop

def power(core, freq, util):
	# Based on cpu properties and a frequency, return the power consumption at maximum temperature
	f = freq
	a1 = cluster[core]['a1']
	a2 = cluster[core]['a2']
	a3 = cluster[core]['a3']
	a4 = cluster[core]['a4']
	a5 = cluster[core]['a5']
	a6 = cluster[core]['a6']
	r = cluster[core]['r']
	tAmb = cluster[core]['t_amb']
	t = maxTemp(core, f)
	p = a1*math.pow(t,2) + a2*math.pow(f,2) + a3*f*t + a4*t + a5*f + a6
	return p

def eMax():
	# power consumption added up assuming all cpu's ran on highest frequency
	eM = 0
	for cpu in range(20):
		p = power(cpu, freqs[cpu][len(freqs[cpu])-1], 4)
		eM += p
	return eM

def eChromo(pop, chromo):
	# Actual power consumption for task allocation.
	# If allocation doesn't comply w temperature restrictions it gets penalized
	eC = 0
	totUtil = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for gene in range(len(taskSet)):
		cpu = pop[chromo][gene+1]
		totUtil[cpu] += taskSet[gene]
	cpu = 0
	for util in totUtil:
		if not (util == 0):
			j = 0
			f = 0
			while (j < len(freqs[cpu])):
				f = freqs[cpu][j]/freqs[cpu][len(freqs[cpu])-1]
				if (util/f <= 4):
					if (maxTemps[cpu] < maxTemp(cpu, freqs[cpu][j])):
						j = 11
					else:
						break
				else:
					j += 1
			if (j < len(freqs[cpu])):
				eC += power(cpu, freqs[cpu][j], (util/(freqs[cpu][j]/freqs[cpu][len(freqs[cpu])-1]))/4)
			else:
				eC += freqs[cpu][len(freqs[cpu])-1]*10000
		cpu += 1
	return eC

def fitnessValue(pop, chromo):
	# e_max - e_chromo, the higher value the better
	eM = eMax()
	eC = eChromo(pop, chromo)
	fV = eM - eC
	return (-fV)

def compFloats(f1, f2):
	allowedError = 0.1
	return abs(f1 - f2) <= allowedError

def genetic(pop, popSize):
	maxElite = int(popSize*0.01)
	crossoverSize = int(popSize*0.85)
	mutationSize = int(popSize*0.01)
	maxConverge = 100
	maxGen = 1000
	generation = 0
	converge = 0
	bestFit = 0
	elitePop = []
	for chromo in range(len(pop)):
		fV = fitnessValue(pop, chromo)
		pop[chromo][0] = fV
	pop = sorted(pop, key=itemgetter(0))
	while ((generation < maxGen) and (converge < maxConverge)):
		generation += 1
		pop = sorted(pop, key=itemgetter(0))
		if compFloats(pop[0][0], bestFit):
			converge += 1
		else:
			bestFit = pop[0][0]
			converge = 1
		elitePop = copy.deepcopy(pop[:maxElite])
		# Crossover
		for i in range(crossoverSize):
			rand = randint(0,popSize-1)
			chromo1 = pop[i]
			chromo2 = pop[rand]
			point1 = randint(1, len(taskSet)-1)
			point2 = randint(1, len(taskSet)-1)
			if (point1 > point2):
				tmp = point1
				point1 = point2
				point2 = tmp
			for j in range(point1, point2):
				tmp = chromo1[j]
				chromo1[j] = chromo2[j]
				chromo2[j] = tmp
			pop[i] = copy.deepcopy(chromo1)
			pop[rand] = copy.deepcopy(chromo2)

		# Mutate
		for i in range(mutationSize):
			rand = randint(0, popSize-1)
			chromo = pop[rand]
			point1 = randint(1, len(taskSet)-1)
			point2 = randint(1, len(taskSet)-1)
			if (point1 > point2):
				tmp = point1
				point1 = point2
				point2 = tmp
			for j in range(point1, point2):
				chromo[j] = randint(0,19)

		# Copy back elite population
		for chromo in range(len(pop)):
			fV = fitnessValue(pop, chromo)
			pop[chromo][0] = fV
		pop = sorted(pop, key=itemgetter(0))
		pop[-maxElite:] = copy.deepcopy(elitePop[:])
	for chromo in range(len(pop)):
		fV = fitnessValue(pop, chromo)
		pop[chromo][0] = fV
	pop = sorted(pop, key=itemgetter(0))
	for chromo in range(len(pop)):
		pop[chromo][0] = -pop[chromo][0]
	print("Generations: " + str(generation))
	return pop

#===================================================================================================
#  A L G O R I T H M
#===================================================================================================
def hybridMinWorstGeneticAlgorithm(cluster_, freqs_, maxTemps_, taskSet_, totUtil, popSize, cores, mwChromo):
	global cluster
	global freqs
	global maxTemps
	global taskSet
	cluster = cluster_
	freqs = freqs_
	maxTemps = maxTemps_
	taskSet = taskSet_
	print("HyWGA")
	check = 1
	while check:
		check, pop = generatePopulation(cores, popSize)
	pop[popSize-1] = copy.deepcopy(mwChromo)
	pop = genetic(pop, popSize)
	return pop
