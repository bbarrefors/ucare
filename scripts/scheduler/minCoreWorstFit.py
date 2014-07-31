#!/usr/local/bin/python
#---------------------------------------------------------------------------------------------------
# Min-Core Worst-Fit Algorithm
#
# Make assumption that total utilization of cluster is sufficient to schedule all tasks
#---------------------------------------------------------------------------------------------------
import math, copy
from operator import itemgetter

cluster = []
freqs = []
maxTemps = []

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

#===================================================================================================
#  A L G O R I T H M
#===================================================================================================
def minCoreWorstFit(cluster_, freqs_, maxTemps_, taskSet, totUtil):
	print("MW")
	global cluster
	global freqs
	global maxTemps
	cluster = cluster_
	freqs = freqs_
	maxTemps = maxTemps_
	s = []
	performance = []
	for i in range(20):
		f = getMaxFreq(i)
		u = maxUtil(i, f)
		performance.append([i, u])
	performance = sorted(performance, reverse=True, key=itemgetter(1))
	chromo = []
	prevChromo = []
	done = 0
	for i in range(19, -1, -1):
		cores = copy.deepcopy(performance[:i])
		prevChromo = copy.deepcopy(chromo)
		chromo = [0]
		for task in taskSet:
			core = max(cores, key=itemgetter(1))
			if core[1] < task:
				done = 1
				break
			core[1] -= task
			chromo.append(core[0])
		if done:
			break
	return prevChromo