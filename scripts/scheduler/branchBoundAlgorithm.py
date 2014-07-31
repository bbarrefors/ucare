#!/usr/local/bin/python
#---------------------------------------------------------------------------------------------------
# Hybrid Min-Core Worst-Fit Genetic Algorithm
#
# Make assumption that total utilization of cluster is sufficient to schedule all tasks
#---------------------------------------------------------------------------------------------------
import math, heapq, copy, random
from operator import itemgetter

processors = []
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

def getMaxFreq(core):
	j = len(freqs[core]) - 1
	while(maxTemp(core, freqs[core][j]) > maxTemps[core]):
		j -= 1
	maxFreq = freqs[core][j]
	return maxFreq

def maxUtil(core, freq):
	maxUtil = 4*(freq/freqs[core][len(freqs[core])-1])
	return maxUtil

def generateChromo(cores):
	tasks = sorted(taskSet, reverse=True)
	U = dict()
	chromo = [0]
	for core in cores:
		f = getMaxFreq(core)
		u = maxUtil(core, f)
		U[core] = u
	for task in taskSet:
		c = max(U, key=U.get)
		if U[c] < task:
			return 1, chromo
		U[c] = U[c] - task
		chromo.append(c)
	return 0, chromo

def lowerBound(n, z, c, j):
	global processors
	z_hat = z
	c_hat = c
	sum_ = 0
	r = -1
	u = 0
	for k in range(j, n):
		sum_ += processors[k][3]
		if sum_ > c_hat:
			r = k
			break
	if r == -1:
		return -1
	u = sum(processors[k][2] for k in range(j, r)) + (c_hat - sum(processors[k][3] for k in range(j, r)))*processors[r][1]
	return z_hat + u

def branchAndBound(limit):
	global processors
	H = []
	n = 20
	X_hat = [0 for i in range(20)]
	j_hat = 0
	z_hat = 0
	c_hat = limit
	b_hat = lowerBound(n, z_hat, c_hat, j_hat)
	heapq.heappush(H, (b_hat, j_hat, X_hat, z_hat, c_hat))
	while j_hat <= n:
		s = heapq.heappop(H)
		j_hat = s[1]
		X_hat = copy.deepcopy(s[2])
		z_hat = s[3]
		c_hat = s[4]
		if j_hat == n:
			break
		j_hat += 1
		b_hat = lowerBound(n, z_hat, c_hat, j_hat)
		if not (b_hat == -1):
			heapq.heappush(H, (b_hat, j_hat, X_hat, z_hat, c_hat))
		Y_hat = copy.deepcopy(X_hat)
		Y_hat[j_hat-1] = 1
		z_hat += processors[j_hat-1][2]
		c_hat -= processors[j_hat-1][3]
		if c_hat < 0:
			b_hat = z_hat
			j_hat = n
		else:
			b_hat = lowerBound(n, z_hat, c_hat, j_hat)
		if not (b_hat == -1):
			heapq.heappush(H, (b_hat, j_hat, Y_hat, z_hat, c_hat))
		j_hat -= 1
	s = []
	for k in range(20):
		if X_hat[k] == 1:
			s.append(processors[k][0])
	return s

#===================================================================================================
#  A L G O R I T H M
#===================================================================================================
def branchBoundAlgorithm(cluster_, freqs_, maxTemps_, taskSet_, totUtil):
	global processors
	global cluster
	global freqs
	global maxTemps
	global taskSet
	cluster = cluster_
	freqs = freqs_
	maxTemps = maxTemps_
	taskSet = taskSet_
	processors = []
	for i in range(20):
		f = getMaxFreq(i)
		w = maxUtil(i, f)
		p = power(i, f, w)
		processors.append([i, p/w, p, w])
	processors = sorted(processors, key=itemgetter(1))
	print("BaB")
	check = 1
	minTask = max(taskSet)
	limit = totUtil
	while check:
		cores = branchAndBound(limit)
		check, chromo = generateChromo(cores)
		limit += minTask
	return cores, chromo