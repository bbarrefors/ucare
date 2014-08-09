#!/usr/local/bin/python
#---------------------------------------------------------------------------------------------------
# Driver for all schedulers
#
# Make assumption that total utilization of cluster is sufficient to schedule all tasks
#---------------------------------------------------------------------------------------------------
import sys, numpy, copy, random, math
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

from minCoreWorstFit import minCoreWorstFit
from geneticAlgorithm import geneticAlgorithm
from branchBoundAlgorithm import branchBoundAlgorithm
from hybridMinWorstGeneticAlgorithm import hybridMinWorstGeneticAlgorithm
from hybridBranchAndBoundGeneticAlgorithm import hybridBranchAndBoundGeneticAlgorithm

#===================================================================================================
#  C L U S T E R
#===================================================================================================
cluster = [{'t_amb' : -8.3, 'r': 0.646, 'a1': 0.0061, 'a2': 4.5036, 'a3': 0.0928, 'a4': -0.3536, 'a5': -4.660637, 'a6': 64.8758, 'util': 4, 'u1' : 247.01, 'u2' : 75.46, 'u0' : 429.51},
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
		   {'t_amb' : -8.8, 'r': 0.704, 'a1': -0.0151, 'a2': 5.6876, 'a3': 0.4642, 'a4': 0.6182, 'a5': -21.2384, 'a6': 54.0389, 'util': 4, 'u1' : 238.74, 'u2' : 87.32, 'u0' : 414.86}]

freqs = [[1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000],
		 [1.197000, 1.330000, 1.463000, 1.596000, 1.729000, 1.862000, 1.995000, 2.128000, 2.261000, 2.394000]]

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

def generateCluster():
	global cluster
	global freqs
	global maxTemps
	tmp = {'t_amb' : -10.0, 'r': 0.731, 'a1': -0.0040, 'a2': 5.5272, 'a3': 0.2977, 'a4': 0.0713, 'a5': -13.2765, 'a6': 56.4242, 'util': 4, 'u1' : 276.60, 'u2' : 114.0, 'u0' : 402.9}
	newCluster = []
	v = 0.0
	for node in cluster:
		newNode = dict()
		for k in node.keys():
			if k == 'a4':
				newNode[k] = v
			else:
				newNode[k] = tmp[k]
		v += 0.01
		newCluster.append(newNode)
	cluster = copy.deepcopy(newCluster)
	newFreqs = []
	for node in freqs:
		newNode = []
		for f in node:
			rand = random.uniform(0.95, 1.05)
			newNode.append(rand*f)
		newFreqs.append(sorted(newNode))
	freqs = copy.deepcopy(newFreqs)
	maxTemps = []
	for node in range(20):
		maxT = maxTemp(node, freqs[node][9]) - 1
		maxTemps.append(maxT)

def buildTaskSet(numTasks, totUtil):
	# Generate a random task set based on the tot util and num tasks
	# task_set is a list of floats where each float is the utilization for a task
	# [ task_util, task_util, ... ]
	taskSetPrime = []
	mean = float(totUtil)/float(numTasks)
	stdDev = mean/2.75
	util = abs(numpy.random.normal(mean, stdDev, numTasks))
	u = 0
	for i in util:
		u += i
		taskSetPrime.append(i)
	taskSet = []
	diff = totUtil - u
	rem = diff/numTasks
	carry = 0.0
	for task in taskSetPrime:
		task += rem
		u += task
		if carry > 0:
			task -= carry
		if task <= 0:
			carry = 2*abs(task)
			task = abs(task)
		else:
			carry = 0.0
		taskSet.append(task)
	if carry > 0:
		taskSet = buildTaskSet(numTasks, totUtil)
	return taskSet

def printPop(pop, taskSet):
	totalCores = 0
	s = set()
	for gene in range(len(pop[0][1:])):
		cpu = pop[0][gene+1]
		s.add(cpu)
	totalCores = len(s)
	print("The number of CPU's used is " + str(totalCores))
	totUtil = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for gene in range(len(pop[0][1:])):
		util = taskSet[gene]
		cpu = pop[0][gene+1]
		totUtil[cpu] += util
	i = 1
	for util in totUtil:
		print("%s\t%s" % (str(i), str(util)))
		i += 1
	print("")

#===================================================================================================
#  A L G O R I T H M S
#===================================================================================================
def algorithms(numTasks, totUtil):
	taskSet = buildTaskSet(numTasks, totUtil)
	mwChromo = minCoreWorstFit(cluster, freqs, maxTemps, taskSet, totUtil)
	popSize = 200
	cores = range(len(cluster))
	pop = hybridMinWorstGeneticAlgorithm(cluster, freqs, maxTemps, taskSet, totUtil, popSize, cores, mwChromo)
	printPop(pop, taskSet)
	cores, babChromo = branchBoundAlgorithm(cluster, freqs, maxTemps, taskSet, totUtil)
	pop = [babChromo]
	printPop(pop, taskSet)

#===================================================================================================
#  M A I N
#===================================================================================================
if __name__ == '__main__':
	numTasks = [250, 350, 450]
	totUtils = [25, 35, 45]
	#numTasks = [250]
	#totUtils = [25]

	generateCluster()

	print("Start schedulers\n")

	for totUtil in totUtils:
		for numTask in numTasks:
			print("Task set: Num Tasks " + str(numTask) + " | Util " + str(totUtil) + "\n")
			algorithms(numTask, totUtil)
	msg = MIMEText("Schedulers are done!")
	msg['Subject'] = "Job is done!"
	msg['From'] = "bbarrefo@cse.unl.edu"
	msg['To'] = "bbarrefo@cse.unl.edu"
	p = Popen(["/usr/sbin/sendmail", "-toi"], stdin=PIPE)
	p.communicate(msg.as_string())
	sys.exit(0)