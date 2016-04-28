import heapq
import copy
from game import play
import numpy as np
import math
import random


crossingoverrate = .9
mutationrate = .05
species = 50
netsize = 20

base= [0,0,0,0,0,0]
######################NEURAL NET CLASS######################

class NeuralNet():
    def __init__(self, weights1=None, weights2=None):
        self.inputnodes = 2
        self.hiddennodes = 2
        self.outputnodes = 1
        if weights1 and weights2:
            self.weights1 = weights1
            self.weights2 = weights2
        else:
            self.random()
            
    def forward(self, inputvalues):
        hiddenlayeroutput = self.sigmoid(np.dot(inputvalues, self.weights1))
        output = self.sigmoid(np.dot(hiddenlayeroutput, self.weights2))
        return output

    def random(self):
        weightslist = []
        for weight in base:
            weightslist.append(weight + random.triangular(weight - .3, weight + .3))
        self.listtonet(weightslist)

    def nettolist(self):
        weightslist = []
        for i in self.weights1:
            weightslist.extend(i)
        for i in self.weights2:
            weightslist.extend(i)
        return weightslist

    def listtonet(self, weightslist):
        weights1 = []
        weights2 = []
        count = 0
        for i in xrange(self.inputnodes):
            n = [] 
            for j in xrange(self.hiddennodes):
                n.append(weightslist[count])
                count += 1
            weights1.append(n)
        for i in xrange(self.hiddennodes):
            n = [] 
            for j in xrange(self.outputnodes):
                n.append(weightslist[count])
                count += 1
            weights2.append(n)
        self.weights1 = weights1
        self.weights2 = weights2

    def sigmoid(self, n):
        return 1/(1 + np.exp(-n))

######################GENETIC ALGORITHM######################


def performance(n):
    #playing the game without displaying on screen
    return play(True,n)

def oldnetlist():
    netlist=[]
    for i in range (0,netsize):
        netelement = NeuralNet()
        netlist.append(netelement)
    return netlist

def updateweights(n1, n2):
        a= random.random()
	if a < crossingoverrate:
		weightslist1 = np.array(n1.nettolist())
		weightslist2 = np.array(n2.nettolist())
		child1 = [i * 0.5 for i in np.add(weightslist1, weightslist2)]
		child2 = [i * 0.5 for i in np.add(weightslist1, weightslist2)]
                b= random.random()
                c= random.random()
                if b < mutationrate:
                    index = random.randint(0, len(child1) - 1)
                    child1[index] += random.triangular(-1, 1) * child1[index]
                if c < mutationrate:
                    index = random.randint(0, len(child2) - 1)
                    child2[index] += random.triangular(-1, 1) * child2[index]
		n1.listtonet(child1)
		n2.listtonet(child2)
	return (n1, n2)

def survivaloffittest(pop):
	first = pop[random.randint(0, len(pop) - 1)]
	second = pop[random.randint(0, len(pop) - 1)]
	if performance(first) > performance(second):
            return first
        else:
            return second

def newnetlist(genome):
	newnetlist = []
	genome = sorted(genome, key=performance,reverse=True)
	print str(genome[0])
	newnetlist.extend(genome[0:5])
	while len(newnetlist) < len(genome):
		first = survivaloffittest(genome)
		second = survivaloffittest(genome)
		first, second = updateweights(first, second)
                newnetlist.append(first)
                newnetlist.append(second)
		#newnetlist.extend([first, second])
	return newnetlist


# start genetic algo
genome = oldnetlist()
for i in range(0,species):
    print '==========================='
    print 'GENERATION ' + str(i)
    genome = newnetlist(genome)
    play(False, genome[0])
    print str(genome[0])

